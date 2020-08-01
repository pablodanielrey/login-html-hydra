import logging
import redis
import json
import uuid
import re
from datetime import timedelta, datetime

from . import UserCredentials, MailTypes, User
from .db import open_login_session, open_users_session, open_redis_session
from .models import loginModel, usersModel

class ResetCredentialsModel:

    def __init__(self, mailsModel, googleSyncModel):
        self.mailsModel = mailsModel
        self.googleSyncModel = googleSyncModel
        self.r = re.compile(r"""^\d+$""")

    def delete_reset_info(self, rid):
        with open_redis_session() as r:
            data = r.get(rid)
            ri = json.loads(data)
            r.delete(ri['username'])
            r.delete(ri['reset_code'])
            r.delete(rid)

    def get_reset_info(self, cid):
        with open_redis_session() as r:
            if cid not in r:
                raise Exception(f'El código {cid} no existe')
            data = r.get(cid)
            assert data is not None
            return json.loads(data)

    def get_indexed_reset_info(self, cid):
        with open_redis_session() as r:
            if cid not in r:
                raise Exception(f'El código {cid} no existe')
            rid = r.get(cid)
            if rid not in r:
                raise Exception(f'El código {rid} no existe')
            data = r.get(rid)
            assert data is not None
            return json.loads(data)

    def generate_reset_info(self, username):
        try:
            data = self.get_indexed_reset_info(username)
            return data
        except Exception:
            pass

        """
        with open_redis_session() as r:
            if username in r:
                rid = r.get(username).decode('utf-8')
                data = r.get(rid)
                assert data is not None
                return json.loads(data)
        """

        types = [MailTypes.NOTIFICATION, MailTypes.ALTERNATIVE, MailTypes.INSTITUTIONAL]
        with open_login_session() as session:
            uc = session.query(UserCredentials).filter(UserCredentials.username == username, UserCredentials.deleted == None).one()
            uid = uc.user_id
        with open_users_session() as session:
            # pylint: disable=no-member
            user = session.query(User).filter(User.id == uid).one()
            confirmed = [m.email for m in user.mails if m.confirmed and m.deleted == None and m.type in types]
            user_data = {'firstname':user.firstname, 'lastname': user.lastname}

        if len(confirmed) <= 0:
            raise Exception(f'{username} no tiene cuentas alternativas confirmadas')

        code = str(uuid.uuid4()).replace('-','')[:5]
        rid = str(uuid.uuid4()).replace('-','')
        reset_code = str(uuid.uuid4()).replace('-','')

        reset = {
            'id': rid,
            'code': code,
            'mails': confirmed,
            'username': username,
            'reset_code': reset_code,
            'uid': uid
        }

        with open_redis_session() as r:
            data = json.dumps(reset)
            timeout = timedelta(minutes=20)
            r.setex(username, timeout, value=rid)
            r.setex(reset_code, timeout, value=rid)
            r.setex(rid, timeout, value=data)

            try:
                r = self.mailsModel.send_code(code, user=user_data, tos=confirmed)
                """ me falta analizar si existe alguna respuesta inválida para el envío de correos """
                
            except Exception as e:
                r.delete(rid)
                raise e


        return reset

    def send_email(self, reset):
        emails = reset['mails']

    def verify_code(self, cid, code):
        ri = self.get_reset_info(cid)
        if ri['code'] != code:
            raise Exception('Código incorrecto')
        return ri['reset_code']

    def reset_credentials(self, reset_code, password):
        ri = self.get_indexed_reset_info(reset_code)
        uid = ri['uid']
        username = ri['username']

        """ si tiene usuario en google intento cambiar primero las credenciales remotamente """
        for mail in ri['mails']:
            if 'econo.unlp.edu.ar' in mail:
                if not self.r.match(username):
                    raise Exception('el usuario no cumple con los parámetros establecidos')
                r = self.googleSyncModel.sync_login(username, password)
                assert r is not None
                break

        with open_login_session() as session:
            loginModel.change_credentials(session, uid, username, password)
            session.commit()

        self.delete_reset_info(ri['id'])

from .MailsModel import mailsModel
from .google.GoogleSyncModel import googleSyncModel
resetCredentialsModel = ResetCredentialsModel(mailsModel, googleSyncModel)
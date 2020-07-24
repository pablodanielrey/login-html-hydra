import redis
import json
import uuid
from datetime import timedelta

from . import UserCredentials, MailTypes, User
from .db import open_login_session, open_users_session, open_redis_session
from .models import loginModel, usersModel

class CredentialsModel:

    def generate_reset_info(self, username):
        with open_redis_session() as r:
            if username in r:
                data = r.get(username)
                return json.loads(data)

        types = [MailTypes.NOTIFICATION, MailTypes.ALTERNATIVE]
        with open_login_session() as session:
            uc = session.query(UserCredentials).filter(UserCredentials.username == username, UserCredentials.deleted == None).one()
            uid = uc.user_id
        with open_users_session() as session:
            user = session.query(User).filter(User.id == uid).one()
            confirmed = [m.email for m in user.mails if m.confirmed and m.deleted == None and m.type in types]

        if len(confirmed) <= 0:
            raise Exception(f'{username} no tiene cuentas alternativas confirmadas')

        code = str(uuid.uuid4()).replace('-','')[:5]
        rid = str(uuid.uuid4()).replace('-','')

        reset = {
            'id': rid,
            'code': code,
            'mails': confirmed,
            'username': username,
            'uid': uid
        }

        with open_redis_session() as r:
            data = json.dumps(reset)
            timeout = timedelta(minutes=20)
            r.setex(username, timeout, value=data)

        return reset

    def send_email(reset):
        emails = reset['mails']


credentialsModel = CredentialsModel()
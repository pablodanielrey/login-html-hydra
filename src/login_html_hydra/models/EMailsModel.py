import uuid
import datetime
import base64
import logging
import os

from email.mime.text import MIMEText
from email.header import Header

class EMailsModel:


    @staticmethod
    def _aplicar_filtros_comunes(q, offset, limit):
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q

    @classmethod
    def correos(cls, mid=None, solo_pendientes=False, offset=None, limit=None):
        session = Session()
        try:
            q = session.query(Mail)
            q = q.filter(Mail.id == mid) if mid else q
            q = q.filter(Mail.enviado == None) if solo_pendientes else q
            q = cls._aplicar_filtros_comunes(q, offset,limit)
            return q.all()
        finally:
            session.close()


    @classmethod
    def enviar_correo(cls, sistema, de, para, asunto, cuerpo):
        ''' inserta un correo en la cola para ser enviado (se supone codificación base64 urlsafe) '''
        session = Session()
        try:
            mail = Mail(sistema=sistema, de=de, para=para, asunto=asunto, cuerpo=cuerpo)
            session.add(mail)
            session.commit()
        finally:
            session.close()

    @classmethod
    def enviar_correos_pendientes(cls):
        enviados = []
        session = Session()
        try:
            cantidad = session.query(Mail).filter(Mail.enviado == None).count()
            if cantidad <= 0:
                return {'pendientes':cantidad, 'enviados':[]}
            service = cls._get_google_service()
            pendientes = session.query(Mail).filter(Mail.enviado == None).all()
            for m in pendientes:
                try:
                    cuerpo = base64.urlsafe_b64decode(m.cuerpo)
                    r = cls._enviar_correo_google(service, m.de, m.para, m.asunto, cuerpo)
                    m.respuesta = str(r)
                    m.enviado = datetime.datetime.now()
                    session.commit()
                    enviados.append(m.id)

                except Exception as e:
                    logging.exception(e)

        finally:
            session.close()
        return {'pendientes':cantidad, 'enviados':enviados}

    def _get_google_service(self):
        service = GAuthApis.getService('gmail', 'v1', 'sistemas@econo.unlp.edu.ar')
        return service

    @classmethod
    def _enviar_correo_google(cls, service, de, para, asunto, cuerpo):
        ''' https://developers.google.com/gmail/api/guides/sending '''

        correo = MIMEText(cuerpo, 'html', 'utf-8')
        correo['to'] = para
        correo['from'] = de
        correo['subject'] = Header(asunto, 'utf-8')
        urlsafe = base64.urlsafe_b64encode(correo.as_string().encode()).decode()

        r = service.users().messages().send(userId=cls.EMAILS_GOOGLE_USER, body={'raw':urlsafe}).execute()
        return r

"""
    http://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.html
    https://developers.google.com/identity/protocols/oauth2/scopes#gmail
    https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md

"""

import uuid
import datetime
import base64
import logging
import os
import inject

from googleapiclient.discovery import Resource

from email.mime.text import MIMEText
from email.header import Header

from jinja2 import Environment, PackageLoader, FileSystemLoader

class MailsModelMock:
    
    def send_code(code, user, tos=[]):
        """ retorno algo no nulo """
        return []

class MailsModel:

    @inject.autoparams()
    def __init__(self, gmail: Resource):
        self.env = Environment(loader=PackageLoader('login_html_hydra.models.templates','.'))
        self.gmail = gmail

    def _send_email(self, _from, mail):
        urlsafe = base64.urlsafe_b64encode(mail.as_string().encode()).decode()
        r = self.gmail.users().messages().send(userId=_from, body={'raw':urlsafe}).execute()
        return r

    def send_code(self, code, user, tos=[]):
        _from = 'sistemas@econo.unlp.edu.ar'
        subject = 'Reseteo de Clave FCE'
        
        code_tmpl = self._load_code_template()
        body = code_tmpl.render(code=code,user=user)

        responses = []
        for to in tos:
            mail = MIMEText(body, 'html', 'utf-8')
            mail['to'] = to
            mail['from'] = _from
            mail['subject'] = Header(subject, 'utf-8')
            r = self._send_email(_from, mail)
            responses.append(r)
        return responses

    def _load_code_template(self):
        code_tmpl = self.env.get_template('code.tmpl')
        return code_tmpl

"""
    https://developers.google.com/admin-sdk/directory/v1/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/
"""

import os
import datetime
import uuid
import logging
import json

import googleapiclient

from login_html_hydra.models.ResetCredentialsModel import InvalidCredentials

class GoogleSyncModel:

    def __init__(self, service):
        self.service = service

    def _get_google_uid(self, username):
        return f"{username}@econo.unlp.edu.ar"

    def sync_login(self, username, credentials):
        # pylint: disable=no-member
        usr = self._get_google_uid(username)

        """ https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/admin_directory_v1.users.html """
        self.service.users().get(userKey=usr).execute()
        data = {}
        data["changePasswordAtNextLogin"] = False
        data['password'] = credentials
        try:
            r = self.service.users().update(userKey=usr,body=data).execute()
            if not r:
                raise Exception(r.response)

        except googleapiclient.errors.HttpError as e:
            if e.resp.status == 400:
                raise InvalidCredentials()
            else:
                raise e

        return r


""" obtengo al api de gmail e instancio el modelo de mails """

from login_html_hydra import config
from .Google import get_api, get_credentials

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
FROM = 'sistemas@econo.unlp.edu.ar'

def _get_api(_from):
    path = config.CredentialsEnv.PATH
    creds = get_credentials(path, _from, SCOPES)
    api = get_api('admin', 'directory_v1', creds)
    return api

googleSyncModel = GoogleSyncModel(_get_api(FROM))    
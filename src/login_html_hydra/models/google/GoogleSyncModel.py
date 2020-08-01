"""
    https://developers.google.com/admin-sdk/directory/v1/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/
"""

import os
import datetime
import uuid
import logging
import json



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
        r = self.service.users().update(userKey=usr,body=data).execute()
        if not r:
            raise Exception(r.response)

        return r


""" obtengo al api de gmail e instancio el modelo de mails """

from .Google import get_api, get_credentials

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
FROM = 'sistemas@econo.unlp.edu.ar'

def _get_api(_from):
    #creds = get_credentials('/src/gitlab/kubernetes/servicios/oidc/login-html/adminecono-173018-66641a886c34.json', _from, SCOPES)
    #creds = get_credentials('/src/gitlab/kubernetes/servicios/oidc/login-html/adminecono-173018-b77dfc44f95a.json', _from, SCOPES)
    creds = get_credentials('/src/gitlab/stacks/fce/emails/credentials/credentials.json', _from, SCOPES)
    api = get_api('admin', 'directory_v1', creds)
    return api

googleSyncModel = GoogleSyncModel(_get_api(FROM))    
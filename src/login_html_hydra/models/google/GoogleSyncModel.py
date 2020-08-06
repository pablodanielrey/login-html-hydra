"""
    https://developers.google.com/admin-sdk/directory/v1/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/
"""

import os
import datetime
import uuid
import logging
import json
import inject

import googleapiclient
from googleapiclient.discovery import Resource

from login_html_hydra.models.exceptions import InvalidCredentials


class AdminResource(Resource):
    pass


class GoogleSyncModelMock:

    def sync_login(self, username, credentials):
        """ retornamos algo distinto de None """
        return {}


class GoogleSyncModel:

    @inject.autoparams()
    def __init__(self, service: AdminResource):
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

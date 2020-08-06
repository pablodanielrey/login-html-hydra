import os

version = '0.0.4'

#CONFIG DE USERS
class UserEnv:
    DB_USER = os.environ.get('USERS_DB_USER')
    DB_PASSWORD = os.environ.get('USERS_DB_PASSWORD')
    DB_HOST = os.environ.get('USERS_DB_HOST')
    DB_PORT = os.environ.get('USERS_DB_PORT',5432)
    DB_NAME = os.environ.get('USERS_DB_NAME')

#CONFIG DE LOGIN
class LoginEnv:
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ.get('DB_PORT',5432)
    DB_NAME = os.environ['DB_NAME']

class HydraEnv:
    HYDRA_ADMIN_URL = os.environ.get('HYDRA_ADMIN_URL')
    VERIFY_HTTPS = bool(int(os.environ.get('VERIFY_HTTPS',0)))

class RedisEnv:
    HOST = os.environ.get('REDIS_HOST', '0.0.0.0')
    PORT = os.environ.get('REDIS_PORT', '6379')


class CredentialsEnv:
    PATH = os.environ.get('CREDENTIALS_PATH', '/credentials/credentials.json')


def _get_admin_api(_from, scopes):
    from login_html_hydra import config
    from .models.google.Google import get_api, get_credentials

    SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
    FROM = 'sistemas@econo.unlp.edu.ar'

    path = CredentialsEnv.PATH
    creds = get_credentials(path, FROM, SCOPES)
    api = get_api('admin', 'directory_v1', creds)
    return api

def _get_gmail_api():
    from login_html_hydra import config
    from .models.google.Google import get_credentials, get_api

    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    FROM = 'sistemas@econo.unlp.edu.ar'

    path = CredentialsEnv.PATH
    creds = get_credentials(path, FROM, SCOPES)
    api = get_api('gmail', 'v1', creds)     
    return api

def config_prod(binder):
    """
        Configura el ambiente de producción
    """
    from googleapiclient.discovery import Resource
    from .models.google.GoogleSyncModel import AdminResource
    from .models.HydraApi import HydraApi

    binder.bind_to_provider(Resource, _get_gmail_api)
    binder.bind_to_provider(AdminResource, _get_admin_api)
    binder.bind(HydraApi, HydraApi(HydraEnv.HYDRA_ADMIN_URL, HydraEnv.VERIFY_HTTPS))

def config_dev(binder):
    """
        Configura un ambiente de desarrollo web
    """
    from login.model.LoginModel import LoginModel
    from users.model.UsersModel import UsersModel

    from .models.HydraApi import HydraApi
    from .models.google.GoogleSyncModel import GoogleSyncModel, GoogleSyncModelMock
    from .models.MailsModel import MailsModel, MailsModelMock

    binder.bind(LoginModel, LoginModel())
    binder.bind(UsersModel, UsersModel())
    binder.bind(HydraApi, HydraApi(HydraEnv.HYDRA_ADMIN_URL, HydraEnv.VERIFY_HTTPS))
    binder.bind(GoogleSyncModel, GoogleSyncModelMock())
    binder.bind(MailsModel, MailsModelMock())



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
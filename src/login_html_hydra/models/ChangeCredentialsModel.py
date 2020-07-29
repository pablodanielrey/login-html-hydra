import json
import uuid
from datetime import timedelta

from .db import open_login_session, open_users_session, open_redis_session
from .models import loginModel, usersModel

class ChangeCredentialsModel:


    def _generate_credentials(self, config):

        code = str(uuid.uuid4()).replace('-','')[:10]
        change = {
            'uid': config['uid'],
            'username': config['username'],
            'password': config['password']
        }

        with open_redis_session() as r:
            data = json.dumps(change)
            timeout = timedelta(minutes=20)
            r.setex(code, timeout, value=data)

        return code


    def change_credentials(self, code, password):

        with open_redis_session() as r:
            data = r.get(code)
            change = json.loads(data)

        uid = change['uid']
        username = change['username']
        credentials = change['password']

        with open_login_session() as session:
            loginModel.change_credentials(session, uid, username, credentials)

        return 'https://lsdfsdfsdf'
    

changeCredentialsModel = ChangeCredentialsModel()
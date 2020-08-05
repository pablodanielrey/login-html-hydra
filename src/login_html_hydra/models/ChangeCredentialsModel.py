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
            'return_url': config['return_url']
        }

        with open_redis_session() as r:
            data = json.dumps(change)
            timeout = timedelta(minutes=20)
            r.setex(code, timeout, value=data)

        return code

    def change_credentials(sefl, code, creds):
        pass

changeCredentialsModel = ChangeCredentialsModel()
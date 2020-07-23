

import uuid

valid_challenge = 'validchallenge'
invalid_challenge = str(uuid.uuid4())

class UserConf:
    uid: str
    firstname: str
    lastname: str
    dni: str
    imail: str
    email: str
    
class PassConf:
    username: str
    credentials: str
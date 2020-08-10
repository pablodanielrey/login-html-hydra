
from . import UserConf, PassConf, valid_challenge, invalid_challenge

def get_config():
    u = UserConf()
    u.firstname = 'username'
    u.lastname = 'lastname'
    u.dni = '21324234'
    u.imail = '70000001@econo.unlp.edu.ar'
    u.email = 'pablodanielrey@gmail.com'

    p = PassConf()
    p.username = 'secretusername'
    p.credentials = 'secretcredentials'

    return {
        'user': u,
        'credentials': p,
        'challenge': valid_challenge
    }
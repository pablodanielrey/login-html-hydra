
from . import UserConf, PassConf, valid_challenge, invalid_challenge

def get_config():
    u = UserConf()
    u.firstname = 'username'
    u.lastname = 'lastname'
    u.dni = '21324234'
    u.imail = 'ditesi@econo.unlp.edu.ar'
    u.email = 'ditesi@econo.unlp.edu.ar'

    p = PassConf()
    p.username = 'secretusername'
    p.credentials = 'secretcredentials'

    u2 = UserConf()
    u2.firstname = 'wrongusername'
    u2.lastname = 'wronglastname'
    u2.dni = '2234'
    u2.imail = 'wrongtestuser@econo.unlp.edu.ar'
    u2.email = 'wrongtestuser@gmail.com'

    p2 = PassConf()
    p2.username = 'wrongusername'
    p2.credentials = 'wrongpassword'

    return {
        'user': u,
        'user_err': u2,
        'credentials': p,
        'credentials_err': p2,
        'challenge': valid_challenge,
        'invalid_challenge': invalid_challenge
    }
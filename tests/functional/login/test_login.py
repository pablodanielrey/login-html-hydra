import pytest
import requests


def test_login_ok(httpserver):
    challenge = 'algodechallengeopaco'
    login_url = httpserver.url:_for('')
    params = {
        'username': 'usuario',
        'password': 'clave',
        'challenge': challenge
    }
    r = requests.post(login_url, params, allow_redirects=False)
    assert r.status_code == 200
    assert challenge in r.text
    assert 'Error de usuario' in r.text 

    

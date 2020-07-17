import pytest
import requests

login_url = 'http://localhost:5000/login/'

def test_login_ok():
    params = {
        'username': 'a',
        'password': '',
        'challenge': 'challenge no valido'
    }
    r = requests.post(login_url, params, allow_redirects=False)
    pytest.fail(str(r.status_code))
    

import requests
import pytest
import time

pytest_plugins = ["docker_compose"]

@pytest.fixture(scope='module')
def wait_for_api(module_scoped_container_getter):
    """ espera hasta que los contendores estén levantados y se pueda conectar a la api correctamente """
    time.sleep(10)
    service = module_scoped_container_getter.get("web").network_info[0]
    api_url = f"http://{service.hostname}:{service.host_port}/"
    return api_url

def test_login_ok(wait_for_api):
    login_url = wait_for_api

    challenge = 'algodechallengeopaco'
    params = {
        'username': 'usuario',
        'password': 'clave',
        'challenge': challenge
    }
    r = requests.post(login_url, params, allow_redirects=False)
    assert r.status_code == 200
    assert challenge in r.text
    assert 'Error de usuario' in r.text 

    

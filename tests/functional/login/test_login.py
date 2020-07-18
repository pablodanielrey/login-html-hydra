import requests
import pytest
import time

pytest_plugins = ["docker_compose"]


@pytest.fixture(scope='module')
def wait_for_api(module_scoped_container_getter):
    """ espera hasta que los contendores estén levantados y se pueda conectar a la api correctamente """
    time.sleep(10)

    users = module_scoped_container_getter.get('db_users').network_info[0]
    login = module_scoped_container_getter.get('db_login').network_info[0]

    service = module_scoped_container_getter.get("hydra").network_info[0]
    hydra_api_url = f"http://{service.hostname}:{service.host_port}/"    

    data = {
        'hydra_api_url': hydra_api_url,
        'users_db_host': users.hostname,
        'users_db_port': users.host_port,
        'login_db_host': login.hostname,
        'login_db_port': login.host_port
    }
    return data

@pytest.fixture(scope='module')
def client(wait_for_api):

    data = wait_for_api

    """ agrego las variables de entorno adecuadas """
    import os
    os.environ['USERS_DB_USER'] = 'users'
    os.environ['USERS_DB_PASSWORD'] = 'clavesuperultrarecontrasecreta'
    os.environ['USERS_DB_NAME'] = 'users'
    os.environ['USERS_DB_HOST'] = data['users_db_host']
    os.environ['USERS_DB_PORT'] = data['users_db_port']

    os.environ['DB_USER'] = 'login'
    os.environ['DB_PASSWORD'] = 'clavesuperultrarecontrasecreta'
    os.environ['DB_NAME'] = 'login'
    os.environ['DB_HOST'] = data['login_db_host']
    os.environ['DB_PORT'] = data['login_db_port']

    os.environ['HYDRA_ADMIN_URL'] = data['hydra_api_url']



    """ agrego el path del sistema para poder instanciarlo """
    import sys
    sys.path.append('../../src/')

    from login_html_hydra.web.app import webapp
    webapp.config['TESTING'] = True
    with webapp.test_client() as client:
        client
        with webapp.app_context():
            yield client


"""
def test_login_ok(wait_for_api, client):
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
"""

def test_login_get(wait_for_api, client):
    query = {
        'login_challenge': 'asdfdssdfsdsdfd'
    }
    r = client.get('/login',query_string=query)

def test_login_ok(wait_for_api, client):
    challenge = 'algodechallengeopaco'
    params = {
        'username': 'usuario',
        'password': 'clave',
        'challenge': challenge
    }
    r = client.post('/login', data=params)
    assert r.status_code == 308
    pytest.fail(r.text)

    r = client.post('/login/', data=params)
    assert challenge in r.text
    assert 'Error de usuario' in r.text     
   

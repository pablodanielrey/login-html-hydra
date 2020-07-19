import requests
import pytest
import time
import uuid
import datetime

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
def prepare_enfironment(wait_for_api):
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



@pytest.fixture(scope='module')
def prepare_dbs(prepare_enfironment):
    """
        genera un usuario de testing dentro de las bases de datos.
    """
    from users.model.entities.User import User, Mail, MailTypes, IdentityNumber, IdentityNumberTypes
    from login.model.entities.Login import UserCredentials
    from login_html_hydra.models.db import open_users_session, open_login_session

    uid = str(uuid.uuid4())
    with open_users_session() as session:
        
        u = User()
        u.id = uid
        u.name = 'name'
        u.lastname = 'lastname'
        session.add(u)

        i = IdentityNumber()
        i.id = str(uuid.uuid4())
        i.user_id = uid
        i.number = '12345678'
        i.type = IdentityNumberTypes.DNI
        session.add(i)

        m = Mail()
        m.id = str(uuid.uuid4())
        m.confirmed = True
        m.email = 'testuser@econo.unlp.edu.ar'
        m.type = MailTypes.INSTITUTIONAL
        m.user_id = uid
        session.add(m)

        m = Mail()
        m.id = str(uuid.uuid4())
        m.confirmed = True
        m.email = 'testuser@alternative.com'
        m.type = MailTypes.ALTERNATIVE
        m.user_id = uid
        session.add(m)

    with open_login_session() as session:

        uc = UserCredentials()
        uc.id = str(uuid.uuid4())
        uc.created = datetime.datetime.utcnow()
        uc.user_id = uid
        uc.username = 'username'
        uc.password = 'password'
        session.add(uc)


@pytest.fixture(scope='module')
def client(prepare_enfironment):

    from login_html_hydra.web.app import webapp
    webapp.config['TESTING'] = True
    with webapp.test_client() as client:
        client
        with webapp.app_context():
            yield client


def test_login_get(prepare_dbs, client):
    query = {
        'login_challenge': 'asdfdssdfsdsdfd'
    }
    r = client.get('/login',query_string=query)

def test_login_ok(prepare_dbs, client):
    challenge = 'algodechallengeopaco'
    params = {
        'username': 'username',
        'password': 'password',
        'challenge': challenge
    }
    r = client.post('/login', data=params)
    assert r.status_code == 308

    r = client.post('/login/', data=params)
    assert r.status_code == 200
    
    
   

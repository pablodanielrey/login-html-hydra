import requests
import pytest
import time
import uuid
import datetime
import logging
import sys


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
def prepare_environment(wait_for_api):
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

@pytest.fixture(scope='module')
def prepare_dbs(prepare_environment):
    """
        genera un usuario de testing dentro de las bases de datos.
    """

    """ agrego el path del sistema para poder instanciarlo """
    sys.path.append('../src/')

    from users.model.entities.User import User, Mail, MailTypes, IdentityNumber, IdentityNumberTypes
    from users.model.__main__ import create_tables as create_user_tables
    create_user_tables()

    from login.model.entities.Login import UserCredentials
    from login.model.__main__ import create_tables as create_login_tables
    create_login_tables()
    
    from login_html_hydra.models.db import open_users_session, open_login_session

    uid = str(uuid.uuid4())
    with open_users_session() as session:
        if not session.query(User).filter(User.firstname == 'name').one_or_none():
            u = User()
            u.id = uid
            u.firstname = 'name'
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
            m.confirmed = datetime.datetime.utcnow()
            m.email = 'testuser@econo.unlp.edu.ar'
            m.type = MailTypes.INSTITUTIONAL
            m.user_id = uid
            session.add(m)

            m = Mail()
            m.id = str(uuid.uuid4())
            m.confirmed = datetime.datetime.utcnow()
            m.email = 'testuser@alternative.com'
            m.type = MailTypes.ALTERNATIVE
            m.user_id = uid
            session.add(m)

            session.commit()

    with open_users_session() as session:
        session.query(User).filter(User.firstname == 'name').one()

    with open_login_session() as session:
        if not session.query(UserCredentials).filter(UserCredentials.username == 'username').one_or_none():
            uc = UserCredentials()
            uc.id = str(uuid.uuid4())
            uc.created = datetime.datetime.utcnow()
            uc.user_id = uid
            uc.username = 'username'
            uc.credentials = 'password'
            session.add(uc)
            session.commit()

    with open_login_session() as session:
        session.query(UserCredentials).filter(UserCredentials.username == 'username', UserCredentials.credentials == 'password').one()


@pytest.fixture(scope='module')
def hydra_model(prepare_dbs):
    from login_html_hydra.models.LoginHydraModel import LoginHydraModel
    model = LoginHydraModel()
    return model
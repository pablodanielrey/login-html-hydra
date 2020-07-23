import requests
import pytest
import time
import uuid
import datetime
import logging
import sys



def pytest_addoption(parser):
    group = parser.getgroup('environ')
    group.addoption(
        '--environ',
        action='store',
        dest='environ',
        default='dev',
        help='setea el environment a testear = dev | prod'
    )

@pytest.fixture(scope='module')
def config(request):
    e = request.config.option.environ

    sys.path.append('config')
    from config import UserConf, PassConf, valid_challenge, invalid_challenge

    if 'dev' == e:
        from config.config_dev import get_config
        return get_config()

    if 'prod' == e:
        from config.config_prod import get_config
        return get_config()

    raise Exception('debe seleccionar un environment')


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
def prepare_environment(request, wait_for_api):
    data = wait_for_api
   
    e = request.config.option.environ
    if 'prod' == e:

        """ 
            las variables de entorno ya vienen seteada con los datos de producción 
            solo modifico los puertos para manejar kubectl
        """ 
        import os
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5555'
        os.environ['USERS_DB_HOST'] = 'localhost'
        os.environ['USERS_DB_PORT'] = '5556'

        os.environ['HYDRA_ADMIN_URL'] = data['hydra_api_url']

    if 'dev' == e:

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
def prepare_dbs(request, config, prepare_environment):

    e = request.config.option.environ

    if 'prod' == e:
        """ no se hace nada. se supone que las bases ya estan configuradas """
        return


    if 'dev' == e:
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

        user_ok = config['user']
        creds_ok = config['credentials']
        uid = str(uuid.uuid4())

        with open_login_session() as session:
            """
            for c in session.query(UserCredentials).filter(UserCredentials.username == creds_ok.username):
                session.delete(c)
            session.commit()
            """

            if not session.query(UserCredentials).filter(UserCredentials.username == creds_ok.username).one_or_none():
                uc = UserCredentials()
                uc.id = str(uuid.uuid4())
                uc.created = datetime.datetime.utcnow()
                uc.user_id = uid
                uc.username = creds_ok.username
                uc.credentials = creds_ok.credentials
                session.add(uc)
                session.commit()

        with open_login_session() as session:
            uc = session.query(UserCredentials).filter(UserCredentials.username == creds_ok.username, UserCredentials.credentials == creds_ok.credentials).one()
            uid = uc.user_id

        with open_users_session() as session:
            """
            for u in session.query(User).filter(User.firstname == user_ok.firstname, User.lastname == user_ok.lastname).all():
                for i in u.identity_numbers:
                    session.delete(i)
                for m in u.mails:
                    session.delete(m)
                session.delete(u)
            session.commit()
            """

            if not session.query(User).filter(User.id == uid).one_or_none():
                u = User()
                u.id = uid
                u.firstname = user_ok.firstname
                u.lastname = user_ok.lastname
                session.add(u)

                i = IdentityNumber()
                i.id = str(uuid.uuid4())
                i.user_id = uid
                i.number = user_ok.dni
                i.type = IdentityNumberTypes.DNI
                session.add(i)

                m = Mail()
                m.id = str(uuid.uuid4())
                m.confirmed = datetime.datetime.utcnow()
                m.email = user_ok.imail
                m.type = MailTypes.INSTITUTIONAL
                m.user_id = uid
                session.add(m)

                m = Mail()
                m.id = str(uuid.uuid4())
                m.confirmed = datetime.datetime.utcnow()
                m.email = user_ok.email
                m.type = MailTypes.ALTERNATIVE
                m.user_id = uid
                session.add(m)

                session.commit()

        with open_users_session() as session:
            session.query(User).filter(User.id == uid, User.firstname == user_ok.firstname).one()


        """
            esto no funca hay que testearlo despues 


        logging.warn('----------------------------------------------------------------------')
        logging.warn('base configurada')
        logging.warn('----------------------------------------------------------------------')

        try:
            yield

        except Exception as e:
            logging.warn('----------------------------------------------------------------------')
            logging.warn('elminando entidades')
            logging.warn('----------------------------------------------------------------------')

            with open_login_session() as session:
                session.query(UserCredentials).filter(UserCredentials.username == 'username', UserCredentials.credentials == 'password').delete()
                session.commit()

            with open_users_session() as session:
                users = session.query(User).filter(User.firstname == 'username', User.lastname == 'lastname').all()
                for u in users:
                    for m in u.mails:
                        m.delete()
                    u.delete()
                session.commit()
        """


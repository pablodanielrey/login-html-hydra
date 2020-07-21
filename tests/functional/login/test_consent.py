import requests
import pytest
import time
import uuid
import datetime
import logging

pytest_plugins = ["docker_compose"]

@pytest.fixture(scope='module')
def wait_for_api(module_scoped_container_getter):
    """ espera hasta que los contendores estén levantados y se pueda conectar a la api correctamente """
    time.sleep(10)

    service = module_scoped_container_getter.get("hydra").network_info[0]
    hydra_api_url = f"http://{service.hostname}:{service.host_port}/"    

    data = {
        'hydra_api_url': hydra_api_url
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
    os.environ['USERS_DB_HOST'] = '0.0.0.0'
    os.environ['USERS_DB_PORT'] = '0.0.0.0'

    os.environ['DB_USER'] = 'login'
    os.environ['DB_PASSWORD'] = 'clavesuperultrarecontrasecreta'
    os.environ['DB_NAME'] = 'login'
    os.environ['DB_HOST'] = '0.0.0.0'
    os.environ['DB_PORT'] = '0.0.0.0'

    os.environ['HYDRA_ADMIN_URL'] = data['hydra_api_url']

    """ agrego el path del sistema para poder instanciarlo """
    import sys
    sys.path.append('../../src/')


def test_consent_ok():
    pass
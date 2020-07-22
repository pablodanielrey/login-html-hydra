import requests
import pytest
import time
import uuid
import datetime
import logging


pytest_plugins = ["docker_compose"]

STRING_DE_ERROR = 'Error de ingreso'

def test_login_url_redireccion(client):
    """ las redirecciones que hace automáticamente flask """
    r = client.get('/login', query_string={})
    assert r.status_code == 308
    r = client.get('/login', query_string={'param1':'value1'})
    assert r.status_code == 308
    r = client.post('/login')
    assert r.status_code == 308
    r = client.post('/login', data={'param1':'value1'})
    assert r.status_code == 308

"""
    get del formulario de login
"""

def test_null_login_get(client):
    r = client.get('/login/')
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_valid_login_get(client, config):
    challenge = config['challenge']
    query = {
        'login_challenge': challenge
    }
    r = client.get('/login/', query_string=query)
    assert r.status_code == 200
    assert challenge in str(r.data)

def test_invalid_login_get(client, config):
    challenge = config['invalid_challenge']
    query = {
        'login_challenge': challenge
    }
    r = client.get('/login/', query_string=query)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

"""
    post de los datos sin challenge
"""

def test_null_login_post(client):
    r = client.post('/login/')
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_null_login_err(client, config):
    creds = config['credentials_err']
    params = {
        'username': creds.username,
        'password': creds.credentials
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_null_login_ok(client, config):
    creds = config['credentials']
    params = {
        'username': creds.username,
        'password': creds.credentials
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)


"""
    post de los datos con challenge
"""

def test_valid_login_required_fail(client, config):
    challenge = config['challenge']
    creds = config['credentials']
    params = {
        'username': creds.username,
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert challenge in str(r.data)

def test_invalid_login_required_fail(client, config):
    challenge = config['invalid_challenge']
    creds = config['credentials']
    params = {
        'username': creds.username,
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert challenge in str(r.data)

def test_valid_login_err(client, config):
    challenge = config['challenge']
    params = {
        'username': config['credentials'].username,
        'password': config['credentials_err'].credentials,
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 302
    
def test_invalid_login_err(client, config):
    challenge = config['invalid_challenge']
    params = {
        'username': config['credentials'].username,
        'password': config['credentials_err'].credentials,
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_valid_login_ok(client, config):
    challenge = config['challenge']
    creds = config['credentials']
    params = {
        'username': creds.username,
        'password': creds.credentials,
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 302

def test_invalid_login_ok(client, config):
    challenge = config['invalid_challenge']
    creds = config['credentials']
    params = {
        'username': creds.username,
        'password': creds.credentials,
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)


    
    
   

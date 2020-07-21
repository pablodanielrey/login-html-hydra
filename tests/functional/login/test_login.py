import requests
import pytest
import time
import uuid
import datetime
import logging

#from . import VALID_CHALLENGE, INVALID_CHALLENGE

pytest_plugins = ["docker_compose"]


INVALID_CHALLENGE = 'invalidchallenge'
VALID_CHALLENGE = 'validchallenge'
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

def test_null_login_get(prepare_dbs, client):
    r = client.get('/login/')
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_valid_login_get(prepare_dbs, client):
    challenge = VALID_CHALLENGE
    query = {
        'login_challenge': challenge
    }
    r = client.get('/login/', query_string=query)
    assert r.status_code == 200
    assert challenge in str(r.data)

def test_invalid_login_get(prepare_dbs, client):
    challenge = INVALID_CHALLENGE
    query = {
        'login_challenge': challenge
    }
    r = client.get('/login/', query_string=query)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

"""
    post de los datos sin challenge
"""

def test_null_login_post(prepare_dbs, client):
    r = client.post('/login/')
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_null_login_err(prepare_dbs, client):
    params = {
        'username': 'username',
        'password': 'wrongpassword'
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_null_login_ok(prepare_dbs, client):
    params = {
        'username': 'username',
        'password': 'password'
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)


"""
    post de los datos con challenge
"""

def test_valid_login_required_fail(prepare_dbs, client):
    challenge = VALID_CHALLENGE
    params = {
        'username': 'username',
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert challenge in str(r.data)

def test_invalid_login_required_fail(prepare_dbs, client):
    challenge = INVALID_CHALLENGE
    params = {
        'username': 'username',
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert challenge in str(r.data)

def test_valid_login_err(prepare_dbs, client):
    challenge = VALID_CHALLENGE
    params = {
        'username': 'username',
        'password': 'wrongpassword',
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 302
    
def test_invalid_login_err(prepare_dbs, client):
    challenge = INVALID_CHALLENGE
    params = {
        'username': 'username',
        'password': 'wrongpassword',
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_valid_login_ok(prepare_dbs, client):
    challenge = VALID_CHALLENGE
    params = {
        'username': 'username',
        'password': 'password',
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 302

def test_invalid_login_ok(prepare_dbs, client):
    challenge = INVALID_CHALLENGE
    params = {
        'username': 'username',
        'password': 'password',
        'challenge': challenge
    }
    r = client.post('/login/', data=params)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)


    
    
   

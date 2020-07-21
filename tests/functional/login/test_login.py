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
    assert "Error de ingreso" in str(r.data)

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
    assert "Error de ingreso" in str(r.data)

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
    assert "Error de ingreso" in str(r.data)


    
    
   

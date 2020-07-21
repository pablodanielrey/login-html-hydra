import requests
import pytest
import time
import uuid
import datetime
import logging

#from . import INVALID_CHALLENGE, VALID_CHALLENGE

pytest_plugins = ["docker_compose"]

INVALID_CHALLENGE = 'invalidchallenge'
VALID_CHALLENGE = 'validchallenge'
STRING_DE_ERROR = 'Error de ingreso'


def test_valid_consent_ok(client):
    challenge = VALID_CHALLENGE
    query = {
        'consent_challenge': challenge
    }
    r = client.get('/consent/', query_string=query)
    assert r.status_code == 302

def test_invalid_consent(client):
    challenge = INVALID_CHALLENGE
    query = {
        'consent_challenge': challenge
    }
    r = client.get('/consent/', query_string=query)
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)

def test_null_consent(client):
    r = client.get('/consent/')
    assert r.status_code == 400
    assert STRING_DE_ERROR in str(r.data)
import pytest
import uuid

INVALID_CHALLENGE = 'invalidchallenge'
VALID_CHALLENGE = 'validchallenge'

USERNAME_OK = 'username'
PASSWORD_OK = 'password'
USERNAME_WRONG = 'u'
PASSWORD_WRONG = 'p'


"""
    otbenr los challenges de login
"""

def test_null_get_login_challenge(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.get_login_challenge(None)

def test_invalid_get_login_challenge(hydra_model, config_err):
    model = hydra_model
    challenge = config_err['challenge']
    with pytest.raises(Exception):
        model.get_login_challenge(challenge)
    
def test_valid_get_login_challenge(hydra_model, config_ok):
    model = hydra_model
    challenge = config_ok['challenge']
    data = model.get_login_challenge(challenge)
    assert data['skip'] is not None
    assert data['challenge'] is not None


"""
    aceptación de los challenge de login
"""

def test_null_accept_login_challenge(hydra_model, config_ok, config_err):
    model = hydra_model
    with pytest.raises(Exception):
        model.accept_login_challenge(None, None)
    with pytest.raises(Exception):
        model.accept_login_challenge(None, str(uuid.uuid4()))
    with pytest.raises(Exception):
        model.accept_login_challenge(config_ok['challenge'], None)
    with pytest.raises(Exception):
        model.accept_login_challenge(config_err['challenge'], None)

def test_invalid_accept_login_challenge(hydra_model, config_err):
    model = hydra_model
    challenge = config_err['challenge']
    with pytest.raises(Exception):
        model.accept_login_challenge(challenge, str(uuid.uuid4()))
    
def test_valid_accept_login_challenge(hydra_model, config_ok):
    model = hydra_model
    challenge = config_ok['challenge']
    r = model.accept_login_challenge(challenge, str(uuid.uuid4()))
    assert r.startswith('http')


"""
    login de un usuario
"""


def test_login_null_params(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.login(None, None, None)

def test_login_valid_ok(hydra_model, config_ok):
    model = hydra_model
    challenge = config_ok['challenge']
    creds = config_ok['credentials']
    r = model.login(challenge, creds.username, creds.credentials)
    assert r.startswith('http')

def test_login_valid_worng_user(hydra_model, config_ok, config_err):
    model = hydra_model
    challenge = config_ok['challenge']
    creds_ok = config_ok['credentials']
    creds_err = config_err['credentials']
    r = model.login(challenge, creds_err.username, creds_ok.credentials)
    assert r.startswith('http')

def test_login_valid_wrong_password(hydra_model, config_ok, config_err):
    model = hydra_model
    challenge = config_ok['challenge']
    creds_ok = config_ok['credentials']
    creds_err = config_err['credentials']
    r = model.login(challenge, creds_ok.username, creds_err.credentials)
    assert r.startswith('http')

def test_login_invalid_ok(hydra_model, config_ok, config_err):
    model = hydra_model
    challenge = config_err['challenge']
    creds_ok = config_ok['credentials']
    with pytest.raises(Exception):
        r = model.login(challenge, creds_ok.username, creds_ok.credentials)
    
def test_login_invalid_worng_user(hydra_model, config_ok, config_err):
    model = hydra_model
    challenge = config_err['challenge']
    creds_ok = config_ok['credentials']
    creds_err = config_err['credentials']
    with pytest.raises(Exception):
        r = model.login(challenge, creds_err.username, creds_ok.credentials)

def test_login_invalid_wrong_password(hydra_model, config_ok, config_err):
    model = hydra_model
    challenge = config_err['challenge']
    creds_ok = config_ok['credentials']
    creds_err = config_err['credentials']
    with pytest.raises(Exception):
        r = model.login(challenge, creds_ok.username, creds_err.credentials)


"""
    challenges de consent
"""

def test_null_check_and_accept_consent(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.check_and_accept_consent_challenge(None)

def test_check_and_accept_valid_consent(hydra_model, config_ok):
    model = hydra_model
    challenge = config_ok['challenge']
    r = model.check_and_accept_consent_challenge(challenge)
    assert r.startswith('http')

def test_check_and_accept_invalid_consent(hydra_model, config_err):
    model = hydra_model
    challenge = config_err['challenge']
    with pytest.raises(Exception):
        model.check_and_accept_consent_challenge(challenge)

    
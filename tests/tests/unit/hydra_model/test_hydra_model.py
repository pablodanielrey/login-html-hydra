import pytest
import uuid


"""
    otbenr los challenges de login
"""

def test_null_get_login_challenge(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.get_login_challenge(None)

def test_invalid_get_login_challenge(hydra_model, config):
    model = hydra_model
    challenge = config['invalid_challenge']
    with pytest.raises(Exception):
        model.get_login_challenge(challenge)
    
def test_valid_get_login_challenge(hydra_model, config):
    model = hydra_model
    challenge = config['challenge']
    data = model.get_login_challenge(challenge)
    assert data['skip'] is not None
    assert data['challenge'] is not None


"""
    aceptación de los challenge de login
"""

def test_null_accept_login_challenge(hydra_model, config):
    model = hydra_model
    with pytest.raises(Exception):
        model.accept_login_challenge(None, None)
    with pytest.raises(Exception):
        model.accept_login_challenge(None, str(uuid.uuid4()))
    with pytest.raises(Exception):
        model.accept_login_challenge(config['challenge'], None)
    with pytest.raises(Exception):
        model.accept_login_challenge(config['invalid_challenge'], None)

def test_invalid_accept_login_challenge(hydra_model, config):
    model = hydra_model
    challenge = config['invalid_challenge']
    with pytest.raises(Exception):
        model.accept_login_challenge(challenge, str(uuid.uuid4()))
    
def test_valid_accept_login_challenge(hydra_model, config):
    model = hydra_model
    challenge = config['challenge']
    r = model.accept_login_challenge(challenge, str(uuid.uuid4()))
    assert r.startswith('http')


"""
    login de un usuario
"""


def test_login_null_params(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.login(None, None, None)

def test_login_valid_ok(hydra_model, config):
    model = hydra_model
    challenge = config['challenge']
    creds = config['credentials']
    r = model.login(challenge, creds.username, creds.credentials)
    assert r.startswith('http')
    assert 'error' not in r

def test_login_valid_worng_user(hydra_model, config):
    model = hydra_model
    challenge = config['challenge']
    creds_ok = config['credentials']
    creds_err = config['credentials_err']
    r = model.login(challenge, creds_err.username, creds_ok.credentials)
    assert r.startswith('http')
    assert 'error' in r

def test_login_valid_wrong_password(hydra_model, config):
    model = hydra_model
    challenge = config['challenge']
    creds_ok = config['credentials']
    creds_err = config['credentials_err']
    r = model.login(challenge, creds_ok.username, creds_err.credentials)
    assert r.startswith('http')

def test_login_invalid_ok(hydra_model, config):
    model = hydra_model
    challenge = config['invalid_challenge']
    creds_ok = config['credentials']
    with pytest.raises(Exception):
        r = model.login(challenge, creds_ok.username, creds_ok.credentials)
    
def test_login_invalid_worng_user(hydra_model, config):
    model = hydra_model
    challenge = config['invalid_challenge']
    creds_ok = config['credentials']
    creds_err = config['credentials_err']
    with pytest.raises(Exception):
        r = model.login(challenge, creds_err.username, creds_ok.credentials)

def test_login_invalid_wrong_password(hydra_model, config):
    model = hydra_model
    challenge = config['invalid_challenge']
    creds_ok = config['credentials']
    creds_err = config['credentials_err']
    with pytest.raises(Exception):
        r = model.login(challenge, creds_ok.username, creds_err.credentials)


"""
    challenges de consent
"""

def test_null_check_and_accept_consent(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.check_and_accept_consent_challenge(None)

def test_check_and_accept_valid_consent(hydra_model, config):
    model = hydra_model
    challenge = config['challenge']
    r = model.check_and_accept_consent_challenge(challenge)
    assert r.startswith('http')

def test_check_and_accept_invalid_consent(hydra_model, config):
    model = hydra_model
    challenge = config['invalid_challenge']
    with pytest.raises(Exception):
        model.check_and_accept_consent_challenge(challenge)

    
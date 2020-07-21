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

def test_invalid_get_login_challenge(hydra_model):
    model = hydra_model
    challenge = INVALID_CHALLENGE
    with pytest.raises(Exception):
        model.get_login_challenge(challenge)
    
def test_valid_get_login_challenge(hydra_model):
    model = hydra_model
    challenge = VALID_CHALLENGE
    data = model.get_login_challenge(challenge)
    assert data['skip'] is not None
    assert data['challenge'] is not None


"""
    aceptación de los challenge de login
"""

def test_null_accept_login_challenge(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.accept_login_challenge(None, None)
    with pytest.raises(Exception):
        model.accept_login_challenge(None, str(uuid.uuid4()))
    with pytest.raises(Exception):
        model.accept_login_challenge(VALID_CHALLENGE, None)
    with pytest.raises(Exception):
        model.accept_login_challenge(INVALID_CHALLENGE, None)

def test_invalid_accept_login_challenge(hydra_model):
    model = hydra_model
    challenge = INVALID_CHALLENGE
    with pytest.raises(Exception):
        model.accept_login_challenge(challenge, str(uuid.uuid4()))
    
def test_valid_accept_login_challenge(hydra_model):
    model = hydra_model
    challenge = VALID_CHALLENGE
    r = model.accept_login_challenge(challenge, str(uuid.uuid4()))
    assert r.startswith('http')


"""
    login de un usuario
"""


def test_login_null_params(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.login(None, None, None)

def test_login_valid_ok(hydra_model):
    model = hydra_model
    challenge = VALID_CHALLENGE
    r = model.login(challenge, USERNAME_OK, PASSWORD_OK)
    assert r.startswith('http')

def test_login_valid_worng_user(hydra_model):
    model = hydra_model
    challenge = VALID_CHALLENGE
    r = model.login(challenge, USERNAME_WRONG, PASSWORD_OK)
    assert r.startswith('http')

def test_login_valid_wrong_password(hydra_model):
    model = hydra_model
    challenge = VALID_CHALLENGE
    r = model.login(challenge, USERNAME_OK, PASSWORD_WRONG)
    assert r.startswith('http')

def test_login_invalid_ok(hydra_model):
    model = hydra_model
    challenge = INVALID_CHALLENGE
    with pytest.raises(Exception):
        r = model.login(challenge, USERNAME_OK, PASSWORD_OK)
    
def test_login_invalid_worng_user(hydra_model):
    model = hydra_model
    challenge = INVALID_CHALLENGE
    with pytest.raises(Exception):
        r = model.login(challenge, USERNAME_WRONG, PASSWORD_OK)

def test_login_invalid_wrong_password(hydra_model):
    model = hydra_model
    challenge = INVALID_CHALLENGE
    with pytest.raises(Exception):
        r = model.login(challenge, USERNAME_OK, PASSWORD_WRONG)


"""
    challenges de consent
"""

def test_null_check_and_accept_consent(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.check_and_accept_consent_challenge(None)

def test_check_and_accept_valid_consent(hydra_model):
    model = hydra_model
    r = model.check_and_accept_consent_challenge(VALID_CHALLENGE)
    assert r.startswith('http')

def test_check_and_accept_invalid_consent(hydra_model):
    model = hydra_model
    with pytest.raises(Exception):
        model.check_and_accept_consent_challenge(INVALID_CHALLENGE)

    
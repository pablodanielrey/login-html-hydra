import pytest

@pytest.fixture(scope='module')
def change_credentials_model(prepare_dbs):
    from login_html_hydra.models.ChangeCredentialsModel import ChangeCredentialsModel
    model = ChangeCredentialsModel()
    return model


@pytest.fixture(scope='module')
def reset_config():
    return {
        'uid': 'uidtest',
        'username': 'usernametest',
        'return_url': 'return_urltest'
    }

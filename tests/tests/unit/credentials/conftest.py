import pytest


@pytest.fixture(scope='module')
def gmail_api():
    return None

@pytest.fixture(scope='module')
def google_api():
    return None

@pytest.fixture(scope='module')
def mails_model(gmail_api):
    from login_html_hydra.models.MailsModel import MailsModel
    model = MailsModel(gmail_api)
    return model

@pytest.fixture(scope='module')
def google_sync_model(google_api):
    from login_html_hydra.models.google.GoogleSyncModel import GoogleSyncModel
    model = GoogleSyncModel(google_api)
    return model

@pytest.fixture(scope='module')
def credentials_model(prepare_dbs, mails_model, google_sync_model):
    from login_html_hydra.models.ResetCredentialsModel import ResetCredentialsModel
    model = ResetCredentialsModel(mails_model, google_sync_model)
    return model

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
        'return_url': 'return_urltest',
        'min_len': 5
    }

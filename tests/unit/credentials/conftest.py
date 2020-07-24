import pytest

@pytest.fixture(scope='module')
def credentials_model(prepare_dbs):
    from login_html_hydra.models.CredentialsModel import CredentialsModel
    model = CredentialsModel()
    return model
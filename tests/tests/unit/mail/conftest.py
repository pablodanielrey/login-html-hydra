import pytest


@pytest.fixture(scope='module')
def gmail_api():
    from login_html_hydra.models.MailsModel import _get_api
    return _get_api('sistemas@econo.unlp.edu.ar')

@pytest.fixture(scope='module')
def mails_model(gmail_api):
    from login_html_hydra.models.MailsModel import MailsModel
    model = MailsModel(gmail_api)
    return model

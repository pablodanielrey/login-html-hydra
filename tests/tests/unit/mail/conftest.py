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

@pytest.fixture(scope='module')
def generate_data():
    return {
        'code': 'ABcDeF5',
        'tos': ['miguel.macagno@gmail.com','miguel.macagno@econo.unlp.edu.ar'],
        'user': User()
    }


class User:
    firstname = 'TestName'
    lastname = 'TestLastname'

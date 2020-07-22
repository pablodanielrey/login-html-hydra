import pytest

@pytest.fixture(scope='module')
def client(prepare_dbs, prepare_environment):
    from login_html_hydra.web.app import webapp
    webapp.config['TESTING'] = True
    webapp.config['WTF_CSRF_CHECK_DEFAULT'] = False
    webapp.config['WTF_CSRF_ENABLED'] = False
    with webapp.test_client() as client:
        client
        with webapp.app_context():
            yield client

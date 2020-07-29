import uuid

def test_change_credentials_get(client):
    r = client.get('/change_credentials/')
    assert r.status_code == 200
    assert 'formulario' in str(r.data)
    assert 'password2' in str(r.data)
    assert 'password2_confirmation' in str(r.data)


def test_null_change_credentials_post(client):
    code = str(uuid.uuid4())
    r = client.post(f'/change_credentials/{code}')
    assert r.status_code == 400
    assert 'faltan datos requeridos' in str(r.data)

def test_valid_change_credentials_post(client):
    code = str(uuid.uuid4())
    params = {
        'password2': 'unapass',
        'password2_confirmation': 'unapass'
    }
    r = client.post(f'/change_credentials/{code}', data=params)
    assert r.status_code == 302
 
def test_invalid_change_credentials_post(client):
    code = str(uuid.uuid4())
    params = {
        'password2': 'unapass',
        'password2_confirmation': 'otrapass'
    }
    r = client.post(f'/change_credentials/{code}', data=params)
    assert r.status_code == 400
    assert 'verifique las claves' in str(r.data)

#def test_ok_username_post(config, client):
#    params = {
#        'username': config['credentials'].username
#    }
#    r = client.post('/reset_credentials/username', data=params)
#    assert r.status_code == 302


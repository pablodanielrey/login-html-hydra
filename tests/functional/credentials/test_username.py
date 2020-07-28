

def test_get_username(client):
    r = client.get('/reset_credentials/username')
    assert r.status_code == 200
    assert 'Ingrese su DNI' in str(r.data)
    assert 'formulario' in str(r.data)


def test_null_username_post(client):
    r = client.post('/reset_credentials/username')
    assert r.status_code == 400
    assert 'formulario' in str(r.data)
 
def test_ok_username_post(config, client):
    params = {
        'username': config['credentials'].username
    }
    r = client.post('/reset_credentials/username', data=params)
    assert r.status_code == 302


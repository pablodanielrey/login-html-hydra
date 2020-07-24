import pytest

def test_generate_null_user_reset_info(credentials_model):
    model = credentials_model
    with pytest.raises(Exception):
        ri = model.generate_reset_info(None)

def test_generate_invalid_user_reset_info(config, credentials_model):
    username = config['credentials_err'].username
    model = credentials_model
    with pytest.raises(Exception):
        ri = model.generate_reset_info(username)

def test_generate_valid_user_reset_info(config, credentials_model):
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)
    assert ri is not None
    assert ri['id'] is not None
    assert ri['username'] == username
    assert ri['uid'] is not None
    assert ri['code'] is not None and type(ri['code']) == str and len(ri['code']) == 5
    assert type(ri['mails']) == list and len(ri['mails']) >= 1

def test_generate_valid_user_reset_info_cache(config, credentials_model):
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)
    ro = model.generate_reset_info(username)
    assert ri['id'] == ro['id']
    assert ri['code'] == ro['code']

def test_get_reset_info_from_null_id(credentials_model):
    model = credentials_model
    with pytest.raises(Exception):
        ro = model.get_reset_info(None)

def test_get_reset_info_from_id(config, credentials_model):
    """ genero la info de reset """
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)

    """ obtengo esa misma info mediante el id """
    rid = ri['id']
    ro = model.get_reset_info(rid)
    assert ri['code'] == ro['code']
    assert ri['username'] == ro['username']
    assert ri['uid'] == ro['uid']

    reset_code = ri['reset_code']
    ro = model.get_indirect_reset_info(reset_code)
    assert ri['code'] == ro['code']
    assert ri['username'] == ro['username']
    assert ri['uid'] == ro['uid']


def test_verify_valid_code(config, credentials_model):
    username = config['credentials'].username

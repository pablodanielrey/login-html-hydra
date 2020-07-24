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
    assert type(ri['mails']) == list and len(ri['mails']) == 1

def test_generate_valid_user_reset_info_cache(config, credentials_model):
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)
    ro = model.generate_reset_info(username)
    assert ri['id'] == ro['id']
    assert ri['code'] == ro['code']
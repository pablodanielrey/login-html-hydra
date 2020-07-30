import pytest
import uuid

def test_generate_null_user_reset_info(credentials_model):
    model = credentials_model
    with pytest.raises(Exception):
        ri = model.generate_reset_info(None)

def test_generate_invalid_user_reset_info(config, credentials_model):
    username = config['credentials_err'].username
    model = credentials_model
    with pytest.raises(Exception):
        ri = model.generate_reset_info(username)

    username = str(uuid.uuid4())
    if config['credentials'].username != username:
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

    """ analizo los indices generados """
    reset_code = ri['reset_code']
    cid = ri['id']
    code = ri['code']
    ro = model.get_indexed_reset_info(reset_code)
    assert code == ro['code']
    assert reset_code == ro['reset_code']
    assert cid == ro['id']
    assert ri['uid'] == ro['uid']
    assert ri['username'] == ro['username']

    ro = model.get_indexed_reset_info(username)
    assert code == ro['code']
    assert reset_code == ro['reset_code']
    assert cid == ro['id']
    assert ri['uid'] == ro['uid']
    assert ri['username'] == ro['username']
 

def test_null_get_indexed_reset_info(credentials_model):
    model = credentials_model
    with pytest.raises(Exception):
        r = model.get_indexed_reset_info(None)


def test_generate_valid_user_reset_info_cache(config, credentials_model):
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)
    ro = model.generate_reset_info(username)
    assert ri['id'] == ro['id']
    assert ri['code'] == ro['code']
    assert ri['reset_code'] == ro['reset_code']
    assert ri['uid'] == ro['uid']
    assert ri['username'] == ro['username']

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
    ro = model.get_indexed_reset_info(reset_code)
    assert ri['code'] == ro['code']
    assert ri['username'] == ro['username']
    assert ri['uid'] == ro['uid']


"""
    paso 2 - código
"""

def test_null_verify_code(config, credentials_model):
    model = credentials_model

    with pytest.raises(Exception):
        rc = model.verify_code(None, None)

    random_cid = str(uuid.uuid4())
    with pytest.raises(Exception):
        rc = model.verify_code(random_cid, None)

    random_code = str(uuid.uuid4())
    with pytest.raises(Exception):
        rc = model.verify_code(None, random_code)

    correct_len_code = random_code[:5]
    with pytest.raises(Exception):
        rc = model.verify_code(None, correct_len_code)


    username = config['credentials'].username
    ri = model.generate_reset_info(username)
    reset_code = ri['reset_code']
    cid = ri['id']
    code = ri['code']

    with pytest.raises(Exception):
        rc = model.verify_code(cid, None)

    with pytest.raises(Exception):
        rc = model.verify_code(cid, random_code)

    with pytest.raises(Exception):
        rc = model.verify_code(cid, correct_len_code)

    with pytest.raises(Exception):
        rc = model.verify_code(random_cid, code)

    with pytest.raises(Exception):
        rc = model.verify_code(None, code)


def test_verify_valid_code(config, credentials_model):
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)

    reset_code = ri['reset_code']
    cid = ri['id']
    code = ri['code']
    rc = model.verify_code(cid, code)
    assert rc == reset_code

    ro = model.get_indexed_reset_info(rc)
    assert ro['username'] == ri['username']
    assert ro['uid'] == ri['uid']
 
def test_verify_invalid_code(config, credentials_model):
    username = config['credentials'].username
    model = credentials_model
    ri = model.generate_reset_info(username)

    reset_code = ri['reset_code']
    cid = ri['id']
    code = ri['code']
    invalid_code = code[::-1]

    with pytest.raises(Exception):
        rc = model.verify_code(cid, invalid_code)

    if reset_code != code:
        with pytest.raises(Exception):
            model.verify_code(cid, reset_code)


"""
    paso 3 - reset credentials
""" 


import pytest

def test_get_uid_by_identity_number(config, credentials_model):

    dni = config['user'].dni

    model = credentials_model
    user = model._get_uid_by_identity_number(dni)
    assert user is not None

    user = model._get_uid_by_identity_number(None)
    assert user is None

    user = model._get_uid_by_identity_number(f"n{dni}a{dni}")
    assert user is None

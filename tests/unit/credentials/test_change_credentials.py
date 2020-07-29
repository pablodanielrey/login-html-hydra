import uuid
import pytest

def test_null_change_credentials(reset_config, change_credentials_model):
    model = change_credentials_model

    with pytest.raises(Exception):
        retorno = model.change_credentials(None, 'asdasds') 

    config = reset_config
    code = model._generate_credentials(config)
    password = config['new_password']

    with pytest.raises(Exception):
        retorno = model.change_credentials(code, None)


def test_invalid_credentials(reset_config, change_credentials_model):
    model = change_credentials_model

    config = reset_config
    code = model._generate_credentials(config)
    password = config['new_password']

    with pytest.raises(Exception):
        retorno = model.change_credentials(code, ' ')


def test_change_credentials(reset_config, change_credentials_model):
    model = change_credentials_model
    config = reset_config

    code = model._generate_credentials(config)
    password = config['new_password']
    
    retorno = model.change_credentials(code, password)



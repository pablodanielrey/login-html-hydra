import requests
import pytest
import time
import uuid
import datetime
import logging
import sys

@pytest.fixture(scope='module')
def hydra_model(prepare_dbs):
    from login_html_hydra.models.LoginHydraModel import LoginHydraModel
    model = LoginHydraModel()
    return model
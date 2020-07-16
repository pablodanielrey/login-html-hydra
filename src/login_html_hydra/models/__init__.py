import os

from login.model.LoginModel import LoginModel
from users.model.UsersModel import UsersModel

HYDRA_ADMIN_URL = os.environ.get('HYDRA_ADMIN_URL')
VERIFY_HTTPS = bool(int(os.environ.get('VERIFY_HTTPS',0)))

from .LoginHydraModel import LoginHydraModel
from .HydraModel import HydraModel

hydraModel = HydraModel(HYDRA_ADMIN_URL, VERIFY_HTTPS)
loginModel = LoginModel()
usersModel = UsersModel()
loginHydraModel = LoginHydraModel()

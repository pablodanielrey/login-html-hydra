from login.model.LoginModel import LoginModel
from users.model.UsersModel import UsersModel

from .HydraApi import HydraApi

from login_html_hydra.config import HydraEnv

hydraApi = HydraApi(HydraEnv.HYDRA_ADMIN_URL, HydraEnv.VERIFY_HTTPS)
loginModel = LoginModel()
usersModel = UsersModel()


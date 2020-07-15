from login_html_hydra import config as config

from flask import Blueprint
bp = Blueprint('login', __name__, template_folder='templates')

from . import routes
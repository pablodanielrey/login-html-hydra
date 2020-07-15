from flask import render_template, flash, redirect,request, Markup, url_for
from .bp import bp
from . import config

from login_html_hydra import config

@bp.route('/')
def index():
    """
    Pagina de login
    """
    return render_template('index.html', version=config.version)
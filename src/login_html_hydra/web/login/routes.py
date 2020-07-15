import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from .forms import LoginForm

@bp.route('/', methods=['GET'])
def login():
    """
    Pagina de login
    """
    form = LoginForm()
    return render_template('login.html', form=form, version=config.version)

@bp.route('/', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        logging.info(f'ingreso {form.username.data} {form.password.data}')
    else:
        logging.info(f'error en submit')
    return render_template('login.html', form=form, version=config.version)

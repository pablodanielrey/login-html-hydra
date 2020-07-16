import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for, request
from . import bp, config

from .forms import LoginForm

from login_html_hydra.models import loginHydraModel

@bp.route('/', methods=['GET'])
def login():
    """
        paso 1
        Ruta solicitada por hydra cuando se inicia un requerimiento de login
        login_challenge va como parámetro query.
        https://www.ory.sh/hydra/docs/reference/api/#get-a-login-request
    """
    challenge = request.args.get('login_challenge')
    valid, skip, redirect_url = loginHydraModel.check_login_challenge(challenge)
    if valid:
        if skip:
            """ el codigo que esta en hydra-api esta mal para este caso """
            redirect_url = loginHydraModel.accept_login_challenge(challenge)
            return redirect(redirect_url)
        else:
            form = LoginForm()
            form.challenge.data = challenge
            return render_template('login.html', form=form, version=config.version)
    else:
        return render_template('error.html', error='Error de ingreso', version=config.version)

@bp.route('/', methods=['POST'])
def login_post():
    """
        paso 2
    """
    form = LoginForm()
    if form.validate_on_submit():
        logging.info(f'ingreso {form.username.data} {form.password.data}')
        challenge = form.challenge.data
        username = form.username.data
        password = form.password.data
        ok, redirect_url = loginHydraModel.login(challenge, username, password)
        if not ok:
            return render_template('error.html', error='Error de ingreso', version=config.version)
        else:
            return redirect(redirect_url)

    else:
        logging.info(f'error en submit')
    return render_template('login.html', form=form, version=config.version)

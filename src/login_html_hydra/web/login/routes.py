import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for, request
from . import bp, config

from .forms import LoginForm

from login_html_hydra.models.LoginHydraModel import loginHydraModel

@bp.route('/', methods=['GET'])
def login():
    """
        paso 1
        Ruta solicitada por hydra cuando se inicia un requerimiento de login
        login_challenge va como parámetro query.
        https://www.ory.sh/hydra/docs/reference/api/#get-a-login-request
    """
    try:
        challenge = request.args.get('login_challenge')
        data = loginHydraModel.get_login_challenge(challenge)
        skip = data['skip']
        if skip:
            uid = data['sub']
            redirect_url = loginHydraModel.accept_login_challenge(challenge, uid)
            return redirect(redirect_url), 302
        else:
            form = LoginForm()
            form.challenge.data = challenge
            return render_template('login.html', form=form, version=config.version), 200

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de ingreso', version=config.version), 400

@bp.route('/', methods=['POST'])
def login_post():
    """
        paso 2
    """
    try:
        form = LoginForm()
        if form.validate_on_submit():
            logging.info(f'ingreso {form.username.data} {form.password.data}')
            challenge = form.challenge.data
            username = form.username.data
            password = form.password.data
            redirect_url = loginHydraModel.login(challenge, username, password)
            assert redirect_url is not None
            return redirect(redirect_url), 302
        else:
            logging.warn('error en formulario')
            return render_template('login.html', form=form, version=config.version), 400

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de ingreso', version=config.version), 400

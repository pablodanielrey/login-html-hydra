import logging
import inject

from login_html_hydra.models.LoginHydraModel import LoginHydraModel

from flask import render_template, flash, request, Markup, url_for, request, Response
from . import bp, config

from .forms import LoginForm

loginHydraModel = inject.instance(LoginHydraModel)

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
            return render_template('redirect.html', url=redirect_url,version=config.version)
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
            return render_template('redirect.html', url=redirect_url,version=config.version)
        else:
            logging.warn('error en formulario')
            challenge = form.challenge.data
            if not challenge:
                return render_template('error.html', error='Error de ingreso', version=config.version), 400
            return render_template('login.html', form=form, version=config.version), 400

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de ingreso', version=config.version), 400

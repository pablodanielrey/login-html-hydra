import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from .forms import ChangeCredentialsForm

@bp.route('/', methods=['GET'])
def change_credentials_get():
    form = ChangeCredentialsForm()
    return render_template('change_credentials.html', form=form, version=config.version), 200

@bp.route('/', methods=['POST'])
def change_credentials_post():
    form = ChangeCredentialsForm()
    if form.validate_on_submit():
        p1 = form.password2.data
        p2 = form.password2_confirmation.data
        if p1 == p2:
            logging.info(f'claves {p1} {p2}')
            return render_template('change_credentials_ok.html', version=config.version), 200
        else:
            logging.info(f'claves inválidas')
            return render_template('change_credentials_error.html', error='verifique las claves', version=config.version), 400
    else:
        return render_template('change_credentials_error.html', error='faltan datos requeridos', version=config.version), 400


"""
    solo para walter para poder estilar las pantallas.
"""


@bp.route('/error', methods=['GET'])
def error_get():
    return render_template('change_credentials_error.html', version=config.version)

@bp.route('/success', methods=['GET'])
def success_get():
    return render_template('change_credentials_ok.html', version=config.version)
import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from .forms import ChangeCredentialsForm

@bp.route('/', methods=['GET'])
def change_credentials_get():
    form = ChangeCredentialsForm()
    return render_template('change_credentials.html', form=form, version=config.version)

@bp.route('/', methods=['POST'])
def change_credentials_post():
    form = ChangeCredentialsForm()
    if form.validate_on_submit():
        p1 = form.password2.data
        p2 = form.password2_confirmation.data
        if p1 == p2:
            logging.info(f'claves {form.password.data} {form.password2.data}')
            return render_template('change_credentials_ok.html', version=config.version)
        else:
            logging.info(f'claves inválidas')
            return render_template('change_credentials_error.html', error='verifique las claves', version=config.version)
    else:
        return render_template('change_credentials_error.html', error='faltan datos requeridos', version=config.version)
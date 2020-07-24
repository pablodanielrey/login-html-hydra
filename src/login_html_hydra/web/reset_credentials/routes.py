import logging

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from .forms import InputUsername, InputCode, InputCredentials

from login_html_hydra.models.CredentialsModel import credentialsModel




"""
    paso 1 -- ingresa su usuario
"""

@bp.route('/username', methods=['GET'])
def input_username():
    form = InputUsername()
    return render_template('input_username.html', form=form, version=config.version)

@bp.route('/username', methods=['POST'])
def input_username_post():
    try:
        form = InputUsername()
        if form.validate_on_submit():
            logging.info(f'reseteo de clave usando {form.username.data}')
            username = form.username.data
            ri = credentialsModel.generate_reset_info(username)
            return redirect(url_for(input_code, rid=ri['id'])), 302
        else:
            logging.warn('error en formulario')
            return render_template('input_username.html', form=form, version=config.version), 400

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400



"""
    paso 2 - ingresa el código enviado al correo
"""

@bp.route('/code', methods=['GET'])
def input_code():
    form = InputCode()
    return render_template('input_code.html', form=form, version=config.version)

@bp.route('/code', methods=['POST'])
def input_code_post():
    form = InputCode()
    return redirect(url_for(input_credentials))


"""
    paso 3 - ingresa las credenciales nuevas
"""

@bp.route('/credentials', methods=['GET'])
def input_credentials():
    form = InputCredentials()
    return render_template('input_credentials.html', form=form, version=config.version)

@bp.route('/credentials', methods=['POST'])
def input_credentials_post():
    form = InputCredentials()
    return redirect(url_for(success))




@bp.route('/error', methods=['GET'])
def error():
    error = 'se ha producido un error enviadno el código'
    return render_template('error.html', error=error, version=config.version)


@bp.route('/success', methods=['GET'])
def success():
    return render_template('success.html', version=config.version)





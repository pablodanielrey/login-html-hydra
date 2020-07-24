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
            return redirect(url_for('reset_credentials.input_code', cid=ri['id'])), 302
        else:
            logging.warn('error en formulario')
            return render_template('input_username.html', form=form, version=config.version), 400

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400



"""
    paso 2 - ingresa el código enviado al correo
"""

@bp.route('/code/<cid>', methods=['GET'])
def input_code(cid):
    try:
        ri = credentialsModel.get_reset_info(cid)
        emails = ri['mails']

        form = InputCode()
        form.cid.data = cid
        return render_template('input_code.html', form=form, emails=emails, version=config.version)

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400    

@bp.route('/code', methods=['POST'])
def input_code_post():
    try:
        form = InputCode()
        if form.validate_on_submit():
            logging.info(f'reseteo de clave {form.code.data} {form.cid.data}')
            cid = form.cid.data
            code = form.code.data
            reset_code = credentialsModel.verify_code(cid, code)
            return redirect(url_for('reset_credentials.input_credentials', code=reset_code)), 302
        else:
            if not form.cid.data:
                raise Exception('error en reseteo')

            cid = form.cid.data
            ri = credentialsModel.get_reset_info(cid)
            emails = ri['mails']
            return render_template('input_code.html', form=form, emails=emails, version=config.version)

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400


"""
    paso 3 - ingresa las credenciales nuevas
"""

@bp.route('/credentials/<code>', methods=['GET'])
def input_credentials(code):
    form = InputCredentials()
    form.cid.data = code
    return render_template('input_credentials.html', form=form, version=config.version)

@bp.route('/credentials', methods=['POST'])
def input_credentials_post():
    try:
        form = InputCredentials()
        if form.validate_on_submit():
            logging.info(f'reseteo de clave {form.cid.data}')
            cid = form.cid.data
            password = form.password.data
            password2 = form.password2.data
            if password != password2:
                return render_template('input_credentials.html', form=form, version=config.version)
            credentialsModel.reset_credentials(cid, password)
            return redirect(url_for(success)), 302
        else:
            if not form.cid.data:
                raise Exception('error en reseteo')

            cid = form.cid.data
            ri = credentialsModel.get_reset_info(cid)
            emails = ri['mails']
            return render_template('input_code.html', form=form, emails=emails, version=config.version)

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400

@bp.route('/error', methods=['GET'])
def error():
    error = 'se ha producido un error enviadno el código'
    return render_template('error.html', error=error, version=config.version)


@bp.route('/success', methods=['GET'])
def success():
    return render_template('success.html', version=config.version)





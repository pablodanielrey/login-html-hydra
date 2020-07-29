import logging

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from .forms import InputUsername, InputCode, InputCredentials

from login_html_hydra.models.CredentialsModel import credentialsModel


"""
    debug 
"""

@bp.route('/debug/<username>', methods=['GET'])
def debug(username):
    ri = credentialsModel.get_indexed_reset_info(username)
    return render_template('debug.html', ri=ri, version=config.version)


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
        return render_template('input_code.html', form=form, emails=emails, version=config.version)

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400    

@bp.route('/code/<cid>', methods=['POST'])
def input_code_post(cid):
    try:
        assert cid is not None
        form = InputCode()
        if form.validate_on_submit():
            logging.info(f'reseteo de clave {form.code.data} {cid}')
            code = form.code.data
            reset_code = credentialsModel.verify_code(cid, code)
            return redirect(url_for('reset_credentials.input_credentials', cid=reset_code)), 302
        else:
            ri = credentialsModel.get_reset_info(cid)
            emails = ri['mails']
            return render_template('input_code.html', form=form, emails=emails, version=config.version)

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de reseteo', version=config.version), 400


"""
    paso 3 - ingresa las credenciales nuevas
"""

@bp.route('/credentials/<cid>', methods=['GET'])
def input_credentials(cid):
    form = InputCredentials()
    return render_template('input_credentials.html', form=form, version=config.version)

@bp.route('/credentials/<cid>', methods=['POST'])
def input_credentials_post(cid):
    try:
        assert cid is not None
        form = InputCredentials()
        if form.validate_on_submit():
            logging.info(f'reseteo de clave {cid}')
            password = form.password.data
            password2 = form.password2.data
            if password != password2:
                return render_template('input_credentials.html', form=form, version=config.version)
            credentialsModel.reset_credentials(cid, password)
            return redirect(url_for('reset_credentials.success')), 302
        else:
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





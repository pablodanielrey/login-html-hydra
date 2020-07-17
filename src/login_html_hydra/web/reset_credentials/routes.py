import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from .forms import InputUsername, InputCode, InputCredentials

@bp.route('/error', methods=['GET'])
def error():
    error = 'se ha producido un error enviadno el código'
    return render_template('error.html', error=error, version=config.version)


@bp.route('/success', methods=['GET'])
def success():
    return render_template('success.html', version=config.version)

@bp.route('/credentials', methods=['GET'])
def input_credentials():
    form = InputCredentials()
    return render_template('input_credentials.html', form=form, version=config.version)

@bp.route('/credentials', methods=['POST'])
def input_credentials_post():
    form = InputCredentials()
    return redirect(url_for(success))


@bp.route('/code', methods=['GET'])
def input_code():
    form = InputCode()
    return render_template('input_code.html', form=form, version=config.version)

@bp.route('/code', methods=['POST'])
def input_code_post():
    form = InputCode()
    return redirect(url_for(input_credentials))

@bp.route('/username', methods=['GET'])
def input_username():
    form = InputUsername()
    return render_template('input_username.html', form=form, version=config.version)

@bp.route('/username', methods=['POST'])
def input_username_post():
    form = InputUsername()
    return redirect(url_for(input_code))


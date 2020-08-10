import logging
import inject

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

from login_html_hydra.models.ChangeCredentialsModel import ChangeCredentialsModel
changeCredentialsModel = inject.instance(ChangeCredentialsModel)

from .forms import ChangeCredentialsForm

@bp.route('/<code>', methods=['GET'])
def change_credentials_get(code):
    try:
        assert code is not None
        form = ChangeCredentialsForm()
        return render_template('change_credentials.html', form=form, version=config.version), 200        
    except Exception as e:
        return render_template('change_credentials_error.html', error='error', version=config.version), 400

@bp.route('/<code>', methods=['POST'])
def change_credentials_post(code):
    try:
        assert code is not None

        form = ChangeCredentialsForm()
        if form.validate_on_submit():
            p1 = form.password2.data
            p2 = form.password2_confirmation.data
            if p1 == p2:
                redirect_url = changeCredentialsModel.change_credentials(code, p1)
                assert redirect_url is not None
                return redirect(redirect_url), 302
            else:
                logging.info(f'claves inválidas')
                return render_template('change_credentials_error.html', error='verifique las claves', version=config.version), 400
        else:
            return render_template('change_credentials_error.html', error='faltan datos requeridos', version=config.version), 400

    except Exception as e:
        return render_template('change_credentials_error.html', error='error', version=config.version), 400

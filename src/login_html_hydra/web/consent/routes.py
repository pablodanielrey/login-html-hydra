import logging
import inject

from login_html_hydra.models.LoginHydraModel import LoginHydraModel

from flask import render_template, flash, redirect,request, Markup, url_for, request
from . import bp, config

loginHydraModel = inject.instance(LoginHydraModel)

@bp.route('/', methods=['GET'])
def consent():
    """
        paso 3
        Ruta solicitada por hydra cuando se inicia acepto un challenge de consent
        consent_challenge va como parámetro query.
        https://www.ory.sh/hydra/docs/reference/api/#get-consent-request-information
    """
    try:
        challenge = request.args.get('consent_challenge')
        redirect_url = loginHydraModel.check_and_accept_consent_challenge(challenge)
        return redirect(redirect_url), 302

    except Exception as e:
        logging.exception(e)
        return render_template('error.html', error='Error de ingreso', version=config.version), 400
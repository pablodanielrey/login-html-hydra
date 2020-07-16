import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for, request
from . import bp, config

from login_html_hydra.models import loginHydraModel

@bp.route('/', methods=['GET'])
def consent():
    """
        paso 3
        Ruta solicitada por hydra cuando se inicia acepto un challenge de login
        login_challenge va como parámetro query.
        https://www.ory.sh/hydra/docs/reference/api/#get-consent-request-information
    """
    challenge = request.args.get('consent_challenge')
    ok, redirect_url = loginHydraModel.check_and_accept_consent_challenge(challenge)
    if ok:
        return redirect(redirect_url)
    else:
        return render_template('error.html', error='Error de ingreso', version=config.version)

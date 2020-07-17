import logging
logging.getLogger().setLevel(logging.INFO)

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

@bp.route('/', methods=['GET'])
def consent():
    return render_template('consent.html', version=config.version)


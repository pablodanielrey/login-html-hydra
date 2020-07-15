from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

@bp.route('/')
def index():
    """
    Pagina de login
    """
    return render_template('login.html', version=config.version)
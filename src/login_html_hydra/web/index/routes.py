from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp, config

@bp.route('/')
def index():
    return render_template('index.html', version=config.version)
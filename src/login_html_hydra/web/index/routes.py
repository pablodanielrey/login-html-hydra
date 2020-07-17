from flask import render_template, flash, redirect,request, Markup, url_for, send_from_directory, jsonify
from . import bp, config

@bp.route('/')
def index():
    return render_template('index.html', version=config.version)

@bp.route('/error')
def error():
    return render_template('error.html', error='aaaaaaaaaa', version=config.version)

from flask import render_template, flash, redirect,request, Markup, url_for, send_from_directory, jsonify
from . import bp, config

@bp.route('/')
def index():
    r = {
        'version': config.version,
        'dir': bp.root_path
    }
    return jsonify(r)


@bp.route('/error')
def error():
    return render_template('error.html', error='', version=config.version)


@bp.route('/assets/<path:filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(f'{bp.root_path}/assets', filename, as_attachment=True)
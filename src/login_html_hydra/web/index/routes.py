from flask import render_template, flash, redirect,request, Markup, url_for, send_from_directory, jsonify
from . import bp, config

@bp.route('/')
def index():
    #return render_template('index.html', version=config.version)
    r = {
        'version': config.version,
        'dir': bp.root_path
    }
    return jsonify(r)

@bp.route('/assets/<path:filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(f'{bp.root_path}/assets', filename, as_attachment=True)
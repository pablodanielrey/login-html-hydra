from flask import Flask
webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'you-will-never-guess'

from .index import bp as index_bp
webapp.register_blueprint(index_bp)

from .login import bp as login_bp
webapp.register_blueprint(login_bp, url_prefix='/login')

from .consent import bp as consent_bp
webapp.register_blueprint(consent_bp, url_prefix='/consent')

from .change_credentials import bp as change_credentials_bp
webapp.register_blueprint(change_credentials_bp, url_prefix='/change_credentials')

from .reset_credentials import bp as reset_credentials_bp
webapp.register_blueprint(reset_credentials_bp, url_prefix='/reset_credentials')
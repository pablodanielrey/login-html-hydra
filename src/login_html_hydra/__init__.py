from flask import Flask
webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'you-will-never-guess'

from .web.index import bp as index_bp
webapp.register_blueprint(index_bp)

from .web.login import bp as login_bp
webapp.register_blueprint(login_bp, url_prefix='/login')
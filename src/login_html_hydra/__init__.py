from flask import Flask
webapp = Flask(__name__)


from .web.login import bp as login_bp
webapp.register_blueprint(login_bp)
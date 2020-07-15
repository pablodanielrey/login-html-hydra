from flask import Flask
webapp = Flask(__name__)

from .web.index import bp as web_bp

webapp.register_blueprint(web_bp)
from flask import Flask
from flask_jwt_extended import JWTManager

from ysl.api.router import bp_interviewer, bp_admin
from ysl.config.config import Config


def create_app():
    _app = Flask('ysl')

    _app.register_blueprint(bp_interviewer)
    _app.register_blueprint(bp_admin)

    _app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    _app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
    _app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES

    JWTManager(app=_app)

    return _app

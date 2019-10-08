from flask import Flask
from flask_jwt_extended import JWTManager

from ysl.api.router import bp_interviewer, bp_admin


def create_app(config):
    _app = Flask('ysl')

    _app.register_blueprint(bp_interviewer)
    _app.register_blueprint(bp_admin)

    _app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    _app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
    _app.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.JWT_REFRESH_TOKEN_EXPIRES

    _app.config['HOST'] = config.HOST
    _app.config['PORT'] = config.PORT
    _app.config['DEBUG'] = config.DEBUG

    JWTManager(app=_app)

    return _app

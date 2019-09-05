from flask import Flask
from flask_jwt_extended import JWTManager

from ysl.api.interviewer import bp_agency
from ysl.api.admin import bp_admin
from ysl.api.agency import bp_test
from ysl.config.config import TestConfig


def create_app():
    _app = Flask('ysl')

    _app.register_blueprint(bp_agency)
    _app.register_blueprint(bp_admin)
    _app.register_blueprint(bp_test)

    _app.config['JWT_SECRET_KEY'] = TestConfig.JWT_SECRET_KEY
    _app.config['JWT_ACCESS_TOKEN_EXPIRES'] = TestConfig.JWT_ACCESS_TOKEN_EXPIRES
    _app.config['JWT_REFRESH_TOKEN_EXPIRES'] = TestConfig.JWT_REFRESH_TOKEN_EXPIRES

    JWTManager(app=_app)

    return _app

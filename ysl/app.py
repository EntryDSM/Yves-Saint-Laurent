from flask import Flask

from ysl.api.test import bp_test


def create_app():
    _app = Flask(__name__)

    _app.register_blueprint(bp_test)

    return _app

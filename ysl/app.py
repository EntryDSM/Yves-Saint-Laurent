from flask import Flask

from ysl.api.agency import bp_agency
from ysl.api.admin import bp_admin
from ysl.db import db
from ysl.config.vault import get_vault_secret_url


def create_app(env):
    _app = Flask('ysl')

    _app.register_blueprint(bp_agency)
    _app.register_blueprint(bp_admin)

    db.init_app(_app)
    db.create_all(app=_app)
    _app.config['SQLALCHEMY_DATABASE_URI'] = get_vault_secret_url(env=env)

    return _app

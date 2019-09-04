from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps

from ysl.db.agency import Agency
from ysl.db import session


def check_json(json):
    def decorator(func):
        @wraps(func)
        def wrapeer(*args, **kwargs):
            if not request.is_json:
                abort(400, "Check json format")

            for k, v in json.items():
                if k not in request.json or type(request.json[k]) is not v:
                    abort(400, "Check you json key name and value type")

            return func(*args, **kwargs)
        return wrapeer
    return decorator


def check_admin():
    def decorator(func):
        @wraps(func)
        @jwt_required
        def wrapeer(*args, **kwargs):

            agency = session.query(Agency).query.filter(Agency.email == get_jwt_identity()).first()

            if not agency:
                abort(403, "No access rights")

            return func(*args, **kwargs)
        return wrapeer
    return decorator


def check_agency():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            agency = session.query(Agency).query.filter(Agency.code == get_jwt_identity()).first()

            if not agency:
                abort(400, "unseen agency")

            return func(*args, **kwargs)
        return wrapper
    return decorator

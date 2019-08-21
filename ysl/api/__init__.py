from flask import request, abort
from flask_jwt_extended  import get_jwt_identity
from functools import wraps

from ysl.db.agency import Agency


def check_json():
    def decorator(func):
        @wraps(func)
        def wrapeer(*args, **kwargs):
            if not request.is_json:
                abort(400, "Check json format")
            return func(*args, **kwargs)
        return wrapeer
    return decorator


def check_admin():
    def decorator(func):
        @wraps(func)
        def wrapeer(*args, **kwargs):
            if not Agency.query.filter(email=get_jwt_identity()).first():
                abort(403, "No access rights")
            return func(*args, **kwargs)
        return wrapeer
    return decorator

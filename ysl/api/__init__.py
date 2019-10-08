from flask import request, abort
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from ysl.db.agency import Agency
from ysl.db.belong import Belong
from ysl.db.access import Access
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


def check_admin(agency_code):
    admin = session.query(Agency).filter(
        Agency.code == agency_code).filter(Agency.email == get_jwt_identity()).first()

    if not admin:
        abort(403, "No access rights")


def check_agency_belong(agency_code):
    belong = session.query(Belong).filter(
        Belong.agency == agency_code).filter(Belong.interviewer == get_jwt_identity()).first()

    if not belong:
        abort(403, "No access rights")


def check_access_interview(interview_id):
    access = session.query(Access).filter(
        Access.interview == interview_id).filter(Access.interviewer == get_jwt_identity()).first()

    if not access:
        abort(403, "No access rights")

from flask import request, abort
from flask_restful import Resource
from secrets import token_hex
from werkzeug.security import generate_password_hash

from ysl.db.agency import Agency
from ysl.db import session
from ysl.api import check_json


class AdminSignup(Resource):
    @check_json({
        "agency_name": str,
        "agency_kind": str,
        "email": str,
        "password": str,
        "agency_explanation": str
    })
    def post(self):
        agency_name = request.json["agency_name"]
        agency_kind = request.json["agency_kind"]
        email = request.json["email"]
        password = generate_password_hash(request.json["password"])
        agency_explanation = request.json["agency_explanation"]

        admin = session.query(Agency).filter(Agency.email == email).first()

        if admin:
            abort(409, "This email has already been signed up")
        else:
            add_agency = Agency(code=token_hex(nbytes=3), email=email, pw=password, name=agency_name,
                                kind=agency_kind, explanation=agency_explanation)
            session.add(add_agency)
            session.commit()
            return {"msg": "Successful signup to admin"}, 201

from flask import Blueprint, request, abort
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex
from werkzeug.security import generate_password_hash, check_password_hash

from ysl.db.agency import Agency
from ysl.db import session
from ysl.api import check_json

bp_admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")
api_admin = Api(bp_admin)


#이메일인증 추가예정
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
            return {"msg": "Successful signup to admin"}, 200


class AdminLogin(Resource):
    @check_json({"email": str, "password": str})
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        admin = session.query(Agency).filter(Agency.email == email and check_password_hash(Agency.pw, password))

        if admin:
            return {
                "access": create_access_token(identity=admin.code),
                "refresh": create_refresh_token(identity=email)
            }, 200
        else:
            return abort(400, "Check email and password")


api_admin.add_resource(AdminSignup, "/signup")
api_admin.add_resource(AdminLogin, "/login")

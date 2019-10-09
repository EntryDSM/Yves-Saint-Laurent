from flask import request, abort
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity

from ysl.db import session
from ysl.db.interviewer import Interviewer
from ysl.db.agency import Agency
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.api import check_json


class CheckAgencyCode(Resource):
    def get(self):
        agency_code = request.args.get('code')

        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        if agency:
            return {"agency_name": agency.name,
                    "agency_explanation": agency.explanation}, 200
        else:
            return abort(400, "unseen agency")


class InterviewerSignup(Resource):
    @check_json({
        "name": str,
        "email": str,
        "password": str,
        "agency": str
    })
    def post(self):
        name = request.json["name"]
        email = request.json["email"]
        password = generate_password_hash(request.json["password"])
        agency = request.json["agency"]

        interviewer = session.query(Interviewer).filter(Interviewer.email == email).first()
        check_agency = session.query(Agency).filter(Agency.code == agency).first()

        if interviewer:
            abort(409, "This email has already been signed up")
        else:
            if check_agency:
                add_interviewer = Interviewer(name=name, email=email, pw=password)
                session.add(add_interviewer)
                session.commit()

                add_apply_interviewer = ApplyInterviewer(agency=agency, interviewer=email)
                session.add(add_apply_interviewer)
                session.commit()
                return {"msg": "Successful signup to interviewer"}, 201
            else:
                abort(404, "Not found Agency")


class Login(Resource):
    @check_json({
        "email": str,
        "password": str
    })
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        interviewer = session.query(Interviewer).filter(Interviewer.email == email).first()
        interviewer_qw_check = check_password_hash(interviewer.pw, password) if interviewer else None

        admin = session.query(Agency).filter(Agency.email == email).first()
        admin_pw_check = check_password_hash(admin.pw, password) if admin else None

        if interviewer_qw_check:
            return {
                        "admin": False,
                        "access": create_access_token(identity=email),
                        "refresh": create_refresh_token(identity=email)
            }, 200
        elif admin_pw_check:
            return {
                       "admin": True,
                       "access": create_access_token(identity=email),
                       "refresh": create_refresh_token(identity=email)
                   }, 200
        else:
            return abort(400, "Check email and password")


class Refresh(Resource):
    @jwt_refresh_token_required
    def patch(self):
        admin = session.query(Agency).filter(Agency.email == get_jwt_identity()).first()
        interviewer = session.query(Interviewer).filter(Interviewer.email == get_jwt_identity()).first()

        if admin:
            return {
                "access": create_access_token(identity=admin.email),
                "refresh": create_refresh_token(identity=admin.email)
            }, 200
        elif interviewer:
            return {
                "access": create_access_token(identity=interviewer.email),
                "refresh": create_refresh_token(identity=interviewer.email)
            }, 200
        else:
            return abort(400, "None Response")

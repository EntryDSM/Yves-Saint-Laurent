from flask import Blueprint, request, abort
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from ysl.db import session
from ysl.db.interviewer import Interviewer
from ysl.db.agency import Agency

bp_interviewer = Blueprint("agency", __name__, url_prefix="/api/v1")
api_interviewer = Api(bp_interviewer)


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
    def post(self):
        name = request.json["name"]
        email = request.json["email"]
        password = generate_password_hash(request.json["password"])

        interviewer = session.query(Interviewer).filter(Interviewer.email == email).first()

        if interviewer:
            abort(409, "This email has already been signed up")
        else:
            add_interviewer = Interviewer(name=name, email=email, pw=password)
            session.add(add_interviewer)
            session.commit()
            return {"msg": "Successful signup to interviewer"}, 409


class InterviewerLogin(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        interviewer = session.query(Interviewer).filter(
            Interviewer.email == email and check_password_hash(Interviewer.pw, password))

        if interviewer:
            return {
                    "access": create_access_token(identity=email),
                    "refresh": create_refresh_token(identity=email)
            }, 200
        else:
            return abort(400, "Check email and password")


api_interviewer.add_resource(CheckAgencyCode, "/agency/check")
api_interviewer.add_resource(InterviewerSignup, "/interviewer/signup")
api_interviewer.add_resource(InterviewerLogin, "/interviewer/login")



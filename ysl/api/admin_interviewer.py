from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db.belong import Belong
from ysl.db.interviewer import Interviewer
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.db import session
from ysl.api import check_admin, check_json


class AcceptInterviewer(Resource):
    @jwt_required
    @check_json({"user_email": str})
    def post(self, agency_code):
        check_admin(agency_code)

        interviewer = request.json["user_email"]

        belong_interviewer = session.query(Belong).filter(Belong.interviewer == interviewer).filter(
            Belong.agency == agency_code
        ).first()

        if belong_interviewer:
            abort(409, "This email has already been belong agency")

        add_interviewer = Belong(agency=agency_code, interviewer=interviewer)
        session.add(add_interviewer)

        delete_interviewer = session.query(ApplyInterviewer).filter(
            ApplyInterviewer.agency == agency_code).filter(ApplyInterviewer.interviewer == interviewer).first()

        if delete_interviewer:
            session.delete(delete_interviewer)
            session.commit()
            return {"msg": "Successful interviewer accept"}, 200
        else:
            return abort(400, "This is an interviewer who didn't apply")


class RejectInterviewer(Resource):
    @check_json({"user_email": str})
    def post(self, agency_code):
        check_admin(agency_code)

        interviewer = request.json["user_email"]

        delete_interviewer = session.query(ApplyInterviewer).filter(
            ApplyInterviewer.agency == agency_code).filter(ApplyInterviewer.interviewer == interviewer).first()

        if delete_interviewer:
            session.delete(delete_interviewer)
            session.commit()
            return {"msg": "Successful interviewer reject"}, 200
        else:
            return abort(400, "This is an interviewer who didn't apply")


class InterviewerList(Resource):
    @jwt_required
    def get(self, agency_code):
        check_admin(agency_code)

        interviewers = session.query(Belong, Interviewer).join(Interviewer).filter(Belong.agency == agency_code).all()

        if interviewers:
            return {
                "interviewer": [
                    {
                        "interviewer_name": interviewer.Interviewer.name,
                        "interviewer_email": interviewer.Interviewer.email
                    } for interviewer in interviewers]
            }, 200
        else:
            abort(404, "There is no interviewer who is registered.")

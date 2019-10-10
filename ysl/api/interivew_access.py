from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.access import Access
from ysl.db.interviewer import Interviewer
from ysl.api import check_json, check_admin


class AddAccessInterviewer(Resource):
    @jwt_required
    def get(self, agency_code, interview_id):
        check_admin(agency_code)

        access_interviewers = session.query(Access, Interviewer).join(Interviewer).filter(
                              Access.interview == interview_id).all()

        if access_interviewers:
            return {
                "interviewer": [
                    {
                        "interviewer_name": interviewer.Interviewer.name,
                        "interviewer_email": interviewer.Interviewer.email
                    } for interviewer in access_interviewers]
            }
        else:
            abort(404, "None interviewer")

    @jwt_required
    @check_json({"interviewer_email": str})
    def post(self, agency_code, interview_id):
        check_admin(agency_code)

        interviewer = request.json["interviewer_email"]

        add_access_interviewer = Access(interview=interview_id, interviewer=interviewer)

        session.add(add_access_interviewer)
        session.commit()

        return {"msg": "Successful interviewer access"}, 200

    @jwt_required
    def delete(self, agency_code, interview_id):
        check_admin(agency_code)

        interviewer = request.json["interviewer_email"]

        access_interviewer = session.query(Access).filter(
            Access.interview == interview_id and Access.interviewer == interviewer).first()

        if access_interviewer:
            session.delete(access_interviewer)
            session.commit()
            return {"msg": "Successful delete access interviewer"}, 200
        else:
            abort(404, "None interviewer")



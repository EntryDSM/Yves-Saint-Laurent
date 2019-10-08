from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db.agency import Agency
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.db.interviewer import Interviewer
from ysl.db import session
from ysl.api import check_admin, check_json


class AgencyInformation(Resource):
    @jwt_required
    def get(self, agency_code):
        check_admin(agency_code)
        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        if agency:
            return {
                    "agency_name": agency.name,
                    "agency_kind": agency.kind,
                    "agency_explanation": agency.explanation,
                    "agency_code": agency.code
                }, 200
        else:
            abort(400, "unseen agency")

    @jwt_required
    def delete(self, agency_code):
        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        session.delete(agency)
        session.commit()

        return {"msg": "successful agency delete"}, 200

    @jwt_required
    @check_json({"explanation": str})
    def patch(self, agency_code):
        explanation = request.json['explanation']

        agency = session.query(Agency).filter(Agency.code == agency_code).first()
        agency.explanation = explanation

        session.commit()

        return {"msg": "successful change agency explanation"}, 200


class ApplyInterviewerList(Resource):
    @jwt_required
    def get(self, agency_code):
        check_admin(agency_code)

        interviewers = session.query(ApplyInterviewer, Interviewer).join(Interviewer).filter(
            ApplyInterviewer.agency == agency_code).all()

        if interviewers:
            return {"interviewer": [
                {
                    "interviewer_name": interviewer.Interviewer.name,
                    "interviewer_email": interviewer.Interviewer.email
                } for interviewer in interviewers]
            }, 200
        else:
            abort(400, "unseen apply interviewer list")

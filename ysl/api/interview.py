from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interview import Interview
from ysl.api import check_agency_belong


class OngoingInterview(Resource):
    @jwt_required
    def get(self, agency_code):
        check_agency_belong(agency_code)

        ongoing_interviews = session.query(Interview).filter(
            Interview.agency == agency_code).filter(Interview.status == 2).all()

        if ongoing_interviews:
            return {
                       "interview": [
                           {
                               "interview_name": interview.interview_name,
                               "interview_explanation": interview.explanation,
                               "interview_id": interview.interview_id
                           } for interview in ongoing_interviews]
                   }, 200
        else:
            return abort(400, "None Resources")

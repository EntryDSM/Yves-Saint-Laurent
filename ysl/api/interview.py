from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interview import Interview
from ysl.api.interviewer import api_interviewer


class OngoingInterview(Resource):
    @jwt_required
    def get(self, agency_code):
        ongoing_interview = session.query(Interview).filter(
            Interview.agency == agency_code and Interview.status == 2).all()

        if ongoing_interview:
            return {
                       "interview": [
                           {
                               "interview_name": interview.interview_name,
                               "interview_explanation": interview.explanation
                           } for interview in ongoing_interview]
                   }, 200
        else:
            return abort(400, "None Resources")


api_interviewer.add_resource(OngoingInterview, "/{agency_code}")

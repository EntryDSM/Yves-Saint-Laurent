from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interview import Interview
from ysl.api import check_admin


class ReadyInterview(Resource):
    @jwt_required
    def get(self, agency_code):
        check_admin(agency_code)

        ready_interviews = session.query(Interview).filter(
            Interview.agency == agency_code).filter(Interview.status == 1).all()

        if ready_interviews:
            return {
                "interview": [
                    {
                        "interview_name": interview.interview_name,
                        "interview_explanation": interview.explanation,
                        "interview_id": interview.interview_id
                    } for interview in ready_interviews]
            }, 200
        else:
            return abort(400, "None Resources")


class DoneInterview(Resource):
    @jwt_required
    def get(self, agency_code):
        check_admin(agency_code)

        done_interviews = session.query(Interview).filter(
            Interview.agency == agency_code).filter(Interview.status == 3).all()

        if done_interviews:
            return {
                       "interview": [
                           {
                               "interview_name": interview.interview_name,
                               "interview_explanation": interview.explanation,
                               "interview_id": interview.interview_id
                           } for interview in done_interviews]
                   }, 200
        else:
            return abort(400, "None Resources")


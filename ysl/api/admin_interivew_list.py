from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interview import Interview
from ysl.api.admin import api_admin
from ysl.api import check_agency, check_admin


class ReadyInterview(Resource):
    @jwt_required
    @check_admin()
    @check_agency()
    def get(self, agency_code):
        ready_interview = session.query(Interview).filter(
            Interview.agency == agency_code and Interview.status == 1).all()

        if ready_interview:
            return {
                "interview": [
                    {
                        "interview_name": interview.interview_name,
                        "interview_explanation": interview.explanation
                    } for interview in ready_interview]
            }, 200
        else:
            return abort(400, "None Resources")


class DoneInterview(Resource):
    @jwt_required
    @check_admin()
    @check_agency()
    def get(self, agency_code):
        done_interview = session.query(Interview).filter(
            Interview.agency == agency_code and Interview.status == 3).all()

        if done_interview:
            return {
                       "interview": [
                           {
                               "interview_name": interview.interview_name,
                               "interview_explanation": interview.explanation
                           } for interview in done_interview]
                   }, 200
        else:
            return abort(400, "None Resources")


api_admin.add_resource(ReadyInterview, "/{agency_code}/ready/interview")
api_admin.add_resource(DoneInterview, "/{agency_code}/done/interview")

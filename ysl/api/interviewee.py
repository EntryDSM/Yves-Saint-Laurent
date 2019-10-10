from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.api import check_admin
from ysl.db.interviewee import Interviewee


class SearchInterviewee(Resource):
    @jwt_required
    def get(self, agency_code, interview_id):
        check_admin(agency_code)

        student_code = request.args.get('code')

        interviewee = session.query(Interviewee).filter(
            Interviewee.student_code == student_code).filter(Interviewee.interview == interview_id).first()

        if interviewee:
            return {
                       "interviewee": interviewee.name,
                       "interviewee_id": interviewee.student_code
                   }, 200
        else:
            abort(404, "an interviewee without")


class AddInterviewee(Resource):
    @jwt_required
    def post(self):
        pass
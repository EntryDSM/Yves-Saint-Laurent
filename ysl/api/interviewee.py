from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interviewee import Interviewee
from ysl.api.interviewer import api_interviewer


class SearchInterviewee(Resource):
    @jwt_required
    def post(self, interview_id):
        student_code = request.args.get('interviewee')

        interviewee = session.query(Interviewee).filter(
            Interviewee.student_code == student_code and Interviewee.interview == interview_id)

        if interviewee:
            return {"interviewee": interviewee.name}, 200
        else:
            abort(400, "an interviewee without")


api_interviewer.add_resource(SearchInterviewee, "/{agency_code}/{interview_id}")

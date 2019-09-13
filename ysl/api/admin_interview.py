from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ysl.db import session
from ysl.db.interview import Interview
from ysl.db.question import Question
from ysl.api.admin import api_admin
from ysl.api import check_json, check_agency, check_admin


class CreateInterview(Resource):
    @jwt_required
    @check_admin()
    @check_agency()
    @check_json({
        "name": str,
        "start_date": str,
        "end_date": str})
    def post(self):
        name = request.json["name"]
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]
        agency_code = get_jwt_identity()

        add_interview = Interview(interview_name=name, start_day=start_date, end_day=end_date, agency=agency_code)

        session.add(add_interview)
        session.commit()

        return {"msg": "Successful create interview"}, 201


class CreateQuestion(Resource):
    @jwt_required
    @check_admin()
    @check_agency()
    @check_json({
        "question_num": int,
        "content": str,
        "type": int})
    def post(self, interview_code):
        question_num = request.json["question_num"]
        content = request.json["content"]
        type = request.json["type"]

        add_question = Question(num=question_num, content=content, type=type, interview=interview_code)

        session.add(add_question)
        session.commit()

        return {"msg": " Successful create interview question"}, 201


class InterviewQuestion(Resource):
    @jwt_required
    @check_admin()
    @check_agency()
    def get(self, question_code):
        question = session.query(Question).filter(Question.id == question_code).first()

        if question:
            return {
                "interview_question": [
                    {
                        "question_num": question.num,
                        "content": question.content,
                        "type": question.type
                    }
                ]
            }, 200
        else:
            return abort(400, "None Resources")

    @jwt_required
    @check_admin()
    @check_agency()
    @check_json({
        "question_num": int,
        "content": str,
        "type": int})
    def put(self, question_code):
        question_num = request.json["question_num"]
        content = request.json["content"]
        type = request.json["type"]

        question = session.query(Question).filter(Question.id == question_code).first()

        if question:
            question.num = question_num
            question.content = content
            question.type = type

            session.commit()
            return {"msg": "Successful change question"}, 200
        else:
            return abort(400, "None Resources")

    @jwt_required
    @check_admin()
    @check_agency()
    def delete(self, question_code):
        question = session.query(Question).filter(Question.id == question_code).first()

        if question:
            session.delete(question)
            session.commit()
            return {"msg": "Successful delete question"}
        else:
            return abort(400, "None Resources")


api_admin.add_resource(CreateInterview, "/{agency_code}/interview")
api_admin.add_resource(CreateQuestion, "/{agency_code}/{interview_id}/question")
api_admin.add_resource(InterviewQuestion, "/{agency_code}/{interview_id}/{question_id}")

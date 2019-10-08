from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interview import Interview
from ysl.db.question import Question
from ysl.api import check_json, check_admin


class CreateInterview(Resource):
    @jwt_required
    @check_json({
        "name": str,
        "start_date": str,
        "end_date": str,
        "interview_explanation": str})
    def post(self, agency_code):
        check_admin(agency_code)

        name = request.json["name"]
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]
        interview_explanation = request.json["interview_explanation"]

        add_interview = Interview(interview_name=name, start_day=start_date,
                                  end_day=end_date, agency=agency_code, explanation=interview_explanation)

        session.add(add_interview)
        session.commit()

        return {"msg": "Successful create interview"}, 201


class CreateQuestion(Resource):
    @jwt_required
    def post(self, agency_code, interview_id):
        check_admin(agency_code)

        questions = request.json["question"]

        for question in questions:
            add_question = Question(num=question['question_num'], content=question['content'],
                                    type=question['type'], interview=interview_id)
            session.add(add_question)
            session.commit()

        return {"msg": " Successful create question"}, 201

    @jwt_required
    def get(self, agency_code, interview_id):
        check_admin(agency_code)

        questions = session.query(Question).filter(Question.interview == interview_id).all()

        if questions:
            return {
                       "interview_question": [
                           {
                               "question_id": question.id,
                               "question_num": question.num,
                               "content": question.content,
                               "type": question.type
                           } for question in questions]
                   }, 200
        else:
            return abort(400, "None Resources")

    @jwt_required
    def put(self, agency_code, interview_id):
        check_admin(agency_code)

        delete_questions = session.query(Question).filter(Question.interview == interview_id).all()

        for delete_question in delete_questions:
            session.delete(delete_question)
            session.commit()

        questions = request.json["question"]

        for question in questions:
            add_question = Question(num=question['question_num'], content=question['content'],
                                    type=question['type'], interview=interview_id)
            session.add(add_question)
            session.commit()

        return {"msg": " Successful change interview question"}, 201


class InterviewQuestion(Resource):
    @jwt_required
    def delete(self, agency_code, interview_id, question_id):
        check_admin(agency_code)

        question = session.query(Question).filter(Question.id == question_id and
                                                  Question.interview == interview_id).first()

        if question:
            session.delete(question)
            session.commit()
            return {"msg": "Successful delete question"}
        else:
            return abort(400, "None Resources")

from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.interview import Interview
from ysl.db.question import Question
from ysl.db.question_check_list import QuestionCheckList
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

        return {"interview_id": add_interview.interview_id}, 201


class CreateQuestion(Resource):
    @jwt_required
    def post(self, agency_code, interview_id):
        check_admin(agency_code)

        questions = request.json["question"]

        for question in questions:
            add_question = Question(num=question['question_num'], title=question['question_title'],
                                    type=question['question_type'], interview=interview_id)

            session.add(add_question)
            session.commit()

            question_id = session.query(Question).filter(Question.interview == interview_id).filter(
                          Question.num == question['question_num']).first()

            check_lists = question['check_list']

            if not check_lists == []:
                for i in range(len(check_lists)):
                    add_check_list = QuestionCheckList(question=question_id.id, content=check_lists[i])

                    session.add(add_check_list)
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
                            "question_title": question.title,
                            "question_type": question.type,
                            "check_list": [check_list.content for check_list in session.query(QuestionCheckList).filter(
                                                                  QuestionCheckList.question == question.id).all()]
                        } for question in questions]
                   }, 200
        else:
            return abort(404, "None Resources")

    @jwt_required
    def put(self, agency_code, interview_id):
        check_admin(agency_code)

        questions = session.query(Question).filter(Question.interview == interview_id).filter(
            Question.interview == interview_id).all()

        for question in questions:
            check_lists = session.query(QuestionCheckList).filter(QuestionCheckList.question == question.id).all()

            if check_lists:
                for check_list in check_lists:
                    session.delete(check_list)
                    session.commit()
            else:
                session.delete(question)
                session.commit()

        questions = request.json["question"]

        for question in questions:
            add_question = Question(num=question['question_num'], title=question['question_title'],
                                    type=question['question_type'], interview=interview_id)

            session.add(add_question)
            session.commit()

            question_id = session.query(Question).filter(Question.interview == interview_id).filter(
                Question.num == question['question_num']).first()

            check_lists = question['check_list']

            if not check_lists == []:
                for i in range(len(check_lists)):
                    add_check_list = QuestionCheckList(question=question_id.id, content=check_lists[i])

                    session.add(add_check_list)
                    session.commit()

        return {"msg": " Successful change interview question"}, 201


class InterviewQuestion(Resource):
    @jwt_required
    def delete(self, agency_code, interview_id, question_id):
        check_admin(agency_code)

        question = session.query(Question).filter(Question.id == question_id).filter(
                                                  Question.interview == interview_id).first()

        check_lists = session.query(QuestionCheckList).filter(QuestionCheckList.question == question_id).all()

        if question:
            session.delete(question)
            session.commit()

            if check_lists:
                for check_list in check_lists:
                    session.delete(check_list)
                    session.commit()
            return {"msg": "Successful delete question"}

        else:
            return abort(404, "None Resources")

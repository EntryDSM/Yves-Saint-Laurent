from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ysl.db import session
from ysl.db.question import Question
from ysl.db.evaluation import Evaluation
from ysl.db.question_check_list import QuestionCheckList
from ysl.api import check_access_interview


class GetQuestionList(Resource):
    @jwt_required
    def get(self, agency_code, interview_id):
        check_access_interview(interview_id)

        questions = session.query(Question).filter(Question.interview == interview_id).all()

        if questions:
            return {
                       "interview_question": [
                           {
                               "question_id": question.id,
                               "question_num": question.num,
                               "question_title": question.title,
                               "question_type": question.type,
                               "check_list": [check_list.content for check_list in
                                              session.query(QuestionCheckList).filter(
                                                  QuestionCheckList.question == question.id).all()]
                           } for question in questions]
                   }, 200
        else:
            return abort(400, "None Resources")


class EvaluationForInterviewee(Resource):
    @jwt_required
    def get(self, agency_code, interview_id, student_code):
        check_access_interview(interview_id)

        evaluations = session.query(Evaluation, Question).join(Question).filter(
            Evaluation.interview == interview_id).filter(Evaluation.interviewer == get_jwt_identity()).filter(
            Evaluation.interviewee == student_code).all()

        if evaluations:
            return {
                    "evaluations": [
                        {
                            "question_id": evaluation.Question.id,
                            "question_num": evaluation.Question.num,
                            "question_type": evaluation.Question.type,
                            "question_content": evaluation.Question.content,
                            "evaluation": evaluation.Evaluation.answer
                        } for evaluation in evaluations]
            }, 200
        else:
            abort(400, "None Resources")

    @jwt_required
    def put(self, agency_code, interview_id, student_code):
        check_access_interview(interview_id)

        delete_evaluations = session.query(Evaluation).filter(Evaluation.interview == interview_id).filter(
                            Evaluation.interviewer == get_jwt_identity()).filter(
                            Evaluation.interviewee == student_code).all()

        for delete_evaluation in delete_evaluations:
            session.delete(delete_evaluation)
            session.commit()

        evaluations = request.json['evaluations']

        for evaluation in evaluations:
            add_question = Evaluation(question=evaluation['question_id'], interview=interview_id,
                                      interviewer=get_jwt_identity(), interviewee=student_code,
                                      answer=evaluation['evaluation'])
            session.add(add_question)
            session.commit()

        return {"msg": " Successful change evaluations"}, 201

    @jwt_required
    def post(self, agency_code, interview_id, student_code):
        check_access_interview(interview_id)

        evaluations = request.json['evaluations']

        for evaluation in evaluations:
            add_question = Evaluation(question=evaluation['question_id'], interview=interview_id,
                                      interviewer=get_jwt_identity(), interviewee=student_code,
                                      answer=evaluation['evaluation'])
            session.add(add_question)
            session.commit()

        return {"msg": " Successful create evaluations"}, 201

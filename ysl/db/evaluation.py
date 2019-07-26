from ysl.db import db


class Evaluation(db.Model):
    __tablename__ = 'EVALUATION_TB'

    id = db.Column(db.Integer, primary_key=True)
    interview = db.Column(db.Integer, db.ForeignKey("INTERVIEW_TB.interview_id"),
                          nullable=True)
    interviewer = db.Column(db.String(50), db.ForeignKey("INTERVIEWER_TB.email"),
                            nullable=True)
    interviewee = db.Column(db.Integer, db.ForeignKey("INTERVIEWEE_TB.student_code"),
                            nullable=True)
    question = db.Column(db.Integer, db.ForeignKey("QUESTION_TB.id"),
                         nullable=True)
    answer = db.Column(db.Text, nullable=True)

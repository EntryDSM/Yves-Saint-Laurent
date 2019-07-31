from ysl.db import db


class Question(db.Model):
    __tablename__ = 'QUESTION_TB'

    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=True)
    content = db.Column(db.String(100), nullable=True)
    type = db.Column(db.Integer, nullable=True)
    interview = db.Column(db.Integer, db.ForeignKey("INTERVIEW_TB.interview_id"), nullable=True)

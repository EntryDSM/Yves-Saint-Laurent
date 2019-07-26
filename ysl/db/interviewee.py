from ysl.db import db


class Interviewee(db.Model):
    __tablename__ = 'INTERVIEWEE_TB'

    student_code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    interview = db.Column(db.Integer, db.ForeignKey("INTERVIEW_TB.interview_id"), nullable=True)

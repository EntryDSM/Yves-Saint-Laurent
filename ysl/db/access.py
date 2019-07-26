from ysl.db import db


class Access(db.Model):
    __tablename__ = 'ACCESS_TB'

    interviewer = db.Column(db.String(50), db.ForeignKey("INTERVIEWER_TB.email"), primary_key=True)
    interview = db.Column(db.Integer, db.ForeignKey("INTERVIEW_TB.interview_id"), primary_key=True)

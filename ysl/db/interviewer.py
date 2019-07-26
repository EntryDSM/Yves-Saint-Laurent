from ysl.db import db


class Interviewer(db.Model):
    __tablename__ = 'INTERVIEWER_TB'

    email = db.Column(db.String(50), primary_key=True)
    pw = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)

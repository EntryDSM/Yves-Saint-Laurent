from ysl.db import db


class Agency(db.Model):
    __tablename__ = 'AGENCY_TB'

    code = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    pw = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    kind = db.Column(db.String(50), nullable=True)
    explanation = db.Column(db.Text, nullable=True)

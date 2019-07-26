from ysl.db import db


class Interview(db.Model):
    __tablename__ = 'INTERVIEW_TB'

    interview_id = db.Column(db.Integer, primary_key=True)
    interview_name = db.Column(db.String(50), nullable=True)
    start_day = db.Column(db.Date, nullable=True)
    end_day = db.Column(db.Date, nullable=True)
    status = db.Column(db.Integer, nullable=True, default=1)
    agency = db.Column(db.String(20), db.ForeignKey("AGENCY.code"), nullable=True)

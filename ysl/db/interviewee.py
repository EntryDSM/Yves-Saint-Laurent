from sqlalchemy import Column, String, ForeignKey, Integer, Text

from ysl.db import Base


class Interviewee(Base):
    __tablename__ = 'INTERVIEWEE_TB'

    student_code = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    interview = Column(Integer, ForeignKey("INTERVIEW_TB.interview_id"), nullable=True)

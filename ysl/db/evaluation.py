from sqlalchemy import Column, String, ForeignKey, Integer, Text

from ysl.db import Base


class Evaluation(Base):
    __tablename__ = 'EVALUATION_TB'

    id = Column(Integer, primary_key=True)
    interview = Column(Integer, ForeignKey("INTERVIEW_TB.interview_id"), nullable=True)
    interviewer = Column(String(50), ForeignKey("INTERVIEWER_TB.email"), nullable=True)
    interviewee = Column(Integer, ForeignKey("INTERVIEWEE_TB.student_code"), nullable=True)
    question = Column(Integer, ForeignKey("QUESTION_TB.id"), nullable=True)
    answer = Column(Text, nullable=True)

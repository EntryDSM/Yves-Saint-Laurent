from sqlalchemy import Column, String, ForeignKey, Integer

from ysl.db import Base


class Question(Base):
    __tablename__ = 'QUESTION_TB'

    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=True)
    title = Column(String(100), nullable=True)
    type = Column(Integer, nullable=True)
    interview = Column(Integer, ForeignKey("INTERVIEW_TB.interview_id"), nullable=True)

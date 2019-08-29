from sqlalchemy import Column, String

from ysl.db import Base


class Interviewer(Base):
    __tablename__ = 'INTERVIEWER_TB'

    email = Column(String(50), primary_key=True)
    pw = Column(String(50), nullable=True)
    name = Column(String(50), nullable=True)

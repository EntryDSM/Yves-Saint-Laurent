from sqlalchemy import Column, Integer, String, ForeignKey

from ysl.db import Base


class Access(Base):
    __tablename__ = 'ACCESS_TB'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    interviewer = Column(String(50), ForeignKey("INTERVIEWER_TB.email"), primary_key=True)
    interview = Column(Integer, ForeignKey("INTERVIEW_TB.interview_id"), primary_key=True)

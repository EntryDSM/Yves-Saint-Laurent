from sqlalchemy import Column, String

from ysl.db import Base


class Interviewer(Base):
    __tablename__ = 'INTERVIEWER_TB'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    email = Column(String(50), primary_key=True)
    pw = Column(String(200), nullable=True)
    name = Column(String(50), nullable=True)

from sqlalchemy import Column, String, ForeignKey

from ysl.db import Base


class Belong(Base):
    __tablename__ = 'BELOGN_TB'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    agency = Column(String(20), ForeignKey("AGENCY_TB.code"), primary_key=True)
    interviewer = Column(String(50), ForeignKey("INTERVIEWER_TB.email"), primary_key=True)

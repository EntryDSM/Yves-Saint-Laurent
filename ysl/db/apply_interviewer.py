from sqlalchemy import Column, String, ForeignKey

from ysl.db import Base


class ApplyInterviewer(Base):
    __tablename__ = 'APPLY_INTERVIEWER_TB'

    agency = Column(String(20), ForeignKey("AGENCY_TB.code"), primary_key=True)
    interviewer = Column(String(50), primary_key=True)

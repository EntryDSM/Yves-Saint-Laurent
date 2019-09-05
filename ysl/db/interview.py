from sqlalchemy import Column, String, ForeignKey, Integer, Date

from ysl.db import Base


class Interview(Base):
    __tablename__ = 'INTERVIEW_TB'

    interview_id = Column(Integer, primary_key=True)
    interview_name = Column(String(50), nullable=True)
    start_day = Column(Date, nullable=True)
    end_day = Column(Date, nullable=True)
    status = Column(Integer, nullable=True, default=1)
    agency = Column(String(20), ForeignKey("AGENCY.code"), nullable=True)

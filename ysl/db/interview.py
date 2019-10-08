from sqlalchemy import Column, String, ForeignKey, Integer, Date

from ysl.db import Base


class Interview(Base):
    __tablename__ = 'INTERVIEW_TB'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    interview_id = Column(Integer, primary_key=True)
    interview_name = Column(String(50), nullable=True)
    explanation = Column(String(100))
    start_day = Column(Date, nullable=True)
    end_day = Column(Date, nullable=True)
    status = Column(Integer, nullable=True, default=1)
    agency = Column(String(20), ForeignKey("AGENCY_TB.code"), nullable=True)

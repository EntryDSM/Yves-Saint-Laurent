from sqlalchemy import Column, Text, String

from ysl.db import Base


class Agency(Base):
    __tablename__ = 'AGENCY_TB'

    code = Column(String(20), primary_key=True)
    email = Column(String(50), nullable=True)
    pw = Column(String(200), nullable=True)
    name = Column(String(50), nullable=True)
    kind = Column(String(50), nullable=True)
    explanation = Column(Text, nullable=True)

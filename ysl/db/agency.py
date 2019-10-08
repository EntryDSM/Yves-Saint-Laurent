from sqlalchemy import Column, Text, String

from ysl.db import Base


class Agency(Base):
    __tablename__ = 'AGENCY_TB'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    code = Column(String(20), primary_key=True)
    email = Column(String(50), nullable=True)
    pw = Column(String(200), nullable=True)
    name = Column(String(50), nullable=True)
    kind = Column(String(50), nullable=True)
    explanation = Column(Text, nullable=True)

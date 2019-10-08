from sqlalchemy import Column, String, ForeignKey, Integer

from ysl.db import Base


class QuestionCheckList(Base):
    __tablename__ = 'QUESTION_CHECK_LIST_TB'
    _table_args_ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(Integer, primary_key=True)
    question = Column(Integer, ForeignKey("QUESTION_TB.id"), nullable=True)
    content = Column(String(100), nullable=True)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ysl.config.config import Config

engine = create_engine(Config.DATABASE_URL, encoding="utf-8", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


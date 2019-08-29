from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ysl.config.config import TestConfig

engine = create_engine(TestConfig.DATABASE_URL)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


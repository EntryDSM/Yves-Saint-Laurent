import os
from datetime import timedelta


class Config:
    SYSTEM_NAME = 'Yves-Saint-Laurent'




class TestConfig(Config):
    HOST = ''
    PORT = 5000
    DEBUG = True
    TESTING = True

    #DATABASE_URL = get_db_credential_url('test')
    #로컬테스트용 db url
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)



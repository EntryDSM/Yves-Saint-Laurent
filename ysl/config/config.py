from ysl.config.vault import get_db_credential_url


class Config:
    SYSTEM_NAME = 'Yves-Saint-Laurent'


class TestConfig(Config):
    HOST = ''
    PORT = 5000
    DEBUG = True
    TESTING = True

    DATABASE_URL = get_db_credential_url('test')
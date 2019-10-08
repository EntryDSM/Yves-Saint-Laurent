import os

from ysl.config.config import TestConfig, ProdConfig
from ysl.db import Base, engine
from ysl.app import create_app

Base.metadata.create_all(engine)
env = os.getenv('env')


if __name__ == '__main__':

    if env == 'test':
        app = create_app(TestConfig)
        app.run()
    elif env == 'prod':
        app = create_app(ProdConfig)
        app.run()

# -- coding: utf-8 --

import os

from ysl.config.config import TestConfig, ProdConfig
from ysl.db import Base, engine
from ysl.app import create_app

Base.metadata.create_all(engine)
env = os.getenv('env')


if __name__ == '__main__':

    if os.getenv('env') == 'test':
        app = create_app()
        app.run(host=TestConfig.HOST, port=TestConfig.PORT, debug=TestConfig.DEBUG)
    elif os.getenv('env') == 'prod':
        app = create_app()
        app.run(host=ProdConfig.HOST, port=ProdConfig.PORT, debug=ProdConfig.DEBUG)


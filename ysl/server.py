from ysl.app import create_app
from ysl.config.config import TestConfig

app = create_app(env='test')

if __name__ == '__main__':
    app.run(host=TestConfig.HOST,
            port=TestConfig.PORT
            )

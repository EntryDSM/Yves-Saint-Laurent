from ysl.app import create_app
from ysl.config import Config

app = create_app()

if __name__ == '__main__':
    app.run(host=Config.HOST,
            port=Config.PORT
            )

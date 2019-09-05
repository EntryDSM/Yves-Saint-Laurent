from ysl.app import create_app
from ysl.config.vault import tl


if __name__ == '__main__':
    app = create_app()

    app.run()

    #tl.start(block=True)

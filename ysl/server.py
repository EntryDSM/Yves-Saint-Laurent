from ysl.config.config import TestConfig
from ysl.config.vault import tl
from ysl.db import Base, engine

app = create_app()
Base.metadata.create_all(engine)

if __name__ == '__main__':

    app.run()

    #tl.start(block=True)

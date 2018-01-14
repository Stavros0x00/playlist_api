# The main entry point for running the api

from api import create_app
from api import scheduler

app = create_app()

scheduler.init_app(app)
scheduler.start()

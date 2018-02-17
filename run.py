# The main entry point for running the api
import logging
from logging.handlers import RotatingFileHandler

from api import create_app
from api import scheduler

app = create_app()

# Set up logging
handler = RotatingFileHandler('playlist_api.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(module)s.%(filename)s:%(lineno)d]'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

scheduler.init_app(app)
scheduler.start()

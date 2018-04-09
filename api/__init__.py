# Flask app generation and integration of used extensions
import os

from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from raven.contrib.flask import Sentry

from config import Config


# The ORM used to communicate with the db
db = SQLAlchemy()
# Used for database migrations
migrate = Migrate()
# Extension used for rate limiting
limiter = Limiter(key_func=get_remote_address)
# Extension used for running background jobs
scheduler = APScheduler()
# Exploit flask framework blueprint architecture-design
bp = Blueprint('api', __name__)
# Library used for logging errors in sentry service
sentry = Sentry()


def create_app(config_class=Config):
    """
    A callable for creating an application object. Needed for running the api or creating one
    when testing for example with the appropriate configurations.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # "Connect" extensions with the app and register blueprints
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    app.register_blueprint(bp)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URI']]) if app.config['ELASTICSEARCH_URI'] else None

    if not app.config.get('DEBUG'):
        sentry.init_app(app, dsn=os.getenv('SENTRY_KEY'))

    return app


from api import routes, models

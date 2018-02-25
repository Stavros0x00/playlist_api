# Flask app generation and integration of used extensions
import os

from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from raven.contrib.flask import Sentry

from config import Config


db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
scheduler = APScheduler()
bp = Blueprint('api', __name__)
sentry = Sentry()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # dsn=''
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    app.register_blueprint(bp)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URI']]) if app.config['ELASTICSEARCH_URI'] else None

    if not app.config.get('DEBUG'):
        sentry.init_app(app, dsn=os.getenv('SENTRY_KEY'))

    return app

#
# app = create_app()
#
# scheduler.init_app(app)
# scheduler.start()


from api import routes, models

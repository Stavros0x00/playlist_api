# Flask app generation and integration of used extensions

from elasticsearch import Elasticsearch
from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
scheduler = APScheduler()
bp = Blueprint('api', __name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URI']]) if app.config['ELASTICSEARCH_URI'] else None

    return app


app = create_app()
scheduler.init_app(app)
scheduler.start()


from api import routes, models

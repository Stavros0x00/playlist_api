# Flask app generation and integration of used extensions

from flask import Flask
from elasticsearch import Elasticsearch
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URI']]) if app.config['ELASTICSEARCH_URI'] else None

    return app


app = create_app()


from api import routes, models

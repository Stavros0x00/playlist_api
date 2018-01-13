# General api configuration. Includes production, development and testing configurations

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URI = os.environ.get('ELASTICSEARCH_URI')

    JOBS = [
        {
            'id': 'job1',
            'name': 'spotify_playlists',
            'func': 'api.tasks:update_spotify_playlists',
            'args': (),
            'trigger': 'interval',
            'hours': 24
        },
        {
            'id': 'job2',
            'name': 'sync_database_elastic',
            'func': 'api.tasks:sync_database_elastic',
            'args': (),
            'trigger': 'interval',
            'hours': 25
        }
    ]

    SCHEDULER_API_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


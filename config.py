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

    UNDIRECTED_GRAPH_LOCATION = 'api/pickled_files/undirected_graph.gpickle'
    DIRECTED_GRAPH_LOCATION = 'api/pickled_files/stochastic_graph.gpickle'

    K_NEIGHBORS_MODEL_LOCATION = 'api/pickled_files/k_neighbors.pickle'
    K_NEIGHBORS_MODEL_LOCATION_METADATA = 'api/pickled_files/k_neighbors_metadata.pickle'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    JOBS = [
        {
            'id': 'job1',
            'name': 'spotify_playlists',
            'func': 'api.tasks:update_spotify_playlists',
            'args': (),
            'trigger': 'cron',
            'hour': '19',
        },
        {
            'id': 'job2',
            'name': 'sync_database_elastic',
            'func': 'api.tasks:sync_database_elastic',
            'args': (),
            'trigger': 'cron',
            'hour': '23'
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

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

    UNDIRECTED_GRAPH_LOCATION = 'api/pickled_files/test_undirected_graph.gpickle'
    DIRECTED_GRAPH_LOCATION = 'api/pickled_files/test_stochastic_graph.gpickle'

    K_NEIGHBORS_MODEL_LOCATION = 'api/pickled_files/test_k_neighbors.pickle'
    K_NEIGHBORS_MODEL_LOCATION_METADATA = 'api/pickled_files/test_k_neighbors_metadata.pickle'

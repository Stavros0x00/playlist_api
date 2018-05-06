#!/usr/bin/env python
# Script for sync between elastic and database

import logging
logger = logging.getLogger('api')

# This is needed for running the scripts from the terminal (without a scheduler)
import sys
sys.path.append('/home/playlistapi/playlist_api/')

from run import app
from api import create_app
from api.models import Track


def sync_database_elastic():
    """
    Syncs data from database to elasticsearch
    """
    logger.info('Started syncing database with elastic')
    with app.app_context():
        Track.reindex()


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        sync_database_elastic()

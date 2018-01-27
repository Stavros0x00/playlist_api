#!/usr/bin/env python
# Script for sync between elastic and database

# This is needed for running the scripts without a sheduler
import sys
sys.path.append('/home/playlist_api/')

from run import app
from api import create_app
from api.models import Track


def sync_database_elastic():
    """
    Syncs data from database to elasticsearch
    """
    with app.app_context():
        Track.reindex()


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        sync_database_elastic()

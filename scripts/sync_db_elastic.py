#!/usr/bin/env python
# Script for sync between elastic and database

# To be removed?
import sys
sys.path.append('/home/work/Dropbox/eap/diplomatikh/source/playlist_api/')

from api import create_app
from api.models import Track


def sync_database_elastic():
    """
    Syncs data from database to elasticsearch for having updated data
    when searching for tracks
    """
    Track.reindex()


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        sync_database_elastic()

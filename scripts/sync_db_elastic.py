#!/usr/bin/env python
# Script for sync between elastic and database


from run import app
from api.models import Track


def sync_database_elastic():
    """
    Syncs data from database to elasticsearch
    """
    with app.app_context():
        Track.reindex()

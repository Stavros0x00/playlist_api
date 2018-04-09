# Pytest configuration file for this directory. Creates acousticbrainz, spotify, lastfm and the whole app (api) flask object
# objects used in the tests

import pytest
from api import create_app, db
from config import TestingConfig
from api.external import AcousticBrainz
from api.external.spotify import sp
from api.external.lastfm import network


@pytest.fixture(scope='module')
def acoustic_brainz_object():
    """
    Setups the AcousticBrainz object.
    """
    return AcousticBrainz()

@pytest.fixture(scope='module')
def spotify_object():
    """
    Setups the Spotify object.
    """
    return sp


@pytest.fixture(scope='module')
def lastfm_object():
    """
    Setups the Last.fm object.
    """
    return network



@pytest.fixture(scope='module')
def app(request):
    """
    Setups the Flask app-api object.
    """
    app = create_app(config_class=TestingConfig)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)

    return app

# Pytest configuration file for this directory. Creates acousticbrainz, spotify and the whole app (api) flask object
# objects used in the tests

import pytest
from api import create_app
from api.auth import sp
from config import TestingConfig
from api.external import AcousticBrainz


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
def app():
    """
    Setups the Flask app-api object.
    """
    app = create_app(config_class=TestingConfig)
    return app

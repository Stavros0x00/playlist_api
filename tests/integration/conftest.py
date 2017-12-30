# Pytest configuration file for this directory. Creates acousticbrainz and spotify
# objects used in the tests

import pytest
from api.auth import sp
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

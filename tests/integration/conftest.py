import pytest
from api.external import AcousticBrainz


@pytest.fixture(scope='module')
def acoustic_brainz_object():
    """
    Setup the AcousticBrainz object.
    """
    return AcousticBrainz()

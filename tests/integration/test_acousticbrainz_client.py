from collections import namedtuple

import pytest


# Test data
EXAMPLE_MBID = 'aaf1f9ea-cd47-450c-9c79-6e76fedb1d84'  # Damon Albarn - Heavy Seas Of Love
EXAMPLE_ARTIST = 'Damon Albarn'
EXAMPLE_TRACK = 'Heavy Seas Of Love'

ExpectedForTrackData = namedtuple('ExpectedForTrackData', ['type', 'level_response_key', 'artist'])


@pytest.mark.parametrize('mbid, level, document_number, expected', [
    (EXAMPLE_MBID, 'high-level', 0, ExpectedForTrackData(dict, 'highlevel', 'Damon Albarn')),
    (EXAMPLE_MBID, 'low-level', 0, ExpectedForTrackData(dict, 'lowlevel', 'Damon Albarn')),
    (EXAMPLE_MBID, 'low-level', 1, ExpectedForTrackData(dict, 'lowlevel', 'Damon Albarn'))
])
def test_get_track_data(acoustic_brainz_object, mbid, level, document_number, expected):
    track_data = acoustic_brainz_object.get_track_data(mbid, level, document_number=document_number)
    assert isinstance(track_data, expected.type)
    assert expected.level_response_key in track_data
    assert track_data['metadata']['tags']['artist']


ExpectedForMbid = namedtuple('ExpectedForMbid', ['type', 'mbid'])


@pytest.mark.parametrize('artist, track, expected', [
    (EXAMPLE_ARTIST, EXAMPLE_TRACK, ExpectedForMbid(dict, 'aaf1f9ea-cd47-450c-9c79-6e76fedb1d84')),
])
def test_get_mbid(acoustic_brainz_object, artist, track, expected):
    recordings = acoustic_brainz_object.get_mbid(artist, track,)
    assert isinstance(recordings, expected.type)
    assert recordings['recording-list'][0]['id'] == expected.mbid

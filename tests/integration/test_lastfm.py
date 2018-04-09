
def test_lastfm_connection(lastfm_object):
    track = lastfm_object.get_track('Damon Albarn', 'Heavy Seas of Love')
    assert track.artist.name == 'Damon Albarn'
    assert track.title == 'Heavy Seas of Love'

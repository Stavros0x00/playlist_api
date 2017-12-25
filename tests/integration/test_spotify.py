urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'


def test_spotify_auth(spotify_object):
    artist = spotify_object.artist(urn)
    assert artist['name'] == 'Weezer'

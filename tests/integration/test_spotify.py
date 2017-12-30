urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'


def test_spotify_connection(spotify_object):
    artist = spotify_object.artist(urn)
    assert artist['name'] == 'Weezer'

from api.external.spotify import get_and_check_seed_recommendations, get_track_genres


def test_spotify_connection(spotify_object):
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
    artist = spotify_object.artist(urn)

    assert artist['name'] == 'Weezer'


def test_get_and_check_seed_recommendations(graph_tracks):
    spotify_id = '6qG8MsR8UlrJi1935ovoAr'

    spotify_seed, graph_tracks = get_and_check_seed_recommendations(spotify_id, graph_tracks)

    assert isinstance(spotify_seed, list)
    assert isinstance(graph_tracks, list)
    assert isinstance(graph_tracks[0], dict)


def test_get_track_genres():
    spotify_id = '6qG8MsR8UlrJi1935ovoAr'

    genres = get_track_genres(spotify_id)

    assert isinstance(genres, list)
    assert 'black thrash' in genres  # This could change. Leave it for now

from api.external.spotify import get_and_check_seed_recommendations, get_track_genres


def test_spotify_connection(spotify_object):
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
    artist = spotify_object.artist(urn)

    assert artist['name'] == 'Weezer'


def test_get_and_check_seed_recommendations():
    # TODO: Make a better case and refactor the function.
    graph_tracks = [{'id': 26756, 'artist': 'Kvelertak', 'name': 'Nattesferd', 'spotify_id': '6qG8MsR8UlrJi1935ovoAr',
                     'preview_url': 'https://p.scdn.co/mp3-preview/7239f74e280a36ff70f7e2ef13dd6970831d6827?cid=0c0bb28de56d49d3b925f9755a289113',
                     'lastfm_tags': ['Black n Roll', 'kvelertak', 'black metal', 'hardcore', 'stoner metal'],
                     'score': 3.061528206093548},
                    {'id': 36317, 'artist': 'Burzum', 'name': 'Dunkelheit', 'spotify_id': '5v3TSHYm8BzbON2u6QBEG7',
                     'preview_url': 'https://p.scdn.co/mp3-preview/7a3ad6a36ce0b47713e287a1838c67ea08f26278?cid=0c0bb28de56d49d3b925f9755a289113',
                     'lastfm_tags': ['black metal', 'ambient black metal', 'dark ambient', 'Norwegian Black Metal',
                                     'True Norwegian Black Metal'], 'score': 1.4426950408889634}]

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

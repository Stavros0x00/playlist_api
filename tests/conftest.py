# Pytest configuration file for this directory. Creates acousticbrainz, spotify, lastfm and the whole app (api) flask object
# objects used in the tests. Also creates sample rows and relationships in db and elasticsearch index to use as dummy data.

import os

import pytest
from api import create_app, db
from config import TestingConfig
from api.external.acousticbrainz import AcousticBrainz
from api.external.spotify import get_spotify_object
from api.external.lastfm import network
from api.models import Playlist, PlaylistToTrack, Track, TrackFeatures


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
    return get_spotify_object()


@pytest.fixture(scope='module')
def spotify_user_auth_object():
    """
    Setups the Spotify object with user based auth.
    """
    return get_spotify_object(with_oauth=True)


@pytest.fixture(scope='module')
def lastfm_object():
    """
    Setups the Last.fm object.
    """
    return network


@pytest.fixture(scope='session')
def app(request):
    """
    Setups the Flask app-api object.
    """
    app = create_app(config_class=TestingConfig)

    # Create an application context
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    # Set up test database
    setup_db_rows(db)

    # Set up test elasticsearch index
    if not app.elasticsearch.indices.exists('test_tracks'):
        app.elasticsearch.indices.create(index='test_tracks')

    # Teardown test pickled files, test database, test elasticsearch
    def teardown():
        db.session.remove()
        db.drop_all()

        os.remove(app.config['UNDIRECTED_GRAPH_LOCATION'])
        os.remove(app.config['DIRECTED_GRAPH_LOCATION'])
        os.remove(app.config['K_NEIGHBORS_MODEL_LOCATION'])
        os.remove(app.config['K_NEIGHBORS_MODEL_LOCATION_METADATA'])

        if app.elasticsearch.indices.exists('test_tracks'):
            app.elasticsearch.indices.delete(index='test_tracks', ignore=[400, 404])

        app_context.pop()

    request.addfinalizer(teardown)

    return app


def setup_db_rows(db):
    """
    Setups some rows in the db tables, to use them in all the tests
    """
    # Add tracks
    track1 = Track(spotify_id='07HF5tFmwh6ahN93JC6LmE',
                   artist='Kyuss',
                   name='Space Cadet',
                   spotify_artist_genres=['modern rock', 'neo-psychedelic'])  # Here the genres are just an example
    db.session.add(track1)
    db.session.commit()

    track2 = Track(spotify_id='6QgjcU0zLnzq5OrUoSZ3OK',
                   artist='Portugal. The Man',
                   name='Feel It Still',
                   spotify_artist_genres=['modern rock', 'neo-psychedelic'])
    db.session.add(track2)
    db.session.commit()

    track3 = Track(spotify_id='1i8oOEZKBzaxnEmcZYAYCQ',
                   artist='Frenic',
                   name='Travel Alone',
                   spotify_artist_genres=['modern rock', 'neo-psychedelic'])  # Here the genres are just an example
    db.session.add(track3)
    db.session.commit()

    # Add playlists
    playlist = Playlist(spotify_id='testrandom123',
                        playlist_user='testrandomuser')
    db.session.add(playlist)

    # Add track features. For now it takes the original features from spotify
    # Manipulate time signature for avoiding division by zero in such a small sample
    sp = get_spotify_object()
    audio_features = sp.audio_features('1i8oOEZKBzaxnEmcZYAYCQ')[0]
    track_features = TrackFeatures(
        track_id=track3.id,
        acousticness=audio_features['acousticness'],
        danceability=audio_features['danceability'],
        duration_ms=audio_features['duration_ms'],
        energy=audio_features['energy'],
        instrumentalness=audio_features['instrumentalness'],
        key=audio_features['key'],
        liveness=audio_features['liveness'],
        loudness=audio_features['loudness'],
        mode=audio_features['mode'],
        speechiness=audio_features['speechiness'],
        tempo=audio_features['tempo'],
        time_signature=1,  # Temp values for not breaking with zero division error with such a small number of tracks
        valence=audio_features['valence'],
    )
    db.session.add(track_features)
    db.session.commit()

    sp = get_spotify_object()
    audio_features = sp.audio_features('6QgjcU0zLnzq5OrUoSZ3OK')[0]
    track_features = TrackFeatures(
        track_id=track2.id,
        acousticness=audio_features['acousticness'],
        danceability=audio_features['danceability'],
        duration_ms=audio_features['duration_ms'],
        energy=audio_features['energy'],
        instrumentalness=audio_features['instrumentalness'],
        key=audio_features['key'],
        liveness=audio_features['liveness'],
        loudness=audio_features['loudness'],
        mode=audio_features['mode'],
        speechiness=audio_features['speechiness'],
        tempo=audio_features['tempo'],
        time_signature=2,  # Temp values for not breaking with zero division error with such a small number of tracks
        valence=audio_features['valence'],
    )
    db.session.add(track_features)
    db.session.commit()

    sp = get_spotify_object()
    audio_features = sp.audio_features('07HF5tFmwh6ahN93JC6LmE')[0]
    track_features = TrackFeatures(
        track_id=track1.id,
        acousticness=audio_features['acousticness'],
        danceability=audio_features['danceability'],
        duration_ms=audio_features['duration_ms'],
        energy=audio_features['energy'],
        instrumentalness=audio_features['instrumentalness'],
        key=audio_features['key'],
        liveness=audio_features['liveness'],
        loudness=audio_features['loudness'],
        mode=audio_features['mode'],
        speechiness=audio_features['speechiness'],
        tempo=audio_features['tempo'],
        time_signature=audio_features['time_signature'],
        valence=audio_features['valence'],
    )
    db.session.add(track_features)
    db.session.commit()

    # Add track to playlist relationships
    tracks = [track1, track2, track3]
    for index, track in enumerate(tracks):
        playlist_to_track = PlaylistToTrack(order_in_playlist=index)
        playlist_to_track.track = track
        with db.session.no_autoflush:
            playlist.tracks.append(playlist_to_track)
        db.session.commit()


@pytest.fixture(scope='session')
def graph_tracks():
    """Sample of suggested from graph tracks returned in the similar endpoint.
    Used across the tests"""
    graph_tracks = [{'id': 26756, 'artist': 'Kvelertak', 'name': 'Nattesferd', 'spotify_id': '6qG8MsR8UlrJi1935ovoAr',
                     'preview_url': 'https://p.scdn.co/mp3-preview/7239f74e280a36ff70f7e2ef13dd6970831d6827?cid=0c0bb28de56d49d3b925f9755a289113',
                     'lastfm_tags': ['Black n Roll', 'kvelertak', 'black metal', 'hardcore', 'stoner metal'],
                     'score': 3.061528206093548},
                    {'id': 36317, 'artist': 'Burzum', 'name': 'Dunkelheit', 'spotify_id': '5v3TSHYm8BzbON2u6QBEG7',
                     'preview_url': 'https://p.scdn.co/mp3-preview/7a3ad6a36ce0b47713e287a1838c67ea08f26278?cid=0c0bb28de56d49d3b925f9755a289113',
                     'lastfm_tags': ['black metal', 'ambient black metal', 'dark ambient', 'Norwegian Black Metal',
                                     'True Norwegian Black Metal'], 'score': 1.4426950408889634}]
    return graph_tracks

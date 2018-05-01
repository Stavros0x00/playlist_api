# Pytest configuration file for this directory. Creates acousticbrainz, spotify, lastfm and the whole app (api) flask object
# objects used in the tests. Also creates sample rows and relationships in db to use as dummy data.

import os

import pytest
from api import create_app, db
from config import TestingConfig
from api.external import AcousticBrainz
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

    setup_db_rows(db)

    def teardown():
        db.session.remove()
        db.drop_all()
        os.remove(app.config['UNDIRECTED_GRAPH_LOCATION'])
        os.remove(app.config['DIRECTED_GRAPH_LOCATION'])
        os.remove(app.config['K_NEIGHBORS_MODEL_LOCATION'])
        os.remove(app.config['K_NEIGHBORS_MODEL_LOCATION_METADATA'])
        app_context.pop()

    request.addfinalizer(teardown)

    return app


def setup_db_rows(db):
    """
    Setups some rows in the db tables, to use them in all the tests
    """
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

    playlist = Playlist(spotify_id='testrandom123',
                        playlist_user='testrandomuser')
    db.session.add(playlist)

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

    tracks = [track1, track2, track3]
    for index, track in enumerate(tracks):
        playlist_to_track = PlaylistToTrack(order_in_playlist=index)
        playlist_to_track.track = track
        with db.session.no_autoflush:
            playlist.tracks.append(playlist_to_track)
        db.session.commit()

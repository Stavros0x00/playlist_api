"""Gets track features from spotify. https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/"""

import sys
sys.path.append('/home/playlistapi/playlist_api/')


from api import create_app, db
from api.external.spotify import get_spotify_object
from api.models import Track, TrackFeatures
from api.utils import chunks


sp = get_spotify_object()


def get_tracks_features():
    """Gets track features for a list of tracks in the db from spotify or only one track if string passed.
    Saves the features in the db with the appropriate relationships.
    """
    # Get all tracks from the db. For performance issues this
    # script must be run on the first server setup with a
    # small number of tracks.
    # Optimize appropriately if otherwise
    tracks = db.session.query(Track.id, Track.spotify_id).all()

    # Iterate over 50 tracks at the time, cause 50 is the max for the spotify function
    for tracks in chunks(tracks, 50):
        # Create a dict with spotify_ids as keys and track_ids as values for better handling
        tracks_dict = {track.spotify_id: track.id for track in tracks}
        # Get spotify audio features
        tracks_audio_features = sp.audio_features(tracks_dict.keys())

        for track_audio_features in tracks_audio_features:
            # Add the features in the db
            track_features = TrackFeatures(
                track_id=tracks_dict[track_audio_features['id']],
                acousticness=track_audio_features['acousticness'],
                danceability=track_audio_features['danceability'],
                duration_ms=track_audio_features['duration_ms'],
                energy=track_audio_features['energy'],
                instrumentalness=track_audio_features['instrumentalness'],
                key=track_audio_features['key'],
                liveness=track_audio_features['liveness'],
                loudness=track_audio_features['loudness'],
                mode=track_audio_features['mode'],
                speechiness=track_audio_features['speechiness'],
                tempo=track_audio_features['tempo'],
                time_signature=track_audio_features['time_signature'],
                valence=track_audio_features['valence'],
            )

            db.session.add(track_features)
            db.session.commit()


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        db.init_app(app)
        audio_features = get_tracks_features()

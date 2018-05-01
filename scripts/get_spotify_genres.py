"""Gets track genres from spotify. """
import sys
sys.path.append('/home/playlistapi/playlist_api/')


from api import create_app, db
from api.external.spotify import get_spotify_object
from api.models import Track
from api.utils import chunks


sp = get_spotify_object()


# TODO: See if you can make it faster
def get_tracks_genres():
    """Gets track genres for all tracks in the db from spotify.
    Spotify gives genres, if available, for artists.
    Stores them as lower case in the db tracks table
    """

    tracks = db.session.query(Track.spotify_id).filter(Track.spotify_artist_genres == None).all()

    # Iterate over 50 tracks at the time, cause 50 is the max for the spotify function for tracks
    for tracks in chunks(tracks, 50):
        spotify_tracks = sp.tracks([track.spotify_id for track in tracks])

        for spotify_track in spotify_tracks['tracks']:
            # For every artist get genres
            spotify_artists = sp.artists([artist['id'] for artist in spotify_track['artists']])

            track_artist_genres = [genre.lower() for artist in spotify_artists['artists']
                                   for genre in artist['genres']]

            try:
                # Store them in the db
                db_track = db.session.query(Track).filter(Track.spotify_id == spotify_track['id']).first()
                if not db_track:
                    continue

                print(db_track.id, db_track.spotify_id)
                print(track_artist_genres)

                db_track.spotify_artist_genres = track_artist_genres
                db.session.commit()
            except Exception as ex:
                print("integrity error..+++++++++++++++++++++++++++++++")
                print(ex)
                db.session.rollback()


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        db.init_app(app)
        get_tracks_genres()

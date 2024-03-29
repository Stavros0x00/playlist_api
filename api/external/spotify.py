# spotify api configurations
import os

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

from api import db, sentry
from api.models import Track
from api.utils import send_email


def get_spotify_oauth():
    """
    Get a user auth object
    """
    return SpotifyOAuth(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                        client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                        redirect_uri='http://localhost').refresh_access_token(os.environ.get('SPOTIFY_REFRESH_TOKEN'))


def get_client_crents_auth():
    """
    Get a simple auth object with only client_id and client_secret for non
    user auth endpoints
    """
    return SpotifyClientCredentials()


def get_spotify_object(with_oauth=False):
    """
    Dynamically return a spotify object when needed. with_oauth = true returns
    user auth object.
    """
    if with_oauth:
        sp = spotipy.Spotify(auth=get_spotify_oauth()['access_token'])
    else:
        sp = spotipy.Spotify(client_credentials_manager=get_client_crents_auth())
    return sp


def get_and_check_seed_recommendations(spotify_id, graph_tracks):
    """Gets a spotify id and and the graph suggested tracks and queries the spotify seed recommendations api.
    Then checks if we have returned ids in the db and common spotify_ids with the
    suggested from the graph tracks. If we have common then boosts the appropriate score.
    Then returns the modified graph suggested items and the suggested from spotify tracks that we have in the db already."""
    sp = get_spotify_object()
    seed_recommendations = sp.recommendations(seed_tracks=[spotify_id], limit=100)

    graph_spotify_ids = {track['spotify_id'] for track in graph_tracks}
    seed_recommendations_for_result = []
    edited_score = False

    for rec in seed_recommendations['tracks']:
        # Get track from the db if exists
        track = db.session.query(Track).filter(Track.spotify_id == rec['id']).first()

        if not track:
            continue

        if rec['id'] in graph_spotify_ids:
            # If we have common spotify results and graph results boost the appropriate score
            for d in graph_tracks:
                if d['spotify_id'] == rec['id']:
                    d['score'] += 1  # TODO: Find a better formula for boosting the score
                    edited_score = True
                    print("We have common!!", rec['id'])

        else:
            # Removing the else condition here is a good way of checking how well the graphs suggestions works
            # compared to spotify suggestions. Common suggestions indicate
            if rec['id'] == spotify_id:
                continue  # Don't return our seed track in seed suggestions from spotify
            seed_recommendations_for_result.append(track.to_dict())

    if edited_score:
        # Sort the tracks with the new score
        graph_tracks_list = sorted(graph_tracks, key=lambda k: k['score'], reverse=True)
    else:
        graph_tracks_list = graph_tracks

    return seed_recommendations_for_result, graph_tracks_list


def get_track_genres(spotify_id):
    """Gets track genres for a track.
    Spotify gives genres, if available, for artists.
    Stores them as lower case in the db tracks table
    """
    sp = get_spotify_object()

    spotify_track = sp.track(spotify_id)

    # For every artist get genres
    spotify_artists = sp.artists([artist['id'] for artist in spotify_track['artists']])

    track_artist_genres = [genre.lower() for artist in spotify_artists['artists']
                           for genre in artist['genres']]

    return track_artist_genres


def create_spotify_playlist(spotify_ids, seed_track):
    """Gets a list of spotify_ids, a seed_track and creates a playlist on spotify with the name of the seed_track.
    Needs user based auth. Returns the metadata of the playlist needed for example for populating the
    appropriate endpoint json response."""
    try:
        sp = get_spotify_object(with_oauth=True)
        playlist = sp.user_playlist_create(user=os.environ.get('SPOTIFY_USERNAME'), name=seed_track.name)

        # Add tracks to playlist
        sp.user_playlist_add_tracks(user=os.environ.get('SPOTIFY_USERNAME'), playlist_id=playlist['id'], tracks=spotify_ids)
        # Add link and id to result
        return {'spotify_id': playlist['id'],
                'url': playlist['external_urls']['spotify']}
    except SpotifyException:
        # send email and log in sentry if spotify exception
        sentry.captureException()
        send_email(os.environ.get('NOTIFICATIONS_EMAIL'),
                   'Possible spotify refresh token invalidation. Check errors and sentry')

# spotify api configurations
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

from api import db
from api.models import Track


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

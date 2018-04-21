# spotify api configurations
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


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

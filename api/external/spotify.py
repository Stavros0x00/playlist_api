# spotify api configurations
import os

import spotipy
from spotipy.oauth2 import  SpotifyOAuth

# Create Spotify client object for connecting to the
# spotify web api with credentials stored as environment variables
auth_token = SpotifyOAuth(client_id=os.environ.get('SPOTIPY_CLIENT_ID'), client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'), redirect_uri='http://localhost').refresh_access_token(os.environ.get('SPOTIFY_REFRESH_TOKEN'))
sp = spotipy.Spotify( auth=auth_token['access_token'])


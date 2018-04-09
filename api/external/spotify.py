# spotify api configurations
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create Spotify client object for connecting to the
# spotify web api with credentials stored as environment variables
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Last.fm api configurations
import os

import pylast

# Create the main authorized object for communicating with the last.fm api
network = pylast.LastFMNetwork(api_key=os.environ.get('LAST_FM_API_KEY'),
                               api_secret=os.environ.get('LAST_FM_SHARED_SECRET'))

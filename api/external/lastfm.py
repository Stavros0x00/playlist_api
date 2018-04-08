import os

import pylast


network = pylast.LastFMNetwork(api_key=os.environ.get('LAST_FM_API_KEY'),
                               api_secret=os.environ.get('LAST_FM_SHARED_SECRET'))

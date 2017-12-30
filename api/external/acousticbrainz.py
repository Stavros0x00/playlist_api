import musicbrainzngs
import requests
from time import sleep


class AcousticBrainz(object):
    """
    A simple client for getting data from the AcousticBrainz Api and MusicBrainz API
    """
    def __init__(self):
        # Initialize acousticbrainz client object
        self.base_url = 'https://acousticbrainz.org/api/v1/'
        self.sleep_time = 0  # Needed for having some rate limiting

    def get_mbid(self, artist, track):
        """
        Get MusicBrainz ID from track
        """
        # TODO: Create appropriate user agent when code is public
        # TODO: Handle rate limit error response
        musicbrainzngs.set_useragent('playlist_api', '0.1')
        return musicbrainzngs.search_recordings(artist=artist, recording=track)

    def get_track_data(self, mbid, level, document_number=0, waiting_for=0.25):
        """
        Gets acoustic brainz data from a track with a musicbrainz id
        """
        params = {'n': document_number} if document_number else None
        r = requests.get(self.base_url + mbid + '/' + level, params=params)

        # Config the sleep time in case of successive requests
        sleep(self.sleep_time)
        self.sleep_time = waiting_for
        return r.json()



# For testing-playing purposes, TODO: remove it later
if __name__ == '__main__':
    a = AcousticBrainz()
    EXAMPLE_MBID = 'aaf1f9ea-cd47-450c-9c79-6e76fedb1d84'  # Damon Albarn - Heavy Seas Of Love
    from pprint import pprint as pp
    pp(a.get_mbid(artist="Clutch", track="The Regulator")['recording-list'][0])

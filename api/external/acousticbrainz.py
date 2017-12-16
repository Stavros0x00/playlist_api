import musicbrainzngs
import requests
from time import sleep

# TODO: Endpoints for datasets
# TODO: Docs and readme

class AcousticBrainz(object):

    def __init__(self):
        self.base_url = 'https://acousticbrainz.org/api/v1/'
        self.sleep_time = 0

    def get_mbid(self, artist, track):
        # TODO: explore the rate limiting quota
        """

        :param artist:
        :param track:
        :param limit:
        :return:
        """
        # TODO: change email?
        musicbrainzngs.set_useragent('pyacousticbrainz', '0.1', contact='stavanto@gmail.com')
        return musicbrainzngs.search_recordings(artist=artist, recording=track)

    def get_track_data(self, mbid, level, document_number=0, waiting_for=0.25):
        # TODO: implement the low level for multiple mbids functionality
        """

        :param mbid:
        :param level:
        :param document_number:
        :param waiting_for:
        :return:
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

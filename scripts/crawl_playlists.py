# Script for crawling featured spotify playlists and also getting chosen playlist.net playlists

from api.auth import sp

# For testing-playing purposes, TODO: remove it later
if __name__ == '__main__':
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
    artist = sp.artist(urn)
    print(artist)

#!/usr/bin/env python
# Script for crawling featured spotify playlists and also getting chosen playlist.net playlists

# To be removed?
import sys
sys.path.append('/home/work/Dropbox/eap/diplomatikh/source/playlist_api/')

from api import db, create_app
from api.auth import sp
from api.models import Track, Playlist

# TODO: make it more modular. You do the same thing again and again
# TODO: see possible performance issues. Many O(n^2) operations here


def get_featured_playlists():
    """
    Gets featured spotify playlists. By default gets the current for
    american english locale and country
    """
    # TODO: Handle posible errors
    playlists = []
    limit = 50  # The max
    result = sp.featured_playlists(limit=limit)

    if 'playlists' in result:
        playlists.extend(result['playlists']['items'])

        while result['playlists']['next']:
            result = sp.next(result['playlists'])
            playlists.extend(result['playlists']['items'])

    return playlists


def get_categories():
    """
    Gets all official spotify playlists categories
    """
    # TODO: Handle posible errors
    categories = []
    limit = 50  # The max
    result = sp.categories(limit=limit)

    if 'categories' in result:
        categories.extend(result['categories']['items'])

        while result['categories']['next']:
            result = sp.next(result['categories'])
            categories.extend(result['categories']['items'])

    return categories


def get_categories_playlists():
    """
    Gets all official spotify playlists from oficial categories
    """
    # TODO: Handle posible errors
    categories = get_categories()
    categories_ids = [category['id'] for category in categories]

    playlists = []
    limit = 50  # The max
    for category_id in categories_ids:
        if category_id == 'comedy':  # Don't keep comedy tracks
            continue

        result = sp.category_playlists(category_id=category_id, limit=limit)

        if 'playlists' in result:
            playlists.extend(result['playlists']['items'])

            while result['playlists']['next']:
                result = sp.next(result['playlists'])
                playlists.extend(result['playlists']['items'])

    return playlists



def update_spotify_playlists():
    """
    Gets spotify playlists and updates the database
    """
    featured_playlists = get_featured_playlists()
    categories_playlists = get_categories_playlists()

    playlists = featured_playlists + categories_playlists
    for playlist in playlists:
        spotify_id = playlist['id']
        playlist_user = playlist['owner']['id']
        playlist_exists = Playlist.query.filter_by(spotify_id=spotify_id).first()

        if not playlist_exists:
            p = Playlist()
            p.spotify_id = spotify_id
            p.playlist_user = playlist_user
            db.session.add(p)
            db.session.commit()

            update_tracks_from_playlist(p)
        else:
            print("We have it!")
        print(spotify_id)


def get_plalist_tracks(playlist):
    """
    Gets tracks from a spotify playlist
    """
    # TODO: Handle posible errors
    tracks = []
    limit = 50  # The max
    result = sp.user_playlist_tracks(playlist.playlist_user, playlist_id=playlist.spotify_id)

    if 'items' in result:
        tracks.extend(result['items'])

        while result['next']:
            result = sp.next(result)
            tracks.extend(result['items'])

    return tracks

def update_tracks_from_playlist(playlist):
    """
    Populates tracks database table from given playlists.
    Also update the relationship between them.
    """
    # db_playlists = Playlist.query.all()
    # from pdb import set_trace
    # set_trace()
    # Add track
    # for playlist in db_playlists:
    playlist_tracks = get_plalist_tracks(playlist)
    for track in playlist_tracks:
        spotify_id = track['track']['id']
        # Here i create a string of the names of the artists
        # TODO: Store different data structure or create another artists table
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])

        track_exists = Track.query.filter_by(spotify_id=spotify_id).first()

        if not track_exists:
            t = Track()
            t.spotify_id = spotify_id
            t.name = track['track']['name']
            t.artist = artists
            db.session.add(t)
            db.session.commit()

            # Add relathionship to the association table
            t.playlists.append(playlist)
            db.session.commit()
        else:
            # Add relathionship to the association table
            track_exists.playlists.append(playlist)
            db.session.commit()
            print("We have it!")
            # import pdb
            # pdb.set_trace()

        print(spotify_id)


# To be removed
if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        db.init_app(app)
        update_spotify_playlists()
        # update_tracks_from_playlist()
    # playlists = get_featured_playlists()
    # categories = get_categories()
    # categories_playlists = get_categories_playlists()
    # from pdb import set_trace
    # set_trace()

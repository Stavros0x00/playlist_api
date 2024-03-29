#!/usr/bin/env python
# Script for crawling featured spotify playlists, getting
# lastfm tags for every track and creating or updating graphs needed

import logging
logger = logging.getLogger('api')

import sys
sys.path.append('/home/playlistapi/playlist_api/')

from pylast import WSError
from spotipy import SpotifyException

from api import db, create_app
from api.external.lastfm import network as lastfm_obj
from api.external.spotify import get_spotify_object, get_track_genres
from api.k_neighbors import build_model
from api.models import Track, Playlist, PlaylistToTrack, TrackFeatures
from run import app

sp = get_spotify_object()


def get_featured_playlists():
    """
    Gets featured spotify playlists. By default gets the current for
    american english locale and country
    """
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
    categories = get_categories()
    categories_ids = [category['id'] for category in categories]

    playlists = []
    limit = 50  # The max
    for category_id in categories_ids:
        if category_id == 'comedy':  # Don't keep comedy tracks
            continue
        try:
            result = sp.category_playlists(category_id=category_id, limit=limit)
        except SpotifyException:
            continue
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
    logger.info('Started updating playlists from spotify')

    with app.app_context():
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

        # Update undirected graph
        from api.graph import create_undirected_graph, transform_to_stochastic
        G = create_undirected_graph()
        transform_to_stochastic(G)
        db.session.close()


def get_playlist_tracks(playlist):
    """
    Gets tracks from a spotify playlist
    """
    tracks = []
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

    playlist_tracks = get_playlist_tracks(playlist)
    for index, track in enumerate(playlist_tracks):
        spotify_id = track['track']['id']

        # Here we create a string of the names of the artists
        artists = ", ".join([artist['name'] for artist in track['track']['artists']])
        if not spotify_id or not track['track']['name'] or not artists:
            print("-================No spotify id or name or artist==========")
            continue
        track_exists = Track.query.filter_by(spotify_id=spotify_id).first()

        playlist_to_track = PlaylistToTrack(order_in_playlist=index)
        if not track_exists:
            t = Track()
            t.spotify_id = spotify_id
            t.name = track['track']['name']
            t.artist = artists
            t.preview_url = track['track']['preview_url']
            t.spotify_artist_genres = get_track_genres(spotify_id)

            try:
                t.lastfm_tags = [tag.item.name for tag in lastfm_obj.get_track(track['track']['artists'][0]['name'],
                                                                               track['track']['name']
                                                                               ).get_top_tags(limit=5)]
                print(t.lastfm_tags)
            except WSError:
                pass

            # Add relathionship to the association table
            playlist_to_track.track = t
            with db.session.no_autoflush:
                playlist.tracks.append(playlist_to_track)
            db.session.flush()

            # Add track features in the db
            audio_features = sp.audio_features(t.spotify_id)[0]
            track_features = TrackFeatures(
                track_id=t.id,
                acousticness=audio_features['acousticness'],
                danceability=audio_features['danceability'],
                duration_ms=audio_features['duration_ms'],
                energy=audio_features['energy'],
                instrumentalness=audio_features['instrumentalness'],
                key=audio_features['key'],
                liveness=audio_features['liveness'],
                loudness=audio_features['loudness'],
                mode=audio_features['mode'],
                speechiness=audio_features['speechiness'],
                tempo=audio_features['tempo'],
                time_signature=audio_features['time_signature'],
                valence=audio_features['valence'],
            )
            db.session.add(track_features)
            db.session.flush()

        else:
            # Add relathionship to the association table
            try:
                playlist_to_track.track = track_exists
                with db.session.no_autoflush:
                    playlist.tracks.append(playlist_to_track)
                db.session.flush()
                print("=================================")
            except Exception as ex:
                # Handle same songs to the same playlist..
                print("integrity error..+++++++++++++++++++++++++++++++")
                print(ex)
                db.session.rollback()
            print("We have it!")

        print(spotify_id)


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        db.init_app(app)
        update_spotify_playlists()
        build_model()

#!/usr/bin/env python

"""Evaluation related functions of the playlist API results"""
# TODO: Refactor everything in this module. This is just a quick evaluation test

from collections import defaultdict
import sys
sys.path.append('/home/playlistapi/playlist_api/')

from api import db, create_app
from api.external.spotify import get_spotify_object
from api.graph import get_shortest_neigbors
from api.models import Track


sp = get_spotify_object()


def music_track_genre_evaluation():
    """
    Checks the intersection of genre sets of seed and 4 more graph suggestions.
    Sample limit songs with all suggestions having a genre set
    """
    # The sample upper limit
    SAMPLE_LIMIT = 1000

    # Limit counter
    counter = 0

    # The dictionary with holds percent of genres intersections for every track
    track_percent = defaultdict(list)

    # Get a sample of SAMPLE_LIMIT of tracks with at least 4 suggestions from graphs
    tracks_query = db.session.query(Track)
    for track in tracks_query.yield_per(1000):
        # A bit of randomness
        if track.id % 9 != 0:
            continue

        if not track.get_genres_set():
            continue

        # Get k nearest nodes
        nodes = get_shortest_neigbors(track.spotify_id)

        # Remove the seed track node from the returned nearest node
        del nodes[track.spotify_id]

        # Filter number of nodes
        to_remove = list(nodes.keys())[4:]
        for key in to_remove:
            del nodes[key]

        if not len(nodes) == 4:
            continue

        # Continue if a node suggestion doesn't have a genre set
        flagged = False
        # for node in nodes:
        #     node_track = db.session.query(Track).filter(Track.spotify_id == node).first()
        #     if not node_track and not node_track.get_genres_set():
        #         flagged = True

        node_objects = [db.session.query(Track).filter(Track.spotify_id == node).first() for node in nodes]
        for node_object in node_objects:
            if not node_object:
                flagged = True
                break
            if not node_object.get_genres_set():
                flagged = True
                break
        if flagged:
            continue

        for node_track in node_objects:
            print('seed spotify id', track.spotify_id)
            print('seed genre set ', track.get_genres_set())
            print('seed last set ', track.lastfm_tags)
            print('seed spotify set ', track.spotify_artist_genres)
            print('node spotify id', node_track.spotify_id)
            print('node genre set ', node_track.get_genres_set())
            print('node last set ', node_track.lastfm_tags)
            print('node spotify set ', node_track.spotify_artist_genres)
            print(track.get_genres_set() & node_track.get_genres_set())
            print((len(track.get_genres_set() & node_track.get_genres_set())/len(track.get_genres_set()))*100)
            track_percent[track.id].append((len(track.get_genres_set() & node_track.get_genres_set())/len(track.get_genres_set()))*100)

        counter += 1
        if counter == SAMPLE_LIMIT:
            break

    valid_tracks = []
    for t in track_percent:
        valid_counter = 0
        for s in track_percent[t]:
            if s:
                valid_counter += 1
        if valid_counter > 3:
            valid_tracks.append(t)

    print('percent ', (len(valid_tracks)/counter)*100)


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        db.init_app(app)
        music_track_genre_evaluation()

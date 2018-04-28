# View functions for every api endpoint
import logging
logger = logging.getLogger('api')
import os

from flask import jsonify, request
from spotipy import SpotifyException

from api import bp, limiter, db, sentry
from api.graph import get_shortest_neigbors
from api.errors import bad_request
from api.external.spotify import get_spotify_object
from api.models import Track
from api.utils import wants_json_response, send_email


@bp.route('/api/v1/search/tracks/', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def tracks():
    """
    The searching of stored tracks endpoint.
    Takes a track artist or/and title text query and returns the results found.
    Takes also a number of wanted results, max to 10.
    For more, see the endpoints documentation http://playlist-api.readthedocs.io/en/latest/.
    """
    logger.info('Search endpoint requested from ip %s' % request.remote_addr)

    # Do not allow non json requests. Commented for now
    # if not wants_json_response():
    #     return bad_request("Send json accept header please")

    track_query = request.args.get('q', '')
    try:
        n = int(request.args.get('n', 10))  # n is the max number of results
    except ValueError:
        n = 10
    # Search on elastic
    tracks, total = Track.search(track_query)
    tracks_num = min(n, total)

    data = {"items": [track.to_dict() for track in tracks][:tracks_num]}

    return jsonify(data)


@bp.route('/api/v1/similar/', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def get_k_similar():
    """
    With a spotify_id return similar tracks with the help of the api's graph algorithms.
    Takes also a number of wanted results, max to 10.
    For more, see the endpoints documentation http://playlist-api.readthedocs.io/en/latest/.
    """
    logger.info('Similar endpoint requested from ip %s' % request.remote_addr)

    # if not wants_json_response():
    #     return bad_request("Send json accept header please")

    track_spotify_id = request.args.get('spotify_id', '')
    seed_track = db.session.query(Track).filter(Track.spotify_id == track_spotify_id).first()
    if not seed_track:
        return jsonify({'seed_info': {}, 'items': []})

    # The seed track metadata info returned in the response
    seed_info = seed_track.to_dict()

    try:
        k = int(request.args.get('n', 10))  # n is the max number of results
    except ValueError:
        k = 10

    # Get k nearest nodes
    nodes = get_shortest_neigbors(track_spotify_id)
    # Nodes-tracks to use to returned playlist. With the seed track
    nodes_to_playlist = list(nodes)

    # Remove the seed track node from the returned nearest node
    del nodes[track_spotify_id]

    # Filter number of nodes according to k
    to_remove = list(nodes.keys())[k:]
    for key in to_remove:
        del nodes[key]

    result = {'seed_info': seed_info, 'items': []}

    # Populate similar tracks info in response
    for spotify_id in nodes:
        track = db.session.query(Track).filter(Track.spotify_id == spotify_id).first()
        if not track:
            continue
        else:
            track_info = track.to_dict()
            track_info.update({'score': 1 / nodes[spotify_id]})
            result['items'].append(track_info)

    try:
        sp = get_spotify_object(with_oauth=True)
        playlist = sp.user_playlist_create(user=os.environ.get('SPOTIFY_USERNAME'), name=seed_track.name)

        # Add tracks to playlist
        sp.user_playlist_add_tracks(user=os.environ.get('SPOTIFY_USERNAME'), playlist_id=playlist['id'], tracks=nodes_to_playlist)
        # Add link and id to result
        result['playlist'] = {'spotify_id': playlist['id'],
                              'url': playlist['external_urls']['spotify']}
    except SpotifyException:
        # send email and log in sentry if spotify exception
        sentry.captureException()
        send_email('santoniou.com@gmail.com',
                   'Possible spotify refresh token invalidation. Check errors and sentry')

    return jsonify(result)

#
# def get_and_check_seed_reccomentations(sp, spotify_id):
#     """Gets a spotify object and a spotify id and queries the spotify seed recommendations api.
#     Then checks if we have returned ids in the db. Then returns them."""
#
#     seed_reccomentations = sp.recommentations(seed_tracks=[spotify_id])
#
#     found_recommentations = []
#     return found_recommentations
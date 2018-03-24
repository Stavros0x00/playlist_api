# View functions for every api endpoint
import logging
logger = logging.getLogger('api')

from flask import jsonify, request

from api import bp, limiter, db
from api.errors import error_response, bad_request
from api.models import Track
from api.utils import wants_json_response


@bp.route('/api/v1/search/songs/', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def songs():
    logger.info('Search endpoint requested from ip %s' % request.remote_addr)
    if not wants_json_response():
        return bad_request("Send json accept header please")
    track_query = request.args.get('q')
    try:
        # n is the max number of results
        n = int(request.args.get('n', 10))
    except ValueError:
        n = 10
    tracks, total = Track.search(track_query)
    tracks_num = min(n, total)
    data = {"items": [track.to_dict() for track in tracks][:tracks_num]}
    return jsonify(data)


@bp.route('/api/v1/similar/', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def get_k_similar():
    logger.info('Similar endpoint requested from ip %s' % request.remote_addr)
    if not wants_json_response():
        return bad_request("Send json accept header please")
    track_id = request.args.get('spotify_id')
    track = db.session.query(Track).filter(Track.spotify_id == track_id).first()
    if not track:
        return ''
        # raise not found
    try:
        # n is the max number of results
        k = int(request.args.get('n', 10))
    except ValueError:
        k = 10
    # Get k nearest nodes
    # Get tags info from external apis
    from api.graph import get_shortest_neigbors
    data = get_shortest_neigbors(track_id, k)
    # find a better way
    to_remove = list(data.keys())[k:]
    for key in to_remove:
        del data[key]

    print(data)
    return jsonify(data=list(data.items()))




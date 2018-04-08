# View functions for every api endpoint
import logging
logger = logging.getLogger('api')

from flask import jsonify, request

from api import bp, limiter, db
from api.auth import sp
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
    seed_track = db.session.query(Track).filter(Track.spotify_id == track_id).first()
    if not seed_track:
        return ''
        # raise not found
    seed_info = {'spotify_id': seed_track.spotify_id,
                 'artist': seed_track.artist,
                 'name': seed_track.name,
                 'preview_url': seed_track.preview_url,
                 'lastfm_tags': seed_track.lastfm_tags}
    try:
        # n is the max number of results
        k = int(request.args.get('n', 10))
    except ValueError:
        k = 10
    # Get k nearest nodes
    # Get tags info from external apis
    from api.graph import get_shortest_neigbors
    data = get_shortest_neigbors(track_id, k)
    # from pdb import set_trace
    # set_trace()
    # find a better way
    del data[track_id]
    to_remove = list(data.keys())[k:]
    for key in to_remove:
        del data[key]

    result = {'seed_info': seed_info, 'items': []}
    for spotify_id in data:
        track = db.session.query(Track).filter(Track.spotify_id == spotify_id).first()
        if not track:
            continue
        else:
            result['items'].append({'spotify_id': spotify_id,
                                    'artist': track.artist,
                                    'name': track.name,
                                    'score': data[spotify_id],
                                    'preview_url': track.preview_url,
                                    'lastfm_tags': track.lastfm_tags})

    # Create spotify playlist
    # playlist = sp.user_playlist_create(user='playlist_api', name=seed_track.name)
    # import pdb
    # pdb.set_trace()
    # # Add tracks to playlist
    # sp.user_playlist_add_tracks(user='playlist_api', playlist_id='', tracks=[])
    # # Add link and id to result
    # result['playlist'] = {'spotify_id': '',
    #                       'url': ''}
    print(data)
    print(result)
    return jsonify(result)




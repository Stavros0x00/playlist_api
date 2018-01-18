# View functions for every api endpoint

from flask import jsonify, request

from api import bp, limiter
from api.errors import error_response, bad_request
from api.models import Track
from api.utils import wants_json_response


@bp.route('/api/v1/search/songs/', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def songs():
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




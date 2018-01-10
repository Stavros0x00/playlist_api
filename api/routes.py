# View functions for every api endpoint

from flask import jsonify, request

from api import app, limiter
from api.errors import error_response, bad_request
from api.models import Track
from api.utils import wants_json_response


@app.route('/api/v1/search/songs', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def songs():
    if not wants_json_response():
        return bad_request("Send json content type header please")
    track_query = request.args.get('q')
    tracks, total = Track.search(track_query)
    data = {"items": [track.to_dict() for track in tracks]}
    return jsonify(data)

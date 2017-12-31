# View functions for every api endpoint

from flask import jsonify

from api import app, limiter
from api.errors import error_response, bad_request
from api.utils import wants_json_response


@app.route('/api/v1/songs', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def songs():
    if not wants_json_response():
        return bad_request("Send json content type header please")
    return jsonify({"songs": "songs"})

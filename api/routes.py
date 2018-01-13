# View functions for every api endpoint

from flask import jsonify, request

from api import app, limiter
from api.errors import error_response, bad_request
from api.models import Track
from api.utils import wants_json_response


@app.route('/api/v1/search/songs', methods=['GET'])
@limiter.limit("5 per second")  # Rate limits are restarting with server restart
def songs():
    """Return collection of posts.

            .. :quickref: Posts Collection; Get collection of posts.

            **Example request**:

            .. sourcecode:: http

              GET /posts/ HTTP/1.1
              Host: example.com
              Accept: application/json

            **Example response**:

            .. sourcecode:: http

              HTTP/1.1 200 OK
              Vary: Accept
              Content-Type: application/json

              [
                {
                  "post_id": 12345,
                  "author": "/author/123/",
                  "tags": ["sphinx", "rst", "flask"],
                  "title": "Documenting API in Sphinx with httpdomain",
                  "body": "How to..."
                },
                {
                  "post_id": 12346,
                  "author": "/author/123/",
                  "tags": ["python3", "typehints", "annotations"],
                  "title": "To typehint or not to typehint that is the question",
                  "body": "Static checking in python..."
                }
              ]

            :query sort: sorting order e.g. sort=author,-pub_date
            :query q: full text search query
            :resheader Content-Type: application/json
            :status 200: posts found
            :returns: :class:`myapp.objects.Post`
            """
    if not wants_json_response():
        return bad_request("Send json content type header please")
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

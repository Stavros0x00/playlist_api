from flask import request


def wants_json_response():
    """
    Checks if the request is for json
    """
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']

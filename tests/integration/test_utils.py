from flask import url_for

from api.utils import wants_json_response


def test_wants_json_response(client, app):
    """The request context here is created flask pytest fixture
    http://pytest-flask.readthedocs.io/en/latest/features.html#request-ctx-request-context"""
    res = client.get(url_for('api.tracks'), headers={'Accept': 'application/json'})

    assert wants_json_response()


def test_not_wants_json_response(client, app):
    """The request context here is created flask pytest fixture
    http://pytest-flask.readthedocs.io/en/latest/features.html#request-ctx-request-context"""
    res = client.get(url_for('api.tracks'), headers={'Accept': 'text/html'})

    assert not wants_json_response()

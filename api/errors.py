# Handle API errors and bad requests

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from api import bp, db


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)


@bp.errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)


@bp.errorhandler(429)
def ratelimit_handler(error):
    return error_response(429, "ratelimit exceeded %s" % error.description)

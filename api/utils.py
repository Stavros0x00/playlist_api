from flask import request
from flask_mail import Message

from api import mail


def wants_json_response():
    """
    Checks if the request is for json
    """
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


def send_email(to, message):
    msg = Message('Log-email-posible-error', sender='santoniou.com@gmail.com', recipients=[to])
    msg.body = message
    mail.send(msg)

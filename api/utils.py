import os

from flask import request
from flask_mail import Message

from api import mail


def wants_json_response():
    """
    Checks if the request is for json
    """
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


def send_email(to, message):
    msg = Message('Log-email-posible-error', sender=os.environ.get('NOTIFICATIONS_EMAIL'), recipients=[to])
    msg.body = message
    mail.send(msg)


def chunks(l, n):
    """Yield successive n-sized chunks from l.
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]
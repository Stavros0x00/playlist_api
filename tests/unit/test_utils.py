# Test the utils.py functions
import os

from api import mail
from api.utils import chunks, send_email


def test_chunks():
    test_list = list(range(999999))
    for index, chunk in enumerate(chunks(test_list, 100000)):
        if index == 0:
            assert isinstance(chunk, list)
            assert len(chunk) == 100000

        elif index == 9:
            assert isinstance(chunk, list)
            assert len(chunk) == 99999


def test_send_email(app):
    """It doesn't send a real email because of the TESTING=True in config.
    https://pythonhosted.org/Flask-Mail/#unit-tests-and-suppressing-emails"""
    with mail.record_messages() as outbox:
        send_email(os.environ.get('NOTIFICATIONS_EMAIL'), 'test')

        assert len(outbox) == 1
        assert outbox[0].subject == "Log-email-posible-error"
        assert outbox[0].body == "test"



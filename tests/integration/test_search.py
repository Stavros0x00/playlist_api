from time import sleep

from api import db
from api.models import Track
from api.search import add_to_index, remove_from_index, query_index


def test_add_to_index():
    track = db.session.query(Track).filter(Track.spotify_id == '07HF5tFmwh6ahN93JC6LmE').first()
    res = add_to_index('test_tracks', track)

    assert res['_index'] == 'test_tracks'
    assert res['result'] == 'created'

    remove_from_index('test_tracks', track)


def test_remove_from_index():
    track = db.session.query(Track).filter(Track.spotify_id == '07HF5tFmwh6ahN93JC6LmE').first()
    add_to_index('test_tracks', track)
    res = remove_from_index('test_tracks', track)

    assert res['_index'] == 'test_tracks'
    assert res['result'] == 'deleted'


def test_query_index():
    track_1 = db.session.query(Track).filter(Track.spotify_id == '6QgjcU0zLnzq5OrUoSZ3OK').first()
    track_2 = db.session.query(Track).filter(Track.spotify_id == '1i8oOEZKBzaxnEmcZYAYCQ').first()
    add_to_index('test_tracks', track_1)
    add_to_index('test_tracks', track_2)

    # We must wait a bit before trying to query the index
    sleep(2)
    res = query_index(index='test_tracks', query='portugal', page=1, per_page=1)
    assert isinstance(res[0], list)
    assert isinstance(res[1], int)
    assert res[0][0] == track_1.id

    res = query_index(index='test_tracks', query='frenic', page=1, per_page=100)
    assert isinstance(res[0], list)
    assert isinstance(res[1], int)
    assert res[0][0] == track_2.id


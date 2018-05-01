# Test models functions

import pytest

from api import db
from api.models import Track


@pytest.mark.parametrize('spotify_id, expected_key', [
    ('07HF5tFmwh6ahN93JC6LmE', 'spotify_id'),
    ('07HF5tFmwh6ahN93JC6LmE', 'artist'),
    ('07HF5tFmwh6ahN93JC6LmE', 'name'),
    ('07HF5tFmwh6ahN93JC6LmE', 'preview_url'),
    ('07HF5tFmwh6ahN93JC6LmE', 'lastfm_tags'),
    ('6QgjcU0zLnzq5OrUoSZ3OK', 'spotify_id'),
    ('1i8oOEZKBzaxnEmcZYAYCQ', 'spotify_id'),
])
def test_track_to_dict(app, spotify_id, expected_key):
    track = db.session.query(Track).filter(Track.spotify_id == spotify_id).first()

    track_info = track.to_dict()
    print(track_info)
    assert expected_key in track_info


@pytest.mark.parametrize('spotify_id, expected_neighbor_1, expected_neighbor_2', [
    ('6QgjcU0zLnzq5OrUoSZ3OK', '07HF5tFmwh6ahN93JC6LmE', '1i8oOEZKBzaxnEmcZYAYCQ'),
])
def test_track_get_neighbors(app, spotify_id, expected_neighbor_1, expected_neighbor_2):
    track = db.session.query(Track).filter(Track.spotify_id == spotify_id).first()
    neighbors = track.get_neighbors()
    assert neighbors[0].spotify_id == expected_neighbor_1
    assert neighbors[1].spotify_id == expected_neighbor_2


@pytest.mark.parametrize('spotify_id, expected_type, expected_genre', [
    ('6QgjcU0zLnzq5OrUoSZ3OK', set, 'modern rock'),
])
def test_track_get_genres_set(app, spotify_id, expected_type, expected_genre):
    track = db.session.query(Track).filter(Track.spotify_id == spotify_id).first()
    genres = track.get_genres_set()
    assert isinstance(genres, expected_type)
    assert expected_genre in genres

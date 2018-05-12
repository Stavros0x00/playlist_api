# Test the routes.py views
from collections import namedtuple

from flask import url_for
import pytest


ExpectedForTrackSearch = namedtuple('ExpectedForTrackSearch', ['type', 'field', 'field_type'])


@pytest.mark.parametrize('query, num_of_results, expected', [
    ('Oasis', '10', ExpectedForTrackSearch(dict, 'items', list)),
    ('Oasis', '0', ExpectedForTrackSearch(dict, 'items', list)),
])
def test_song_search(client, query, num_of_results, expected):  # The client object comes from pytest-flask fixtures
    result = client.get(url_for('api.tracks', q=query, n=num_of_results))
    json_payload = result.json

    assert isinstance(json_payload, expected.type)
    assert expected.field in json_payload
    assert isinstance(json_payload[expected.field], expected.field_type)


ExpectedForSimilarSearch = namedtuple('ExpectedForSimilarSearch', ['type', 'items_field', 'seed_info_field', 'items_field_type'])


@pytest.mark.parametrize('spotify_id, num_of_results, expected', [
    ('07HF5tFmwh6ahN93JC6LmE', '10', ExpectedForSimilarSearch(dict, 'items', 'seed_info', list)),
    ('6QgjcU0zLnzq5OrUoSZ3OK', '0', ExpectedForSimilarSearch(dict, 'items', 'seed_info', list)),
])
def test_similar_search(client, spotify_id, num_of_results, expected):
    result = client.get(url_for('api.get_k_similar', spotify_id=spotify_id, n=num_of_results))
    json_payload = result.json

    assert isinstance(json_payload, expected.type)

    assert expected.seed_info_field in json_payload
    assert 'id' in json_payload[expected.seed_info_field]
    assert 'spotify_id' in json_payload[expected.seed_info_field]
    assert 'artist' in json_payload[expected.seed_info_field]
    assert 'name' in json_payload[expected.seed_info_field]

    assert expected.items_field in json_payload
    assert isinstance(json_payload[expected.items_field], expected.items_field_type)

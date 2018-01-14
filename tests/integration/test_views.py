from collections import namedtuple

from flask import url_for
import pytest


ExpectedForMbid = namedtuple('ExpectedForMbid', ['type', 'field', 'field_type'])


@pytest.mark.parametrize('query, num_of_results, expected', [
    ('Oasis', '10', ExpectedForMbid(dict, 'items', list)),
    ('Oasis', '0', ExpectedForMbid(dict, 'items', list)),
])
def test_song_search(client, query, num_of_results, expected):
    result = client.get(url_for('api.songs', q=query, n=num_of_results))
    json_payload = result.json
    assert isinstance(json_payload, expected.type)
    assert expected.field in json_payload
    assert isinstance(json_payload[expected.field], expected.field_type)

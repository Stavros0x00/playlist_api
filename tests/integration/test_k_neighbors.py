from api import db
from api.k_neighbors import get_min_max_values, normalize_columns, build_model, query_model, boost_from_k_neigbors
from api.models import TrackFeatures, Track


def test_normalize_columns(app):
    track = db.session.query(Track).filter(Track.spotify_id == '6QgjcU0zLnzq5OrUoSZ3OK').first()
    track_features = db.session.query(TrackFeatures).filter(TrackFeatures.track_id == track.id).first()
    MIN_MAX_VALUES = get_min_max_values(TrackFeatures)

    normalized = normalize_columns(track_features, MIN_MAX_VALUES)

    assert isinstance(normalized, dict)
    assert 'valence' in normalized
    assert isinstance(normalized['valence'], float)
    assert 0 <= normalized['valence'] <= 1


def test_get_min_max_values(app):
    MIN_MAX_VALUES = get_min_max_values(TrackFeatures)

    assert isinstance(MIN_MAX_VALUES, dict)
    assert 'valence' in MIN_MAX_VALUES
    assert 'min' in MIN_MAX_VALUES['valence'] and isinstance(MIN_MAX_VALUES['valence']['min'], float)
    assert 'max' in MIN_MAX_VALUES['valence'] and isinstance(MIN_MAX_VALUES['valence']['max'], float)


def test_query_model(app):
    build_model()

    track = db.session.query(Track).filter(Track.spotify_id == '6QgjcU0zLnzq5OrUoSZ3OK').first()

    k_neigbors = query_model(track, k=2)

    assert isinstance(k_neigbors, list)
    assert isinstance(k_neigbors[0], dict)
    assert 'artist' in k_neigbors[0]


def test_boost_from_k_neighbors(app, graph_tracks):
    k_neigbors = [{'id': 3, 'artist': 'Frenic', 'name': 'Travel Alone', 'spotify_id': '1i8oOEZKBzaxnEmcZYAYCQ',
                   'preview_url': None, 'lastfm_tags': None}
                  ]

    k_neigbors_suggestions = boost_from_k_neigbors(k_neigbors, graph_tracks)

    assert isinstance(k_neigbors_suggestions, list)
    assert isinstance(k_neigbors_suggestions[0], dict)


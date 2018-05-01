"""The functionality related to the k neighbors model created from the spotify track features"""
import pickle
import sys
sys.path.append('/home/playlistapi/playlist_api/')

from flask import current_app
import numpy as np
from sklearn.neighbors import KDTree
from sqlalchemy import func

from api import db, create_app
from api.models import TrackFeatures, Track


EXLUDED_COLUMNS = {'id', 'track_id'}


def get_min_max_values(Model):
    """Gets min max values for every column in the Model as a dict"""

    min_max_column_dict = {}

    for column in Model.__table__.columns:
        min_value = db.session.query(func.min(getattr(Model, column.name))).scalar()
        max_value = db.session.query(func.max(getattr(Model, column.name))).scalar()

        if column.name not in EXLUDED_COLUMNS:
            min_max_column_dict[column.name] = {'max': max_value, 'min': min_value}

    return min_max_column_dict


def normalize_columns(row, min_max_values_cols_dict):
    """Gets a db row and a min max column values dict and returns the values
    of this row normalized between 0 and 1"""
    normarized_row_dict = {}

    for column in row.__table__.columns:
        if column.name not in EXLUDED_COLUMNS:
            normarized_row_dict[column.name] = (getattr(row, column.name) - min_max_values_cols_dict[column.name]['min']) / (min_max_values_cols_dict[column.name]['max'] - min_max_values_cols_dict[column.name]['min'])

    return normarized_row_dict


def build_model():
    """Builds the k neighbors model"""
    # Get features for all tracks
    tracks_features = db.session.query(TrackFeatures).all()

    # Get min max values for every necessary column from the track_features table. Helps in normalisation
    min_max_values_cols_dict = get_min_max_values(TrackFeatures)

    # Normalize every row
    # Append also every track_id to keep them as metadata when indexing the results
    normalized = []
    for track_features in tracks_features:  # Maybe cache or make it global to not find the min and maxs every time
        normalized.append((normalize_columns(track_features, min_max_values_cols_dict), track_features.track_id))

    normalized_features = [list(entry[0].values()) for entry in normalized]
    normalized_ids = [entry[1] for entry in normalized]

    # Create the model
    tree = KDTree(np.array(normalized_features))  # , leaf_size=2)

    # Save the model
    with open(current_app.config['K_NEIGHBORS_MODEL_LOCATION'], 'wb') as f:
        pickle.dump(tree, f)

    # Save metadata of the vectors of the model. It helps when querying the model
    with open(current_app.config['K_NEIGHBORS_MODEL_LOCATION_METADATA'], 'wb') as f:
        pickle.dump(normalized_ids, f)


def query_model(seed_track, k=20):
    """Queries the k neighbors model. k is the number of k neighbors that we want"""

    query_track_features = db.session.query(TrackFeatures).get(seed_track.id)
    if not query_track_features:
        return []

    # Normalize track features
    # Get min max values for every necessary column from the track_features table. Helps in normalisation
    min_max_values_cols_dict = get_min_max_values(TrackFeatures)  # Maybe cache or make it global to not find the min and maxs every time
    normalized = normalize_columns(query_track_features, min_max_values_cols_dict)
    normalized_features = [normalized[key] for key in normalized]


    # Load Model
    with open(current_app.config['K_NEIGHBORS_MODEL_LOCATION'], 'rb') as f:
        k_neigbors_model = pickle.load(f)

    # Load Metadata
    with open(current_app.config['K_NEIGHBORS_MODEL_LOCATION_METADATA'], 'rb') as f:
        k_neigbors_model_metadata = pickle.load(f)

    # Query the model and return the indexes of the closest neighbors and the distances
    # Indexes then will be used to query the metadata list of track ids

    try:
        dist, ind = k_neigbors_model.query([normalized_features], k=k)
    except FileNotFoundError:
        build_model()
        dist, ind = k_neigbors_model.query([normalized_features], k=k)

    # Find the track from the resulted indexes
    tracks_ids = [k_neigbors_model_metadata[index] for index in ind[0]]
    tracks = db.session.query(Track).filter(Track.id.in_(tracks_ids)).all()

    filtered_tracks = []
    for track in tracks:
        # Filter suggested tracks with same name and title
        # This is needed cause in the db we have same tracks with different spotify ids..
        if seed_track.name == track.name and seed_track.artist == track.artist:
            continue

        # Filter according to genre
        # Don't return tracks that don't have at least one common genre. This needs to be better analyzed.
        # e.g. don't just compare whole string. Use Levenshtein distance or something.
        if not (seed_track.get_genres_set() & track.get_genres_set()):
            continue

        filtered_tracks.append(track)

    return [track.to_dict() for track in filtered_tracks][:20]


def boost_from_k_neigbors(k_neighbors, graph_tracks):
    """Gets k_neighbors and the graph suggested tracks
        Then checks if we have returned ids in the db and common k_neighbors with the
        suggested from the graph tracks. If we have common then boosts the appropriate score.
        Then returns the modified graph suggested items"""

    graph_tracks_ids = {track['id'] for track in graph_tracks}
    k_neighbors_recommendations_for_result = []
    edited_score = False

    for rec in k_neighbors:
        # Get track from the db if exists
        track = db.session.query(Track).filter(Track.id == rec['id']).first()

        if not track:
            continue

        if rec['id'] in graph_tracks_ids:
            # If we have common spotify results and graph results boost the appropriate score
            for d in graph_tracks:
                if d['spotify_id'] == rec['id']:
                    d['score'] += 1  # TODO: Find a better formula for boosting the score
                    edited_score = True
                    print("We have common!!", rec['id'])

        else:
            k_neighbors_recommendations_for_result.append(track.to_dict())

    if edited_score:
        # Sort the tracks with the new score
        graph_tracks_list = sorted(graph_tracks, key=lambda k: k['score'], reverse=True)
    else:
        graph_tracks_list = graph_tracks

    return graph_tracks_list


if __name__ == '__main__':
    # Initialize app needed for using the models
    app = create_app()
    with app.app_context():
        build_model()

import math

from flask import current_app
import networkx as nx

from api import db
from api.models import Track


def create_undirected_graph():
    """
    Creates or updates a pickled undirected graph from the stored tracks.
    """
    try:
        G = nx.read_gpickle(current_app.config['UNDIRECTED_GRAPH_LOCATION'])
    except FileNotFoundError:
        G = nx.Graph()

    # Collect the tracks from the db that don't match current created nodes in the graph
    tracks = db.session.query(Track.spotify_id).all()
    tracks = [track[0] for track in tracks if not G.has_node(track[0])]

    if not tracks:
        return G

    G.add_nodes_from(tracks)

    for track_spotify_id in tracks:
        track = db.session.query(Track).filter(Track.spotify_id == track_spotify_id).first()
        if not track:
            continue

        neighbors = track.get_neighbors()

        for neighbor in neighbors:
            if G.has_edge(track_spotify_id, neighbor.spotify_id):
                G[track_spotify_id][neighbor.spotify_id]['weight'] += 1
            else:
                G.add_edge(track_spotify_id, neighbor.spotify_id, weight=1)

    # Normalize weight until you find a better solution to not record double weights
    for edge in G.edges():
        G[edge[0]][edge[1]]['weight'] /= 2

    nx.write_gpickle(G, current_app.config['UNDIRECTED_GRAPH_LOCATION'])

    return G


def transform_to_stochastic(G):
    """Transforms an undirected graph created from the stored tracks to a
    directed stochastic used to find the shortest path"""
    G = G.to_directed()
    G = nx.stochastic_graph(G, copy=True, weight='weight')

    for edge in G.edges():
        # Transform the previous weights to
        # the negative logs of the weights to use them as weights when finding the shortest path
        G[edge[0]][edge[1]]['weight'] = abs(-(math.log(G[edge[0]][edge[1]]['weight']))) if G[edge[0]][edge[1]]['weight'] > 0 else 0
        G[edge[1]][edge[0]]['weight'] = abs(-(math.log(G[edge[1]][edge[0]]['weight']))) if G[edge[1]][edge[0]]['weight'] > 0 else 0

    nx.write_gpickle(G, current_app.config['DIRECTED_GRAPH_LOCATION'])

    return G


def get_shortest_neigbors(spotify_id):
    """Finds the closest nodes to the node matching the spotify_id.
    Uses Dijkstra algorithm and finds nodes with a depth of 1"""
    try:
        G = nx.read_gpickle(current_app.config['DIRECTED_GRAPH_LOCATION'])
    except FileNotFoundError:
        G = transform_to_stochastic(create_undirected_graph())

    tracks = nx.single_source_dijkstra_path_length(G, spotify_id, cutoff=1)

    return tracks

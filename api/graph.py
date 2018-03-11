import networkx as nx

# remove it later
import sys
sys.path.append('/home/work/Dropbox/eap/diplomatikh/source/playlist_api/')

from api import db, create_app
from api.models import Track


def create_undirected_graph():
    # TODO: refactor the whole think...
    try:
        G = nx.read_gpickle("api/pickled_files/undirected_graph.gpickle")
    except FileNotFoundError:
        G = nx.Graph()
    tracks = db.session.query(Track.spotify_id).all()
    tracks = [track[0] for track in tracks if not G.has_node(track[0])]
    for edge in G.edges():
        if G[edge[0]][edge[1]]['weight'] > 2:
            print(G[edge[0]][edge[1]]['weight'])
            print(edge)
    if not tracks:
        return G
    G.add_nodes_from(tracks)
    # print(G)

    for track_spotify_id in tracks:
        track = db.session.query(Track).filter(Track.spotify_id == track_spotify_id).first()
        if not track:
            continue
        # print(track_spotify_id)
        neighbors = track.get_neighbors()
        # Careful here with O(n^2) and more if you count the for loops of get_neighbors... Refactor it
        for neighbor in neighbors:
            if G.has_edge(track_spotify_id, neighbor.spotify_id):
                G[track_spotify_id][neighbor.spotify_id]['weight'] += 1

            else:
                G.add_edge(track_spotify_id, neighbor.spotify_id, weight=1)

    # Normalize weight until you find a better solution to not record double weights
    for edge in G.edges():
        G[edge[0]][edge[1]]['weight'] /= 2
        print(G[edge[0]][edge[1]]['weight'])

    print(G.number_of_edges())
    print(G.number_of_nodes())
    print("called write")
    nx.write_gpickle(G, "api/pickled_files/undirected_graph.gpickle")

    return G


if __name__ == '__main__':
    # Initialize app needed for using the models
    from config import DevelopmentConfig
    app = create_app(config_class=DevelopmentConfig)
    with app.app_context():
        db.init_app(app)
        g = create_undirected_graph()


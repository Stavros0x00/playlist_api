from api import db
from api.graph import create_undirected_graph, transform_to_stochastic, get_shortest_neigbors
from api.models import Track, PlaylistToTrack, Playlist


def test_create_undirected_graph(app):
    track1 = Track(spotify_id='07HF5tFmwh6ahN93JC6LmE',
                   artist='Kyuss',
                   name='Space Cadet')
    db.session.add(track1)
    db.session.commit()
    track2 = Track(spotify_id='6QgjcU0zLnzq5OrUoSZ3OK',
                   artist='Portugal. The Man',
                   name='Feel It Still')
    db.session.add(track2)
    db.session.commit()
    track3 = Track(spotify_id='1i8oOEZKBzaxnEmcZYAYCQ',
                   artist='Frenic',
                   name='Travel Alone')
    db.session.add(track3)
    db.session.commit()

    playlist = Playlist(spotify_id='testrandom123',
                        playlist_user='testrandomuser')
    db.session.add(playlist)
    db.session.commit()

    tracks = [track1, track2, track3]
    for index, track in enumerate(tracks):
        playlist_to_track = PlaylistToTrack(order_in_playlist=index)
        playlist_to_track.track = track
        with db.session.no_autoflush:
            playlist.tracks.append(playlist_to_track)
        db.session.commit()

    G = create_undirected_graph()

    assert '6QgjcU0zLnzq5OrUoSZ3OK' in G.nodes
    assert ('07HF5tFmwh6ahN93JC6LmE', '6QgjcU0zLnzq5OrUoSZ3OK') in G.edges
    assert not G.is_directed()
    assert G.edges[('07HF5tFmwh6ahN93JC6LmE', '6QgjcU0zLnzq5OrUoSZ3OK')]['weight'] == 1
    assert G.edges[('6QgjcU0zLnzq5OrUoSZ3OK', '1i8oOEZKBzaxnEmcZYAYCQ')]['weight'] == 1


def test_transform_to_stochastic(app):
    G = create_undirected_graph()
    G = transform_to_stochastic(G)

    assert '6QgjcU0zLnzq5OrUoSZ3OK' in G.nodes
    assert ('07HF5tFmwh6ahN93JC6LmE', '6QgjcU0zLnzq5OrUoSZ3OK') in G.edges
    assert G.is_directed()
    assert G.edges[('07HF5tFmwh6ahN93JC6LmE', '6QgjcU0zLnzq5OrUoSZ3OK')]['weight'] == 0
    assert G.edges[('6QgjcU0zLnzq5OrUoSZ3OK', '1i8oOEZKBzaxnEmcZYAYCQ')]['weight'] == 0.36651292058166435


def test_get_shortest_neigbors(app):
    G = create_undirected_graph()
    G = transform_to_stochastic(G)
    nodes = get_shortest_neigbors('6QgjcU0zLnzq5OrUoSZ3OK')

    assert '6QgjcU0zLnzq5OrUoSZ3OK' in nodes
    assert nodes['6QgjcU0zLnzq5OrUoSZ3OK'] == 0
    assert nodes['07HF5tFmwh6ahN93JC6LmE'] == 0.36651292058166435
    assert nodes['1i8oOEZKBzaxnEmcZYAYCQ'] == 0.36651292058166435


from api.graph import create_undirected_graph, transform_to_stochastic, get_shortest_neigbors


def test_create_undirected_graph(app):
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

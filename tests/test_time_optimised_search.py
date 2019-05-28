import networkx as nx
import pytest
from color_coding.time_optimised_search import (
    count_all_children,
    numerate_from_leafs_to_root
)
import matplotlib.pyplot as plt


@pytest.mark.parametrize(
    "edges_list, root, node, expected",
    [
        ([(0, 1), (1, 2), (2, 3), (3, 4), (5, 1)], 0, 0, 5),
        ([(0, 1), (1, 2), (2, 3), (3, 4), (5, 1)], 0, 1, 4),
        ([(0, 1), (0, 2), (2, 3), (2, 4)], 0, 0, 4),
        ([(0, 1), (0, 2), (2, 3), (2, 4)], 0, 1, 0),
        ([(0, 1), (0, 2), (2, 3), (2, 4)], 0, 2, 2),
        ([(0, 1), (0, 2), (2, 3), (2, 4)], 0, 3, 0),
        ([(0, 1), (0, 2), (2, 3), (2, 4)], 0, 4, 0)
    ]
)
def test_count_all_children(edges_list, root, node, expected):
    g = nx.Graph()
    g.add_edges_from(edges_list)
    graph_labels_dict = {}
    for v in g.nodes:
        graph_labels_dict[v] = v
    nx.draw(g, labels=graph_labels_dict)
    plt.show()
    nodes_order = numerate_from_leafs_to_root(g, root)

    assert expected == count_all_children(g, nodes_order, root)[node]
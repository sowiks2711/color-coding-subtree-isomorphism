import networkx as nx
import pytest
from color_coding.time_optimised_search import (
    count_all_children,
    numerate_from_leafs_to_root
)


@pytest.mark.parametrize(
    "edges_list, root, node, expected",
    [
        ([(0, 1), (1, 2), (2, 3), (3, 4), (5, 1)], 0, 0, 5),
    ]
)
def test_count_all_children(edges_list, root, node, expected):
    g = nx.Graph()
    g.add_edges_from(edges_list)
    nx.draw(g)
    nodes_order = numerate_from_leafs_to_root(g, root)

    assert expected == count_all_children(g, nodes_order, root)[node]
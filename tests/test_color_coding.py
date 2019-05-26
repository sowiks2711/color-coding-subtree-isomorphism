import pytest
import networkx as nx
from color_coding.graph_utils import has_any_cycles
from color_coding.graph_utils import numerate_from_root

@pytest.mark.parametrize(
    "edges_list, expected",
    [
        ([(0, 1), (1, 2), (2, 3), (3, 4), (3, 1)], True),
        ([(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)], False)
    ]
)
def test_has_any_cycles_finds_cycle(edges_list, expected):
    g = nx.Graph()
    g.add_edges_from(edges_list)

    assert expected == has_any_cycles(g)


@pytest.mark.parametrize(
    "edges_list, expected",
    [
        ([(0, 1), (0, 2), (2, 5), (1, 3), (1, 4)], [5, 4, 3, 2, 1, 0]),
        ([(0, 1), (1, 2), (2, 3), (3, 4)], [4, 3, 2, 1])
    ]
)
def test_numerate_from_root(edges_list, expected):
    g = nx.Graph()
    g.add_edges_from(edges_list)

    assert expected == list(numerate_from_root(g))

import pytest
import networkx as nx
from color_coding.graph_utils import has_any_cycles


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

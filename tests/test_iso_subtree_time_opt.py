import pytest
import networkx as nx
from color_coding.time_optimised_alg import (
    SubtreeAnalizerFactory, SubtreeAnalizer, SubtreeData
)
import numpy as np
from unittest.mock import patch

square_g = nx.from_edgelist(
    [(0, 1), (1, 2), (2, 3), (3, 2)]
)

two_edeges_t = nx.from_edgelist(
    [(0, 1), (1, 2)]
)


@pytest.mark.parametrize(
    "tree, graph, g_colors",
    [
        (two_edeges_t, square_g, [0, 1, 2, 1])
    ]
)
def test_initialize_memory(tree, graph, g_colors):
    simple_tree_analizer = SubtreeAnalizerFactory(two_edeges_t, graph,
                                                  g_colors).create(0)
    memory_dict = simple_tree_analizer._memory_array
    assert len(memory_dict) == len(set(g_colors))
    for key, arr in memory_dict.items():
        arr.shape == (simple_tree_analizer._size, len(square_g))


@pytest.mark.parametrize(
    "tree, graph, g_colors",
    [
        (two_edeges_t, square_g, [0, 1, 2, 1])
    ]
)
def test_square_te_init(tree, graph, g_colors):
    alg = SubtreeAnalizerFactory(two_edeges_t, square_g, g_colors).create(0)
    memory_dict = alg._memory_array
    expected = {
        frozenset([0]): np.array(
            [
                [True, False, False, False],
                [True, False, False, False],
                [True, False, False, False]
            ]
        ), frozenset([1]): np.array(
            [
                [False, True, False, True],
                [False, True, False, True],
                [False, True, False, True]
            ]
        ), frozenset([2]): np.array(
            [
                [False, False, True, False],
                [False, False, True, False],
                [False, False, True, False]
            ]
        ),
    }
    for act, exp in zip(memory_dict, expected):
        np.testing.assert_array_equal


@pytest.fixture
def subtree_analizer() -> SubtreeAnalizer:
    def mock_call(mock):
        return {}
    with patch.object(
        SubtreeAnalizerFactory, "_initialize_memory",
        mock_call
    ):
        tree = nx.from_edgelist(
            [
                (0, 1), (0, 3), (0, 2),
                (3, 6), (3, 5), (3, 4),
                (2, 7), (7, 8), (7, 9)
            ]
        )
        colors = list(range(10))
        return SubtreeAnalizerFactory(tree, colors, colors).create(0)


def test_tree_analizer_size(subtree_analizer):
    actual_size = subtree_analizer._size
    assert actual_size == 10


def test_tree_analizer_root(subtree_analizer):
    actual_root = subtree_analizer._root
    assert actual_root == 0


def test_tree_analizer_children_count(subtree_analizer):
    actual_children_count = subtree_analizer._children_count
    assert actual_children_count == [9, 0, 3, 3, 0, 0, 0, 2, 0, 0]


def test_tree_node_order(subtree_analizer):
    actual_nodes_order = list(subtree_analizer._bottom_up_order)
    assert actual_nodes_order == [9, 8, 7, 4, 5, 6, 2, 3, 1, 0]


def test_subt_connections_order(subtree_analizer):
    actual_nodes_order = list(subtree_analizer._subtree_connections_asc())
    expected = [
        (SubtreeData(agg_root=7, agg_size=1, att_root=8, att_size=1)),
        (SubtreeData(agg_root=7, agg_size=2, att_root=9, att_size=1)),
        (SubtreeData(agg_root=2, agg_size=1, att_root=7, att_size=3)),
        (SubtreeData(agg_root=3, agg_size=1, att_root=6, att_size=1)),
        (SubtreeData(agg_root=3, agg_size=2, att_root=5, att_size=1)),
        (SubtreeData(agg_root=3, agg_size=3, att_root=4, att_size=1)),
        (SubtreeData(agg_root=0, agg_size=1, att_root=1, att_size=1)),
        (SubtreeData(agg_root=0, agg_size=2, att_root=3, att_size=4)),
        (SubtreeData(agg_root=0, agg_size=6, att_root=2, att_size=4)),
    ]
    print(actual_nodes_order)
    assert actual_nodes_order == expected


def test_subtree_colorings(subtree_analizer):
    coloring_list = list(subtree_analizer._colors_subset_iterator(2, 2))
    assert len(coloring_list) != 0
    #comb(2,10)*comb(2,8)
    assert len(coloring_list) == 1260
    for superset, s1, s2 in coloring_list:
        assert s1 < superset
        assert s2 < superset
        assert not s1 < s2
        assert not s2 < s1
        assert s1.union(s2) == superset

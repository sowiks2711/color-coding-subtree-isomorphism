import networkx as nx
from random import randint
from math import exp
import numpy as np
from typing import List, Dict, FrozenSet, Iterator, Tuple
from pydantic import BaseModel
from .graph_utils import (
    list_subsets_of_given_size,
    pairs_of_sets,
)


class SubtreeData(BaseModel):
    agg_root: int
    agg_size: int
    att_root: int
    att_size: int


class SubtreeAnalizer():
    def __init__(self,
                 root: int,
                 size: int,
                 children_count: List[int],
                 bottom_up_order: List[int],
                 tree: nx.Graph,
                 graph: nx.Graph,
                 graph_colors: List[int],
                 colors: FrozenSet,
                 memory_array: Dict[FrozenSet, np.ndarray]
                 ):
        self._root = root
        self._size = size
        self._children_count = children_count
        self._bottom_up_order = bottom_up_order
        self._tree = tree
        self._graph = graph
        self._graph_colors = graph_colors
        self._colors = colors
        self._memory_array = memory_array
        self._mapping_restore: Dict[Tuple[FrozenSet[int], int, int],
                                    Tuple[Tuple[FrozenSet[int], int, int],
                                          Tuple[FrozenSet[int], int, int]]
                                    ] = {}

    def find_subtree(self):
        for con_data in self._subtree_connections_asc():
            agg_subt, agg_size, att_subt, att_size = con_data
            for colors_data in self._subtree_colorings(
                agg_size[1], att_size[1]
            ):
                cols_subset, agg_cols, att_cols = colors_data
                self._check_mappings(
                    cols_subset, agg_subt[1], agg_cols, att_subt[1], att_cols
                )
        try:
            g_root = list(self._memory_array[self._colors][0, :]).index(True)
            return self._restore_mapping(g_root)
        except (ValueError, KeyError):
            return None

    def _restore_mapping(self, g_root):
        mapping = [0] * len(self._tree)
        self._traverse(self._colors, mapping, g_root, 0)
        return mapping

    def _traverse(self, colors, mapping, g_root, t_root):
        mapping[t_root] = g_root
        if len(colors) == 1:
            return

        (col1, tr1, gr1), (col2, tr2, gr2) = self._mapping_restore[
                                                (colors, t_root, g_root)
                                             ]
        self._traverse(col1, mapping, gr1, tr1)
        self._traverse(col2, mapping, gr2, tr2)

    def _check_mappings(self, cols_subset, agg_subt, agg_cols, att_subt,
                        att_cols):
        for v in self._graph:
            for vn in self._graph.neighbors(v):
                is_first_colorable = self._memory_array[agg_cols][agg_subt, v]
                is_sec_colorable = self._memory_array[att_cols][att_subt, vn]
                if is_first_colorable and is_sec_colorable:
                    self._fill_mappings(agg_cols, agg_subt, v,
                                        att_cols, att_subt, vn,
                                        cols_subset)

    def _fill_mappings(self, agg_cols, agg_subt, v,
                       att_cols, att_subt, vn,
                       cols_subset):
        if cols_subset not in self._memory_array:

            match_array = np.zeros((len(self._tree), len(self._graph)), 
                                   dtype=bool)
            self._memory_array[cols_subset] = match_array
        self._memory_array[cols_subset][agg_subt, v] = True
        connected_subt = (cols_subset, agg_subt, v)
        if connected_subt not in self._mapping_restore:
            last_agg = (agg_cols, agg_subt, v)
            last_att = (att_cols, att_subt, vn)
            self._mapping_restore[connected_subt] = (last_agg, last_att)

    def _subtree_connections_asc(self) -> Iterator[SubtreeData]:
        for agg_subt in self._bottom_up_order:
            agg_subt_size = 1
            for att_subt in self._get_direct_children(agg_subt):
                att_subt_size = self._children_count[att_subt] + 1
                yield SubtreeData(
                                  agg_root=agg_subt,
                                  agg_size=agg_subt_size,
                                  att_root=att_subt,
                                  att_size=att_subt_size
                                  )
                agg_subt_size = agg_subt_size + att_subt_size

    def _get_direct_children(self, node: int) -> Iterator[int]:
        for v in self._tree.neighbors(node):
            buo = self._bottom_up_order
            if buo.index(node) > buo.index(v):
                yield v

    def _subtree_colorings(self, agg_size, att_size):
        for cols_subset, agg_cols, att_cols in self._colors_subset_iterator(
                agg_size, att_size
        ):
            is_first_possible = agg_cols in self._memory_array
            is_second_possible = att_cols in self._memory_array
            if is_first_possible and is_second_possible:
                yield cols_subset, agg_cols, att_cols

    def _colors_subset_iterator(self, agg_size, att_size):
        avail_cols = agg_size + att_size
        for cols_subset in list_subsets_of_given_size(
            self._colors, avail_cols
        ):
            for agg_cols, att_cols in pairs_of_sets(
                cols_subset, agg_size, att_size
            ):
                yield cols_subset, agg_cols, att_cols


class SubtreeAnalizerFactory():
    def __init__(self, tree: nx.Graph, graph: nx.Graph):
        self._tree = tree
        self._graph = graph
        self._size = len(self._tree)
        self._nodes_order = list(self._bottom_up_order(0))
        self._children_count = self._count_all_children(self._nodes_order, 0)

    def create(self, graph_colors: List[int]) -> SubtreeAnalizer:
        if (len(graph_colors) != len(self._graph)):
            raise ValueError(
                "Graph colors mapping does not cover all graph vertices")
        colors = frozenset(graph_colors)
        mapping_restore = self._initialize_memory(graph_colors)

        return SubtreeAnalizer(
            0, self._size, self._children_count, self._nodes_order,
            self._tree, self._graph, graph_colors, colors, mapping_restore
        )

    def _bottom_up_order(self, root: int) -> Iterator[int]:
        top_down = nx.bfs_tree(self._tree, source=root)
        for g in reversed(list(top_down)):
            yield g

    def _count_all_children(self, nodes_order: List[int],
                            root: int) -> List[int]:
        """
        returns list of counts of descendants for every node in tree
        by the direction given by root node
        """
        nodes_order = list(nodes_order)
        children_count = [0]*len(self._tree)
        for v in nodes_order:
            vo = v

            count = 0
            for nv in self._tree.neighbors(vo):
                if nodes_order.index(nv) < nodes_order.index(vo):
                    count = count + 1 + children_count[nv]
            children_count[vo] = count

        return children_count

    def _initialize_memory(self, graph_colors) -> Dict[FrozenSet, np.ndarray]:
        iso_subtree = {}
        graph_size = len(self._graph)
        tree_size = len(self._tree)
        colors = set(graph_colors)
        for c in colors:
            match_array = np.zeros((tree_size, graph_size),
                                   dtype=bool)
            iso_subtree[frozenset([c])] = match_array
        for c in colors:
            for t in self._tree.nodes():
                for v in self._graph.nodes:
                    if graph_colors[v] == c:
                        iso_subtree[frozenset([c])][t, v] = True
        return iso_subtree


def color_coding_subtree(tree, graph):
    k = len(tree)
    attempts = int(exp(k+2))
    mapping = None
    random_coloring = None
    analizer_factory = SubtreeAnalizerFactory(tree, graph)
    for i in range(attempts):
        print(f"Attempt nr {i}", end='\r')
        random_coloring = [randint(0, k) for i in range(len(graph))]
        analizer = analizer_factory.create(random_coloring)
        mapping = analizer.find_subtree()
        if mapping is not None:
            break
    return mapping, random_coloring

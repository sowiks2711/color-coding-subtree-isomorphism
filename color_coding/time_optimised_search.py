import networkx as nx
from typing import List, Iterator, Dict, FrozenSet, Tuple
import numpy as np
from numpy import ndarray
from .graph_utils import (
    list_subsets_of_given_size,
    pairs_of_sets,
)


def get_direct_children(tree: nx.Graph, nodes_order: List[int],
                        node: int) -> Iterator[int]:
    for v in tree.neighbors(node):
        if nodes_order[node] > nodes_order[v]:
            yield v


def count_all_children(tree: nx.Graph, nodes_order: List[int],
                       root: int) -> List[int]:
    """
    returns list of counts of descendants for every node in tree 
    by the direction given by root node
    """
    nodes_order = list(nodes_order)
    children_count = [0]*len(tree)
    for v in nodes_order:
        vo = v

        count = 0
        for nv in tree.neighbors(vo):
            if nodes_order.index(nv) < nodes_order.index(vo):
                count = count + 1 + children_count[nv]
        children_count[vo] = count

    return children_count


def numerate_from_leafs_to_root(graph: nx.Graph, root: int) -> Iterator[int]:
    top_down = nx.bfs_tree(graph, source=root)
    for g in reversed(list(top_down)):
        yield g


def initialize_memory_array(graph, graph_colors, tree):
    iso_subtree = {}
    for t in tree.nodes:
        match_array = np.zeros((len(tree), len(graph)), dtype=bool)
        iso_subtree[frozenset([t])] = match_array
    for c in range(len(tree)):
        for t in tree.nodes:
            for v in graph.nodes:
                if graph_colors[v] == c:
                    iso_subtree[frozenset([c])][t, v] = True
    return iso_subtree


def find_isomorhic_subtree(graph: nx.Graph,
                           tree: nx.Graph,
                           graph_colors: List[int]
                           ) -> Tuple[ndarray, Dict[FrozenSet[int], ndarray]]:

    mapping_restore: Dict[FrozenSet[int], ndarray] = {}
    colors = list(range(len(tree)))
    tree_nodes_order = list(numerate_from_leafs_to_root(tree, 0))
    childrens_count = count_all_children(tree, tree_nodes_order, 0)
    iso_subtree = initialize_memory_array(graph, graph_colors, tree)
    for subt_index in tree_nodes_order:
        cur_subt_size = 1
        t_children_gen = get_direct_children(tree, tree_nodes_order,
                                             subt_index)
        for include_subt in t_children_gen:
            include_subt_size = childrens_count[include_subt] + 1
            find_colored_iso_subtree(colors, cur_subt_size,
                                     include_subt_size,
                                     graph, iso_subtree,
                                     subt_index, include_subt,
                                     tree, mapping_restore)
            cur_subt_size = cur_subt_size + include_subt_size
    print(f"Algorithm checked {len(iso_subtree.keys())} subsets")
    print(iso_subtree)
    print(iso_subtree[frozenset(colors)])
    return iso_subtree, mapping_restore


def find_colored_iso_subtree(colors, cur_subt_size, include_subt_size, graph,
                             iso_subtree, subt_index, include_subt, tree,
                             mapping_restore):
    colors_nb = cur_subt_size + include_subt_size
    for avail_cols in list_subsets_of_given_size(colors,
                                                 colors_nb):
        for subt_cols, include_subt_cols in pairs_of_sets(avail_cols,
                                                          cur_subt_size,
                                                          include_subt_size):
            if subt_cols not in iso_subtree or \
               include_subt_cols not in iso_subtree:
                continue
            for v in graph.nodes:
                for vn in graph.neighbors(v):
                    is_first_colorable = iso_subtree[subt_cols][subt_index, v]
                    is_second_colorable = iso_subtree[include_subt_cols][include_subt, vn]
                    if is_first_colorable and is_second_colorable:
                        if avail_cols not in iso_subtree:
                            match_array = np.zeros((len(tree),
                                                    len(graph)),
                                                   dtype=bool)
                            iso_subtree[avail_cols] = match_array
                        iso_subtree[avail_cols][subt_index, v] = True
                        if (avail_cols, subt_index, v) not in mapping_restore:
                            mapping_restore[(avail_cols, subt_index, v)] =\
                              ((subt_cols, subt_index, v), (include_subt_cols,
                                                            include_subt, vn))
                        break


def restore_iso_subtree(iso_subtree: Dict[FrozenSet, np.array], tree: nx.Graph,
                        graph: nx.Graph, coloring: List[int],
                        mapping_restore: Dict[Tuple[FrozenSet, int, int],
                                              Tuple[Tuple[FrozenSet, int, int],
                                                    Tuple[FrozenSet, int, int]]
                                              ]) -> List[int]:
    # Change to auxiliary dict with list of all pointer vertices to given subtree.
    colors = frozenset(list(range(len(tree))))
    g_root = list(iso_subtree[colors][0, :]).index(True)
    mapping = [0] * len(tree)
    t_root = 0
    print("mapping_restore")
    print(mapping_restore)
    breakpoint()
    traverse(mapping, colors, g_root, t_root, mapping_restore)
    return mapping

# Do raportu
# czas ze względu na mały i duży graf,
# pamięć,
# liczba iteracji,
# dużo kopii w grafie, tylko jedno
# duże grafy bez poddrzewa


def traverse(mapping, colors, g_root, t_root, mapping_restore):
    mapping[t_root] = g_root
    if len(colors) <= 1:
        return

    (col1, tr1, gr1), (col2, tr2, gr2) = mapping_restore[(colors, t_root,
                                                          g_root)]
    traverse(mapping, col1, gr1, tr1, mapping_restore)
    traverse(mapping, col2, gr2, tr2, mapping_restore)
from networkx import Graph
from typing import List
import numpy as np
from .graph_utils import (
    get_direct_children,
    list_subsets_of_given_size,
    pairs_of_sets,
    count_all_children,
    numerate_from_leafs_to_root
)


def find_isomorhic_subtree(graph: Graph,
                           tree: Graph,
                           graph_colors: List[int]) -> np.array:

    colors = list(range(len(tree)))
    print(colors)
    print(tree.nodes)
    iso_subtree = {}
    len_t = len(tree)
    len_g = len(graph)
    tree_nodes_order = list(numerate_from_leafs_to_root(tree, 0))
    childrens_count = count_all_children(tree, tree_nodes_order, 0)
    print(tree_nodes_order)
    for v in graph.nodes:
        match_array = np.zeros((len_t, len_g), dtype=bool)
        iso_subtree[frozenset([graph_colors[v]])] = match_array
        for t in tree.nodes:
            match_array[t, v] = True

    for t in tree_nodes_order:
        t_size = 1
        t_children = list(get_direct_children(tree, tree_nodes_order, t))
        for tc in t_children:
            t_child_size = childrens_count[tc] + 1
            for sc in list_subsets_of_given_size(colors, t_size + t_child_size):
                for v in graph.nodes:
                    for s_prim, s_bis in pairs_of_sets(sc,
                                                       t_size,
                                                       t_child_size):
                        for vn in graph.neighbors(v):
                            fs_prim = frozenset(s_prim)
                            fs_bis = frozenset(s_bis)
                            if fs_prim not in iso_subtree or \
                               fs_bis not in iso_subtree:
                                continue
                            is_first_colorable = iso_subtree[fs_prim][t, v]
                            is_second_colorable = iso_subtree[fs_bis][tc, vn]
                            if is_first_colorable and is_second_colorable:
                                fs = frozenset(sc)
                                if fs not in iso_subtree:
                                    match_array = np.zeros((len_t, len_g),
                                                           dtype=bool)
                                    iso_subtree[fs] = match_array
                                iso_subtree[fs][t, v] = True
                                break
            t_size = t_size + t_child_size    
    print(iso_subtree[frozenset(colors)])
    return iso_subtree

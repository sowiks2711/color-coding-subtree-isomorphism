import networkx as nx
from typing import List, Iterator, Dict, FrozenSet
import numpy as np
from .graph_utils import (
    list_subsets_of_given_size,
    pairs_of_sets,
)
from collections import deque


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
    for v in graph.nodes:
        if frozenset([graph_colors[v]]) not in iso_subtree:
            match_array = np.zeros((len(tree), len(graph)), dtype=bool)
            iso_subtree[frozenset([graph_colors[v]])] = match_array
        for t in tree.nodes:
            match_array[t, v] = True
    return iso_subtree


def find_isomorhic_subtree(graph: nx.Graph,
                           tree: nx.Graph,
                           graph_colors: List[int]) -> np.array:

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
                                     subt_index, include_subt, tree)
            cur_subt_size = cur_subt_size + include_subt_size
    print(f"Algorithm checked {len(iso_subtree.keys())} subsets")
    print(iso_subtree)
    print(iso_subtree[frozenset(colors)])
    return iso_subtree


def find_colored_iso_subtree(colors, cur_subt_size, include_subt_size, graph,
                             iso_subtree, subt_index, include_subt, tree):
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
                        break


def restore_iso_subtree(iso_subtree: Dict[FrozenSet, np.array], tree: nx.Graph,
                        graph: nx.Graph, coloring: List[int]) -> List[int]:
    # Change to auxiliary dict with list of all pointer vertices to given subtree.
    tree_queue = deque([0])
    colors = set(list(range(len(tree))))
    all_colors = frozenset(list(range(len(tree))))
    g_root = list(iso_subtree[all_colors][0, :]).index(True)
    graph_queue = deque([g_root])
    mapping = [0] * len(tree)
    tree_nodes_order = list(numerate_from_leafs_to_root(tree, 0))
    childrens_count = count_all_children(tree, tree_nodes_order, 0)
    while(len(tree_queue) > 0):
        find_mapped_neighbours(tree_queue, graph_queue, mapping, colors,
                               coloring, tree, tree_nodes_order,
                               childrens_count, iso_subtree, graph)
    return mapping


def find_mapped_neighbours(tree_queue, graph_queue, mapping, colors, coloring,
                           tree, tree_nodes_order, childrens_count,
                           iso_subtree, graph):
    breakpoint()
    vt = tree_queue.popleft()
    vg = graph_queue.popleft()
    mapping[vt] = vg
    colors.discard(coloring[vg])

    def children_criterion(v):
        return childrens_count[v]
    dir_children = list(get_direct_children(tree, tree_nodes_order, vt))
    dir_children.sort(key=children_criterion)
    for nt in dir_children:
        tree_queue.append(nt)
        find_mapping(colors, childrens_count, nt, iso_subtree,
                     graph, vg, graph_queue, mapping)


def find_mapping(colors, childrens_count, nt, iso_subtree, graph,
                 vg, graph_queue, mapping):
    for subset in list_subsets_of_given_size(colors, childrens_count[nt] + 1):
        if subset in iso_subtree:
            for ng in graph.neighbors(vg):
                if ng not in set(mapping) and iso_subtree[subset][nt, ng]:
                    breakpoint()
                    graph_queue.append(ng)
                    return
    raise AssertionError()



    # # labels = range(len(graph.nodes))
    # labels = list(numerate_from_root(graph, 0))
    # print(f"labels: {labels}")
    # labels_dict = {}
    # for l, i in zip(labels, range(len(graph))):
    #     labels_dict[l] = i
    # print(labels_dict)
    # print(graph.nodes)
    # nx.draw(graph, node_color=range(len(graph)), labels=labels_dict)
    # plt.show()
    # print(labels)
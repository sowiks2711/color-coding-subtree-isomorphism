import time as time
from datetime import datetime
import uuid
import os
import psutil
from typing import Tuple, Iterator
import networkx as nx
import random as rnd
from color_coding.time_optimised_alg import color_coding_subtree
import matplotlib.pyplot as plt
# write function that for different sizes of tree and the same graph measures
# time, space, iterations
#   for graph without tree
#   for graph with one copy of tree
#   for graph with many copies of tree
# do the same for fixed tree and different sizes of graph
# kilka przykładów


def basic_graph_with_tree(tree, size):
    graph = nx.Graph()
    for e in tree.edges:
        graph.add_edge(*e)
    len_t = len(tree)
    for i in range(size - len_t):
        graph.add_edge(i + len_t, rnd.randint(0, len_t-1))
    
    id = str(uuid.uuid4().hex)
    return id, graph


def dense_graph_with_tree_copy(
    tree: nx.Graph,
    size: int
) -> Tuple[str, nx.Graph]:
    # just make every node degree higher or equal to maxdegree of tree
    if len(tree) > size:
        raise ValueError(
            "Contained tree has more nodes than specified graph size"
            )
    id, graph = basic_graph_with_tree(tree, size)

    for v in graph.nodes:
        for vv in graph.nodes:
            if rnd.uniform(0, 1) < 0.9:
                graph.add_edge(v, vv)

    return id, graph


def sparse_graph_with_tree_copy(
    tree: nx.Graph,
    size: int
) -> Tuple[str, nx.Graph]:
    # start from tree copy and add new vertices
    id, graph = basic_graph_with_tree(tree, size)

    return id, graph


def sparse_graph_without_copy(
    tree: nx.Graph,
    size: int
) -> Tuple[str, nx.Graph]:
    # create sparse graph with max degree lower than tree's max degree
    degree = get_max_degree(tree)
    if degree < 3:
        raise NotImplementedError(
            "Function supports only trees with max node degree higher than 2"
            )

    graph = nx.path_graph(size)

    return str(uuid.uuid4().hex), graph


def growing_trees_generator(
    from_size: int,
    to_size: int
) -> Iterator[Tuple[str, nx.Graph]]:
    '''
    Generates trees of growing size by adding extra
    edges to last generated tree
    '''
    gen = nx.nonisomorphic_trees(from_size)
    next(gen)
    g = next(gen)
    yield str(uuid.uuid4().hex), g
    for i in range(to_size - from_size):
        v = len(g)
        vv = rnd.randint(0, v-1)
        g = g.copy()
        g.add_edge(v, vv)
        yield str(uuid.uuid4().hex), g


def growing_sparse_graphs_with_tree(
    from_size: int,
    to_size: int,
    tree: nx.Graph
) -> (Iterator[Tuple[str, nx.Graph]]):
    id, g = sparse_graph_with_tree_copy(tree, from_size)
    yield id, g

    for i in range(from_size, to_size, 10):
        g = g.copy()
        for j in range(10):
            v = len(g)
            vv = rnd.randint(0, v-1)
            g.add_edge(v, vv)
        yield str(uuid.uuid4().hex), g


def growing_dense_graphs_with_tree(
    from_size: int,
    to_size: int,
    tree: nx.Graph
):
    id, g = dense_graph_with_tree_copy(tree, from_size)
    yield id, g

    for i in range(from_size, to_size, 10):
        for j in range(10):
            v = len(g)
            for k in range(int(len(g)/2)):
                vv = rnd.randint(0, v-1)
                g.add_edge(v, vv)
        yield str(uuid.uuid4().hex), g


def growing_graphs_without_tree(from_size: int, to_size: int, tree: nx.Graph):
    for i in range(from_size, to_size, 10):
        id, g = sparse_graph_without_copy(tree, i)
        g = g.copy()
        yield id, g


def get_max_degree(graph: nx.Graph) -> int:
    def degree_extractor(t: Tuple[int, int]) -> int:
        v, d = t
        return d

    graph_degree = max(graph.degree(),
                       key=degree_extractor)[1]

    return graph_degree


def save_result(tree, graph, mapping, colors, save):
    graph_labels_dict = {}
    nodes_order = list(graph.nodes)
    for v in nodes_order:
        graph_labels_dict[v] = v
    tree_labels_dict = {}
    for v in tree.nodes:
        tree_labels_dict[v] = v
    colors_mapping = [0] * len(graph)
    for i in range(len(graph)):
        colors_mapping[nodes_order[i]] = colors[i]

    plt.subplot(121)
    nx.draw(tree, labels=tree_labels_dict)

    result_labels = {}
    for v in graph.nodes:
        if v in mapping:
            result_labels[v] = f"{v},{mapping.index(v)}"
        else:
            result_labels[v] = v

    plt.subplot(122)
    nx.draw(graph, node_color=colors_mapping, labels=result_labels,
            cmap=plt.cm.gist_rainbow)
    if save:
        plt.savefig("./results/fig" + str(hash(tree)) + "_" + str(hash(graph)))
    else:
        plt.show()
    plt.clf()


def report_performance(
    tree: Tuple[str, nx.Graph],
    graph: Tuple[str, nx.Graph],
    with_copy: bool,
    is_dense_graph: bool
):
    # csv model
    # tree_id, graph_id, tree_size, graph_size, time, memory, is_success,
    # graph_includes_copy, graph_density, iterations
    start_time = time.time()
    tree_id, tree_g = tree
    graph_id, graph_g = graph
    graph_size = len(graph_g)
    tree_size = len(tree_g)
    mapping, colors, iters, mean_mem = color_coding_subtree(tree_g, graph_g)
   
    time_meas = str(time.time() - start_time)
    is_success = True if mapping is not None else False
    if mapping is not None:
        save_result(tree_g, graph_g, mapping, colors, with_copy)

    print(f"{tree_id},{graph_id},{tree_size},{graph_size},{time_meas},{mean_mem},{is_success},{with_copy},{is_dense_graph},{iters}")


if __name__ == '__main__':

    start_tree_size = 4
    end_tree_size = 9

    start_graph_size = 10
    end_graph_size = 50
    midle_graph_size = int((end_graph_size+start_graph_size)/2)

    trees = list(growing_trees_generator(start_tree_size, end_tree_size))

    last_tree = trees[len(trees)-1][1]
    dense_graph_with_copy = dense_graph_with_tree_copy(
        last_tree,
        midle_graph_size
    )
    sparse_g_with_copy = sparse_graph_with_tree_copy(
        last_tree,
        midle_graph_size
    )

    sparse_g_without_copy = sparse_graph_without_copy(
        trees[0][1],
        midle_graph_size
    )

    middle_tree = trees[int(len(trees)/2)]

    # Test case 1: Growing trees, constant dense graph with many tree copies

    dense_graph_with_tree = dense_graph_with_tree_copy(
        last_tree,
        midle_graph_size
    )

    for tree in trees:
        report_performance(tree, dense_graph_with_tree, True, True)

    # Test case 2: Growing trees, constant sparse graph with small nr of tree
    # copies

    sparse_graph_with_tree = sparse_graph_with_tree_copy(
        last_tree,
        midle_graph_size
    )

    for tree in trees:
        report_performance(tree, sparse_graph_with_tree, True, False)


    # Test case 5: Constant tree, growing sparse graph with one or couple tree
    # copies

    sparse_graphs_with_tree = growing_sparse_graphs_with_tree(
        start_graph_size,
        end_graph_size,
        middle_tree[1]
    )

    for g in sparse_graphs_with_tree:
        report_performance(middle_tree, g, True, False)

    # Test case 6: Constant tree, growing dense graph with many tree copies

    dense_graphs = growing_dense_graphs_with_tree(
        start_graph_size,
        end_graph_size,
        middle_tree[1]
    )

    for g in dense_graphs:
        report_performance(middle_tree, g, True, True)

    # Test case 4: Constant tree, growing sparse graph without any tree copy

    sparse_graphs_without_tree = growing_graphs_without_tree(
        start_graph_size,
        end_graph_size,
        middle_tree[1]
    )

    for g in sparse_graphs_without_tree:
        report_performance(middle_tree, g, False, False)

    # Test case 3: Growing trees, constant sparse graph without any tree copy

    sparse_graph_without_tree = sparse_graph_without_copy(
        last_tree,
        midle_graph_size
    )

    for tree in trees:
        report_performance(tree, sparse_graph_without_tree, False, False)
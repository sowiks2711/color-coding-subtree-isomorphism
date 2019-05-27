import networkx as nx
import matplotlib.pyplot as plt
import itertools
from typing import Set, Tuple, Iterator


def draw_graph(graph: nx.Graph):
    colors = range(graph.number_of_nodes())
    nx.draw(graph, node_color=colors, cmap=plt.cm.gist_rainbow, 
            with_labels=True)
    plt.show()


def has_any_cycles(graph: nx.Graph) -> bool:
    n = graph.number_of_nodes()
    visited = [False] * n

    def traverse_graph(cv: int, lv: int):
        visited[cv] = True
        # import pdb; pdb.set_trace()
        for nv in graph.neighbors(cv):
            if nv == lv:
                continue
            if visited[nv]:
                return True
            if traverse_graph(nv, cv):
                return True
        return False

    for v in graph.nodes:
        if not visited[v]:
            if traverse_graph(v, -1):
                return True
    return False


def nodes_connected(graph: nx.Graph, u: int, v: int):
    return u in graph.neighbors(v)


def get_subtree_rooted_in_T(graph: nx.Graph, root: int):
    order = list(numerate_from_root(graph, 0))
    output = []
    operational = []
    output.append(root)
    operational.append(root)
    while len(operational) != 0:
        currRoot = operational.pop(0)
        for n in graph.neighbors(currRoot):
            if order.index(n) < order.index(currRoot):
                output.append(n)
                operational.append(n)
    for n in output:
        yield n


def numerate_from_root(graph: nx.Graph, source: int):
    top_down = nx.bfs_tree(graph, source=source)
    for g in reversed(list(top_down)):
        yield g


def list_subsets_of_given_size(set, size: int):
    list_subsets = list(itertools.combinations(set, size))
    for l in list_subsets:
        yield l


def are_disjoint(t1: tuple, t2: tuple):
    s1 = set(t1)
    s2 = set(t2)
    return s1.isdisjoint(s2)


def pairs_of_sets(color_set: Set[int], size: int,
                  size2: int) -> Iterator[Tuple[Set[int], Set[int]]]:
    for s in list_subsets_of_given_size(color_set, size):
        for ss in list_subsets_of_given_size(set(color_set) - set(s), size2):
            yield s, ss


if __name__ == "__main__":
    # draw_graph()
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)
        ]
    )
    print(list(numerate_from_root(graph, 0)))
    # print(list(pairs_of_sets(set(numerate_from_root(graph, 0)), 7, 1)))
    print(list(get_subtree_rooted_in_T(graph, 2)))

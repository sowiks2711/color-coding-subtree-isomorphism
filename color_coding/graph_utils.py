import networkx as nx
import matplotlib.pyplot as plt
import itertools
from typing import Set, Tuple, Iterator, FrozenSet


def draw_graph():
    graph = nx.Graph()
    edges_arr = [(0, 1), (1, 2), (2, 3), (3, 4), (3, 1)]
    graph.add_edges_from(edges_arr)
    colors = range(len(edges_arr))
    nx.draw(graph, node_color=colors, cmap=plt.cm.gist_rainbow)
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


def numerate_from_root(graph: nx.Graph, source: int):
    top_down = nx.bfs_tree(graph, source=source)
    for g in list(top_down):
        yield (abs(len(graph)-g-1))


def list_subsets_of_given_size(set, size: int):
    list_subsets = list(itertools.combinations(set, size))
    for l in list_subsets:
        yield frozenset(l)


def are_disjoint(t1: tuple, t2: tuple):
    s1 = set(t1)
    s2 = set(t2)
    return s1.isdisjoint(s2)


def pairs_of_sets(color_set: Set[int], size: int,
                  size2: int) -> Iterator[Tuple[FrozenSet[int],
                                                FrozenSet[int]]]:
    for s in list_subsets_of_given_size(color_set, size):
        for ss in list_subsets_of_given_size(set(color_set) - set(s), size2):
            yield frozenset(s), frozenset(ss)


if __name__ == "__main__":
    draw_graph()
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 6), (0, 2), (0, 3), (0, 4), (0, 5), (6, 1), (6, 7)
        ]
    )
    print(list(numerate_from_root(graph, 0)))
    print(list(pairs_of_sets(set(numerate_from_root(graph, 0)), 7, 1)))

import networkx as nx
import matplotlib.pyplot as plt


def draw_graph():
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 1), (0, 2), (1, 3), (1, 4), (2, 5)
        ]
    )
    nx.draw(graph, node_color=range(len(graph)), cmap=plt.cm.gist_rainbow,
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


def numerate_from_root(graph: nx.Graph, source: int):
    top_down = nx.bfs_tree(graph, source=source)
    for g in list(top_down):
        yield (abs(len(graph)-g-1))


if __name__ == "__main__":
    draw_graph()
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 6), (0, 2), (0, 3), (0, 4), (0, 5), (6, 1), (6, 7)
        ]
    )
    print(list(numerate_from_root(graph, 0)))

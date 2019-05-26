import networkx as nx
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    draw_graph()

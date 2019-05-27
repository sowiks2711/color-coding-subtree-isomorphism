from color_coding.time_optimal_search import find_isomorhic_subtree
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":

    tree = nx.Graph()
    tree.add_edges_from(
        [
            (0, 1), (0, 2), (0, 3), (2, 4), (2, 5), (5, 6)
        ]
    )
    graph = nx.Graph()
    graph.add_edges_from(
        [
            #(0, 1), (0, 2), (0, 3), (2, 4), (2, 5), (5, 6)
            (0, 1), (0, 2), (0, 3), (0, 6), (1, 5),
            (3, 4), (3, 5), (4, 5), (5, 6), (5, 7)
        ]
    )
    colors = [0, 1, 2, 3, 4, 5, 6, 1]
    print(graph.nodes)
    graph_labels_dict = {}
    for v in graph.nodes:
        graph_labels_dict[v] = v
    tree_labels_dict = {}
    for v in tree.nodes:
        tree_labels_dict[v] = v
    print(colors)
    plt.subplot(121)
    nx.draw(graph, node_color=colors, labels=graph_labels_dict, cmap=plt.cm.gist_rainbow)
    plt.subplot(122)
    nx.draw(tree, labels=tree_labels_dict)
    plt.show()

    find_isomorhic_subtree(graph, tree, colors)
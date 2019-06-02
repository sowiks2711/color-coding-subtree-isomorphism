from color_coding.time_optimised_alg import (
    SubtreeAnalizerFactory,
    SubtreeAnalizer,
    color_coding_subtree
)
import networkx as nx
import matplotlib.pyplot as plt


def show_result(tree, graph, mapping, colors):
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
            cmap=plt.cm.gist_rainbow, node_size=800)

    plt.show()


if __name__ == "__main__":

    print("@@@@Testy wydajnościowe duże@@@@")
    graph = nx.random_lobster(20, 0.75, 0.75)
    trees = nx.nonisomorphic_trees(6)
    for tree in trees:
        mapping, coloring = color_coding_subtree(tree, graph)
        print()
        if mapping is not None:
            print("Found!")
            show_result(tree, graph, mapping, coloring)
        else:
            print("Not found.")

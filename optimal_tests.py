from color_coding.time_optimised_search import find_isomorhic_subtree, restore_iso_subtree
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":

    tree = nx.Graph()
    tree.add_edges_from(
        [
            #(0, 1), (1, 2), (2, 3)
            (0, 1), (0, 2), (2, 3), (2, 4)
            #(0, 1), (0, 2), (2, 3)
        ]
    )
    graph = nx.Graph()
    graph.add_edges_from(
        [
            # (0, 1), (1, 2), (1, 3)
            #(0, 1), (1, 2), (1, 3), (2, 4)
            #(0, 1), (0, 2), (2, 3), (3, 4)
            #(0, 1), (0, 2), (2, 3), (2, 4), (4, 5)
             (0, 1), (0, 2), (0, 3), (0, 6), (1, 5),
             (3, 4), (3, 5), (4, 5), (5, 6), (5, 7)
        ]
    )
    # colors = [0, 1, 2, 3, 4, 5, 6, 1]
    # colors = [0, 1, 2, 3]
    colors = list(range(len(tree))) + list(range(len(graph)-len(tree)))
    print(graph.nodes)
    graph_labels_dict = {}
    for v in graph.nodes:
        graph_labels_dict[v] = v
    tree_labels_dict = {}
    for v in tree.nodes:
        tree_labels_dict[v] = v
    print(colors)
    plt.subplot(131)
    nx.draw(graph, node_color=colors, labels=graph_labels_dict,
            cmap=plt.cm.gist_rainbow)
    plt.subplot(132)
    nx.draw(tree, labels=tree_labels_dict)
    iso_subtree, mapping_restore = find_isomorhic_subtree(graph, tree, colors)
    mapping = restore_iso_subtree(iso_subtree, tree, graph, colors,
                                  mapping_restore)
    #breakpoint()
    print(mapping)
    result_labels = {}
    for v in graph.nodes:
        if v in mapping:
            result_labels[v] = mapping.index(v)
        else:
            result_labels[v] = -1

    plt.subplot(133)
    nx.draw(graph, node_color=colors, labels=result_labels,
            cmap=plt.cm.gist_rainbow)

    plt.show()

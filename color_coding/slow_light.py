import networkx as nx
# import matplotlib.pyplot as plt
from random import randint
from math import exp
from graph_utils import numerate_from_root, draw_graph
from graph_utils import get_subtree_rooted_in_T
import itertools
from typing import List


class Coloring:
    coloringsList: List[int]
    graph: nx.Graph

    def __init__(self, coloringsList, graph):
        self.coloringsList = coloringsList
        self.graph = graph


def CheckColoring(treeColoring: Coloring, treeRoot: int,
                  gPrim: Coloring, v: int, isoSubTree, order: List) -> bool:
    # order = list(numerate_from_root(treeColoring.graph, treeRoot))
    existsIsoSubtree = True
    if treeColoring.coloringsList[treeRoot] != gPrim.coloringsList[v]:
        return False
    subtreeSize = 0
    for t in treeColoring.graph.neighbors(treeRoot):
        if order.index(t) < order.index(treeRoot):
            subtreeSize = subtreeSize + 1
    if subtreeSize == 0:
        return True
    # children = list(treeColoring.graph.neighbors(treeRoot))
    for xCT in treeColoring.graph.neighbors(treeRoot):
        if order.index(xCT) < order.index(treeRoot):
            for vN in gPrim.graph.neighbors(v):
                if isoSubTree[xCT][vN]:
                    existsIsoSubtree = True
                    break
                existsIsoSubtree = False
        if not existsIsoSubtree:
            return False
    return True


def checkIfTreeExist(gPrim: Coloring, T: nx.Graph,
                     isoSubTree: List):
    order = list(numerate_from_root(T, 0))
    for coloring in getNextColoring(T):
        for t in order:
            for v in gPrim.graph.nodes():
                isoSubTree[t][v] = CheckColoring(coloring, t,
                                                 gPrim, v,
                                                 isoSubTree,
                                                 order)
    return isoSubTree


def getNextColoring(tree: nx.Graph):
    for per in itertools.permutations(range((tree.number_of_nodes()))):
        yield Coloring(per, tree)


def findTreeInGraph(G: nx.Graph, T: nx.Graph):
    if G.number_of_nodes() < T.number_of_nodes():
        return False
    k = (T.number_of_nodes())
    attempts = int(exp(k+2))
    # K = []
    # K.append(Coloring(range(4), T))
    for i in range(attempts):
        print(i)
        isoSubTree = [[False for x in range((G.number_of_nodes()))]
                      for y in range((T.number_of_nodes()))]
        randomColoringList = [randint(0, k) for i in
                              range((G.number_of_nodes()))]
        gPrim = Coloring(randomColoringList, G)
        isoSubTree = checkIfTreeExist(gPrim, T, isoSubTree)

        for i in isoSubTree[0]:
            if i:
                return True
    return False


if __name__ == "__main__":
  
    # graph.add_edges_from(
    #     [
    #         (0, 1), (0, 2), (0, 3), (3, 1), (1, 2), (4, 2), (5, 2), (5, 6)
    #     ]
    # )
    # graph2 = nx.Graph()
    # graph2.add_edges_from(
    #     [
    #         (0, 1), (1, 2), (0, 3), (0, 4), (0, 5), (0, 6)
    #     ]
    # )
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 1), (0, 2), (0, 3), (0, 4)
        ]
    )
    graph2 = nx.Graph()
    graph2.add_edges_from(
        [
            (0, 1), (1, 2), (2, 3), (3, 4)
        ]
    )
    draw_graph(graph)
    draw_graph(graph2)
    print(findTreeInGraph(graph, graph2))
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 1), (0, 2), (1, 3), (1, 4), (3, 7), (3, 8), (2, 5), (2, 6),
            (5, 9), (5, 10), (6, 11), (6, 12)
        ]
    )
    graph2 = nx.Graph()
    graph2.add_edges_from(
        [
            (0, 1), (0, 2), (2, 3)
        ]
    )
    draw_graph(graph)
    draw_graph(graph2)
    print(findTreeInGraph(graph, graph2))

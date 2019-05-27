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
    subTree = list(get_subtree_rooted_in_T(treeColoring.graph, treeRoot))
    if treeColoring.coloringsList[treeRoot] != gPrim.coloringsList[v]:
        return False
    if len(subTree) == 1:
        return True
    existsIsoSubtree = False
    for xCT in treeColoring.graph.neighbors(treeRoot):
        if xCT in subTree:
            for vN in gPrim.graph.neighbors(v):
                if isoSubTree[order.index(xCT)][vN] is True:
                    existsIsoSubtree = True
                    break
        if not existsIsoSubtree:
            return False
    return True


def checkIfTreeExist(gPrim: Coloring, T: nx.Graph, K: List[Coloring],
                     isoSubTree: List):
    order = list(numerate_from_root(T, 0))
    for coloring in K:
        for t in order:
            for v in gPrim.graph.nodes():
                isoSubTree[order.index(t)][v] = CheckColoring(coloring, t,
                                                              gPrim, v,
                                                              isoSubTree,
                                                              order)
        return isoSubTree


def findTreeInGraph(G: nx.Graph, T: nx.Graph):
    if G.number_of_nodes() < T.number_of_nodes():
        return False
    k = (T.number_of_nodes())
    attempts = int(exp(k))
    K = []
    for per in itertools.permutations(range((T.number_of_nodes()))):
        K.append(Coloring(per, T))

    for i in range(attempts):
        isoSubTree = [[False for x in range((G.number_of_nodes()))]
                      for y in range((T.number_of_nodes()))]
        randomColoringList = [randint(0, k) for i in
                              range((G.number_of_nodes()))]
        gPrim = Coloring(randomColoringList, G)
        isoSubTree = checkIfTreeExist(gPrim, T, K, isoSubTree)

        for i in isoSubTree[T.number_of_nodes()-1]:
            print(i)
            if i:
                return True
    return False


if __name__ == "__main__":
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 1), (0, 2), (0, 3)
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
    print(findTreeInGraph(graph2, graph))

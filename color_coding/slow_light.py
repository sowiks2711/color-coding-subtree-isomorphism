import networkx as nx
# import matplotlib.pyplot as plt
from random import randint
from math import exp
from graph_utils import numerate_from_root
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
                  gPrim: Coloring, v: int, isoSubTree) -> bool:
    subTree = list(get_subtree_rooted_in_T(treeColoring.graph, treeRoot))
    existsIsoSubtree = False
    if treeColoring.coloringsList[treeRoot] != gPrim.coloringsList[v]:
        return False
    if len(subTree) == 1:
        return True
    for xCT in treeColoring.graph.neighbors(treeRoot):
        if xCT in subTree:
            for vN in gPrim.graph.neighbors(v):
                if isoSubTree[vN][xCT]:
                    existsIsoSubtree = True
                    break
            if not existsIsoSubtree:
                return False
    return True


def checkIfTreeExist(gPrim: Coloring, T: nx.Graph, K: List[Coloring],
                     isoSubTree: List):
    for coloring in K:
        for t in numerate_from_root(coloring.graph, 0):
            for v in gPrim.graph.nodes():
                print(str(t) + " " + str(v))
                isoSubTree[v][t] = CheckColoring(coloring, t, gPrim, v,
                                                 isoSubTree)
        return isoSubTree


def findTreeInGraph(G: nx.Graph, T: nx.Graph):
    isoSubTree = [[False for x in range(len(G))]
                  for y in range(len(T))]
    k = len(T)
    attempts = int(exp(k))
    K = []
    for per in itertools.permutations(range(len(T))):
        K.append(Coloring(per, T))

    for i in range(attempts):
        randomColoringList = [randint(0, k) for i in range(len(G))]
        gPrim = Coloring(randomColoringList, G)
        isoSubTree = checkIfTreeExist(gPrim, T, K, isoSubTree)

    for s in isoSubTree[len(G)-1]:
        if s:
            return True


if __name__ == "__main__":
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 6), (0, 2), (0, 3), (0, 4), (0, 5), (6, 1), (6, 7)
        ]
    )
    graph2 = nx.Graph()
    graph2.add_edges_from(
        [
            (0, 1)
        ]
    )
    print(findTreeInGraph(graph, graph2))

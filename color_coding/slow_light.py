import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from math import exp
from graph_utils import draw_graph, has_any_cycles, numerate_from_root
from graph_utils import list_subsets_of_given_size, pairs_of_sets
import itertools
from typing import List


class Coloring:

    coloringsList: List[int]
    graph: nx.Graph

    def __init__(self, coloringsList, graph):
        self.coloringsList = coloringsList
        self.graph = graph


def CheckColoring(treeColoring: Coloring, treeRoot: int,
                  gPrim: Coloring, v: int) -> bool:
    if treeColoring.coloringsList[treeRoot] != gPrim.coloringsList[v]:
        return False
    return False


def checkIfTreeExist(gPrim: Coloring, T: nx.Graph, K: List[Coloring]):
    outputArray = [[False for x in range(len(gPrim.graph))]
                   for y in range(len(T))]
    for coloring in K:
        for t in numerate_from_root(coloring.graph, 0):
            for v in gPrim.graph.nodes():
                outputArray[t][v] = CheckColoring(coloring, t, gPrim, v)
    return outputArray


def findTreeInGraph(G: nx.Graph, T: nx.Graph):
    k = len(T)
    attempts = int(exp(k))
    K = []
    for per in itertools.permutations(range(len(T))):
        K.append(Coloring(per, T))

    for i in range(attempts):
        randomColoringList = [randint(0, k) for i in range(len(G))]
        gPrim = Coloring(randomColoringList, G)
        isoSubTree = checkIfTreeExist(gPrim, T, K)


if __name__ == "__main__":
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 6), (0, 2), (0, 3), (0, 4), (0, 5), (6, 1), (6, 7)
        ]
    )
    findTreeInGraph(graph, graph)

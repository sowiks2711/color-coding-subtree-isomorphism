import networkx as nx
# import matplotlib.pyplot as plt
from random import randint
from math import exp
from graph_utils import numerate_from_root, draw_graph_save, draw_result_save
import itertools
from typing import List
import time


class Coloring:
    coloringsList: List[int]
    graph: nx.Graph

    def __init__(self, coloringsList, graph):
        self.coloringsList = coloringsList
        self.graph = graph


def TraverseToLeaf(G: nx.Graph, T: nx.Graph, isoSubtree: List, v: int, xT: int,
                   mapping: List, order: List):
    mapping[xT] = v
    for xN in T.neighbors(xT):
        if order.index(xN) < order.index(xT):
            for vN in G.neighbors(v):
                if isoSubtree[xN][vN]:
                    mapping = TraverseToLeaf(G, T, isoSubtree, vN, xN, mapping, 
                                             order)
                    break
    return mapping


def getGraphBack(G: nx.Graph, T: nx.Graph, isoSubTree: List, order: List):
    mapping = [-1 for i in range(T.number_of_nodes())]
    vN = isoSubTree[0].index(True)
    xN = 0
    mapping = TraverseToLeaf(G, T, isoSubTree, vN, xN, mapping, order)
    return mapping


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
                     isoSubTree: List, order: List):
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
    order = list(numerate_from_root(T, 0))
    k = (T.number_of_nodes())
    attempts = int(exp(k+2))
    # K = []
    # K.append(Coloring(range(4), T))
    for i in range(attempts):
        isoSubTree = [[False for x in range((G.number_of_nodes()))]
                      for y in range((T.number_of_nodes()))]
        randomColoringList = [randint(0, k) for i in
                              range((G.number_of_nodes()))]
        gPrim = Coloring(randomColoringList, G)
        isoSubTree = checkIfTreeExist(gPrim, T, isoSubTree, order)

        for a in isoSubTree[0]:
            if a:
                mapping = getGraphBack(G, T, isoSubTree, order)
                print("@@@Printing Mapping@@@")
                draw_result_save(G, mapping, "result")
                print("It took: " + str(i) + " attempts")
                return True
    return False


if __name__ == "__main__":
    print("@@@@Testy wydajnościowe@@@@")
    graph = nx.random_lobster(10, 0.75, 0.75)
    graph2 = nx.nonisomorphic_trees(4)
    for g in graph2:
        draw_graph_save(graph, "endurance_small")
        draw_graph_save(g, "endurance_small")
        start_time = time.time()
        print(findTreeInGraph(graph, g))
        print("It took " + str(time.time() - start_time) + " to calculate")

    print("@@@@Testy wydajnościowe duże@@@@")
    graph = nx.random_lobster(20, 0.75, 0.75)
    graph2 = nx.nonisomorphic_trees(6)
    for g in graph2:
        draw_graph_save(graph, "endurance_small")
        draw_graph_save(g, "endurance_small")
        start_time = time.time()
        print(findTreeInGraph(graph, g))
        print("It took " + str(time.time() - start_time) + " to calculate")

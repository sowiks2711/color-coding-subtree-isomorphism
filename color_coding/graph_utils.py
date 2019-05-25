import networkx as nx
import matplotlib.pyplot as plt

def draw_graph():
    G = nx.Graph()
    G.add_edges_from(
        [
            (1,2), (2,3), (3, 4), (3,1)
        ]
    )
    nx.draw(G, node_color=range(4) ,cmap=plt.cm.gist_rainbow)
    plt.show()
    

if __name__ == "__main__":
    draw_graph()
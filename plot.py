import matplotlib.pyplot as plt
import networkx as nx



def plotNeuralNetwork(architecture):
    #architecture.insert(0,architecture[0])

    G = nx.Graph()
    # explicitly set positions
    pos = {}
    z = 0
    numMax = max(architecture)
    ajusteAltura = (numMax-1)/2
    for i in range(0,len(architecture)): # layers
        num = architecture[i]
        alturaMedia = (num-1)/2
        layer = z
        for j in range(0,architecture[i]):    # neurons
            if num == numMax:
                pos.update({z: (i*2, j*2)})
            else:
                pos.update({z: (i*2, (j + (ajusteAltura-alturaMedia))*2)})
            if i > 0:
                for n in range(0,architecture[i-1]):
                    G.add_edge(z,z-n-1-j)
            z = z + 1


    # Plot nodes with different properties for the "wall" and "roof" nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=range(0,architecture[0]), alpha=0)
    nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=range(architecture[0],z), node_color="tab:blue")
    nx.draw_networkx_edges(G, pos, alpha=1, width=2)
    # Customize axes
    ax = plt.gca()
    ax.margins(0.11)
    plt.tight_layout()
    plt.axis("off")
    plt.show()


if __name__=="__main__":
    plotNeuralNetwork([3,3,4,1])
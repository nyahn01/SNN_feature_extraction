import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import networkx as nx

def draw_network(weights, delays, maxwidth=5, title=None):

    assert len(weights) == 78
    assert len(delays) == 78

    wmax = 20
    dmax = 10

    G = nx.Graph()

    # nodes

    layer1 = {
        11: [0, 0],
        12: [0, 1],
        13: [0, 2],
        14: [0, 3],
        15: [0, 4],
        16: [0, 6]
    }
    layer2 = {
        20: [7, 2],
        21: [6, 2+3**0.5],
        22: [4, 2+3**0.5],
        23: [3, 2],
        24: [4, 2-3**0.5],
        25: [6, 2-3**0.5]
    }
    layer3 = {
        30: [10, 1],
        31: [10, 3]
    }

    G.add_nodes_from(layer1.keys())
    G.add_nodes_from(layer2.keys())
    G.add_nodes_from(layer3.keys())

    #edges

    index = 0

    for a in layer1.keys():
        for b in layer2.keys():
            G.add_edges_from([(a, b, {'weight': weights[index], 'delay': delays[index]})])
            index += 1
    
    for a in layer2.keys():
        for b in layer2.keys():
            if a != b:
                G.add_edges_from([(a, b, {'weight': weights[index], 'delay': delays[index]})])
                index += 1

    for a in layer2.keys():
        for b in layer3.keys():
            G.add_edges_from([(a, b, {'weight': weights[index], 'delay': delays[index]})])
            index += 1

    # draw positively weighted connections

    nx.draw(G, pos = layer1|layer2|layer3, node_color='k', style='-',
            width = maxwidth * np.clip(weights, 0, None) / wmax,
            edge_color=[plt.get_cmap('coolwarm')(d) for d in delays/dmax])

    # draw negatively weighted connections

    nx.draw(G, pos = layer1|layer2|layer3, node_shape='.', node_color='w', style='--',
            width = maxwidth * np.abs(np.clip(weights, None, 0)) / wmax,
            edge_color=[cmap(d) for d in delays/dmax])

    # legend

    handles = [
        Line2D([0], [0], c='k', ls='-', label='(+) weight'),
        Line2D([0], [0], c='k', ls='--', label='(–) weight'),
        Line2D([0], [0], c='k', ls='-', lw=maxwidth, label='max |weight|'),
        Patch(facecolor=cmap(0.), label='min delay'),
        Patch(facecolor=cmap(1.), label='max delay')
    ]
    plt.legend(handles=handles)

    plt.title(title)

    return G


def cmap(value):

    return plt.get_cmap('coolwarm')(value)
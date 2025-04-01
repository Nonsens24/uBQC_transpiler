import QCompute
import networkx as nx
import matplotlib.pyplot as plt
from QCompute import *
# from QCompute.Define.PublicError import ArgumentError
from QCompute.QPlatform.QOperation import Operation


import networkx as nx


def plot_brickwork_graph_bfk_format(pattern):
    G = nx.Graph()
    coords = {}  # Maps qubit label to (row, col)

    # Build graph with correct (i, j) mapping
    for cmd in pattern.commands:
        if cmd.__dict__['name'] == "N":
            i, j = cmd.__dict__['which_qubits'][0]
            G.add_node((i, j))
            coords[(i, j)] = (j, -i)  # For plotting: X = col (j), Y = row (i), flipped for correct vertical stacking

        elif cmd.__dict__['name'] == "E":
            (i1, j1), (i2, j2) = cmd.__dict__['which_qubits']
            G.add_edge((i1, j1), (i2, j2))

    # Plot with grid alignment
    pos = {(i, j): (j, -i) for (i, j) in G.nodes}

    plt.figure(figsize=(12, 6))
    nx.draw(
        G, pos, with_labels=True,
        node_color='skyblue', node_size=600,
        font_size=8, font_weight='bold'
    )
    plt.title("Brickwork Graph in BFK Format")
    plt.axis("off")
    plt.show()




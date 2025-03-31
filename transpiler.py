# UBQC Compiler Project using Graphix
import networkx as nx
# Step 1: Installation
# First, install graphix and its dependencies
# pip install graphix networkx matplotlib numpy
from qiskit import QuantumCircuit, transpile

# Step 2: Project Structure
# ubqc_compiler/
# ├── compiler.py
# ├── example.py
# └── utils.py

# File: compiler.py
import numpy as np
from graphix import Circuit
from graphix.pattern import Pattern
import matplotlib.pyplot as plt


def circuit_to_brickwork(circuit: Circuit):

    # Decompose into universal gates explicitly
    basis_gates = ['h', 't', 'cx']
    qc_decomposed = transpile(circuit, basis_gates=basis_gates, optimization_level=3)
    print(qc_decomposed)


    print("Commands: ", commands)

    # Determine dimensions based on commands
    circuit_depth = len(commands)  # Approximation
    print("Len commands: ", circuit_depth)
    num_qubits = qc_decomposed.width
    print("num qubits: ", num_qubits)
    m = num_qubits + ((5 - num_qubits) % 8)
    n = circuit_depth * 3  # each gate can take up to 3 columns

    brickwork_graph = create_brickwork_state(n, m)

    # Map each command from Graphix onto the brickwork graph
    col = 1
    for cmd in commands:
        if cmd[0] == 'H' or cmd[0] == 'T':
            # Single qubit gate placement
            place_single_qubit_gate(brickwork_graph, col, cmd[1], gate=cmd[0])
            col += 3
        elif cmd[0] == 'CNOT':
            # Two qubit gate placement
            place_two_qubit_gate(brickwork_graph, col, cmd[1], cmd[2])
            col += 3

    return brickwork_graph

# Helper functions for gate placements
def place_single_qubit_gate(graph: nx.Graph, col: int, row: int, gate: str):
    """Place a single-qubit gate (H or T)"""
    assert gate in ['H', 'T'], "Unsupported single-qubit gate"
    for offset in range(3):
        graph.nodes[(col + offset, row)]['gate'] = gate


def place_two_qubit_gate(graph: nx.Graph, col: int, ctrl_row: int, target_row: int):
    """Place a two-qubit CNOT gate"""
    for offset in range(3):
        graph.nodes[(col + offset, ctrl_row)]['gate'] = 'CNOT_ctrl'
        graph.nodes[(col + offset, target_row)]['gate'] = 'CNOT_target'

def create_brickwork_state(n: int, m: int) -> nx.Graph:
    """
    Construct a brickwork state Gn×m according to Definition 1 from the Broadbent et al. paper.
    :param n: Number of columns.
    :param m: Number of rows (must satisfy m ≡ 5 mod 8).
    :return: NetworkX Graph representing the brickwork state.
    """
    assert m % 8 == 5, "Number of rows m must satisfy m ≡ 5 mod 8"

    G = nx.Graph()
    for x in range(1, n + 1):
        for y in range(1, m + 1):
            G.add_node((x, y))

    # Apply horizontal ctrl-Z gates
    for x in range(1, n + 1):
        for y in range(1, m):
            G.add_edge((x, y), (x, y + 1))

    # Apply vertical ctrl-Z gates
    for y in range(1, m + 1):
        if y % 8 == 3:
            for x in range(1, n, 2):
                G.add_edge((x, y), (x + 1, y))
                if y + 2 <= m:
                    G.add_edge((x, y + 2), (x + 1, y + 2))
        elif y % 8 == 7:
            for x in range(2, n, 2):
                G.add_edge((x, y), (x + 1, y))
                if y + 2 <= m:
                    G.add_edge((x, y + 2), (x + 1, y + 2))

    return G

def visualize_brickwork(graph: nx.Graph):
    """
    Visualize the brickwork graph.
    :param graph: NetworkX graph of the brickwork state.
    """
    pos = {(x, y): (y, -2 * x) for x, y in graph.nodes()}
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=300, edge_color='black', font_size=8)
    plt.title('Brickwork Graph')
    plt.show()

# Example usage
if __name__ == "__main__":
    n = 5
    m = 13  # Example satisfying m ≡ 5 mod 8
    brickwork_graph = create_brickwork_state(n, m)
    visualize_brickwork(brickwork_graph)
import QCompute
import networkx as nx
import matplotlib.pyplot as plt
from QCompute import *
# from QCompute.Define.PublicError import ArgumentError
from QCompute.QPlatform.QOperation import Operation


import networkx as nx

def dag_to_brickwork_graph(dag):
    G = nx.Graph()
    layer_map = {}  # Qubit ID → next column index

    # Track qubit positions in the brickwork layout
    for node in dag.topological_nodes():
        if node.name == 'barrier':
            continue
        qubits = node.qRegList
        classical = node.cRegList

        # Assign time slot per qubit
        max_layer = max([layer_map.get(q, 0) for q in qubits])
        for q in qubits:
            layer_map[q] = max_layer + 1

        # For now, treat each gate as a node
        node_id = (tuple(q for q in qubits), max_layer)
        G.add_node(node_id, gate=node.name)

        # Add edges between dependencies
        for q in qubits:
            for other_node in G.nodes:
                if other_node == node_id:
                    continue
                if q in other_node[0] and other_node[1] == max_layer - 1:
                    G.add_edge(node_id, other_node)

    return G

def draw_gate_graph(G):
    pos = {n: (n[1], -sum(n[0])/len(n[0])) for n in G.nodes()}  # Time vs qubit axis
    labels = {n: G.nodes[n]['gate'] for n in G.nodes()}
    plt.figure(figsize=(10, 5))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=800)
    nx.draw_networkx_labels(G, pos, labels)
    plt.title("Brickwork-style DAG from QCompute")
    plt.axis('off')
    plt.show()



def extract_graph_from_qcompute_circuit(env: QEnv):
    """
    Extracts a graph from QCompute circuit based on entangling (e.g., CZ) operations.
    Returns a NetworkX graph.
    """
    G = nx.Graph()

    print("Start Extraction")
    # Extract all gates from the circuit
    for cmd in env.program:
        # Check if the gate is a two-qubit entangling gate (like CZ)
        if hasattr(cmd, 'gate') and cmd.gate.name in ['CZ', 'CX', 'CNOT']:
            qubits = [q.qid for q in cmd.qRegList]
            if len(qubits) == 2:
                q1, q2 = qubits
                G.add_edge(q1, q2)
            elif len(qubits) == 1:
                G.add_node(qubits[0])
        elif hasattr(cmd, 'gate') and len(cmd.qRegList) == 1:
            # Add single-qubit operations as nodes (in case not entangled)
            G.add_node(cmd.qRegList[0].qid)

    return G

def visualize_graph(G: nx.Graph, title='QCompute-derived Graph State'):
    """
    Visualizes a NetworkX graph.
    """
    pos = nx.spring_layout(G)  # or use a circular layout etc.
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
    plt.title(title)
    plt.show()


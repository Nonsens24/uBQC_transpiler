import networkx as nx
from matplotlib import pyplot as plt

import example_circuits.qft
import utils
import visualiser

# Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT

# QCompute
from QCompute import *
from QCompute.OpenService.service_ubqc.client.transpiler import transpile_to_brickwork
from QCompute.OpenService.service_ubqc.client.qobject import Circuit
from QCompute.OpenService.service_ubqc.client.mcalculus import MCalculus

from UBQCClient import UBQCClient
from UBQCServer import UBQCServer
from utils import print_attributes_M

def main():
    """ Create circuit for the client to execute """
    n = 5

    # Create a QCompute UBQC-style Circuit
    circuit = Circuit(n)

    # MBQC initialization
    for i in range(n):
        circuit.h(i)

    # Add algorithmic gates
    circuit.h(0)
    circuit.cnot([0, 1])
    circuit.h(2)
    circuit.h(3)
    circuit.h(4)

    # Get gate list for functional application
    gate_list = circuit.get_circuit()

    # Add measurements (after saving gate list)
    for i in range(n):
        circuit.measure(i)

    print("Gate list: ", gate_list)

    # --- QCompute Standard Circuit Simulation (Unitary Path) ---
    env = QEnv()
    env.backend(BackendName.LocalBaiduSim2)

    # Create QList circuit (qubits registered in env)
    qlist_circuit = env.Q.createList(n)

    # Apply your UBQC gate list using the compatible utils function
    utils.apply_get_circuit_to_env(gate_list, qlist_circuit)

    # Request state vector output (new API!)
    env.outputState()

    # Commit job
    result = env.commit(shots=1)

    # Access and print quantum state
    state_vector = result['state']
    print("Final quantum state vector:")
    for i, amp in enumerate(state_vector):
        print(f"|{format(i, f'0{n}b')}>: {amp}")

    # --- Brickwork Conversion (UBQC) ---
    print("Start conversion to brickwork")

    mc = MCalculus()
    circuit.simplify_by_merging(True)
    circuit.to_brickwork()
    mc.set_circuit(circuit)
    mc.to_brickwork_pattern()
    mc.standardize()
    bw_pattern = mc.get_pattern()

    # Visualise brickwork graph
    visualiser.plot_brickwork_graph_bfk_format(bw_pattern)

    # Simulate UBQC interaction
    client = UBQCClient(bw_pattern)
    server = UBQCServer(bw_pattern)

    # Step 1: Client sends qubits
    qubit_states = client.prepare_qubits()

    # Step 2: Server entangles brickwork graph
    server.entangle_graph()

    # Step 3: Interactive measurement round
    print("Measurement interaction started")
    for _ in range(len(client.phi) or 1):
        deltas = client.compute_delta()
        raw_results = server.measure_qubits(deltas)
        for ij, raw in raw_results.items():
            corrected = client.correct_result(ij, raw)
            client.outcomes[ij] = corrected
            print(f"Measured qubit {ij}, raw = {raw}, corrected = {corrected}")

    # Step 4: Compare results
    print("Final state vector of regular unitary execution:")
    print(state_vector)

if __name__ == "__main__":
    main()

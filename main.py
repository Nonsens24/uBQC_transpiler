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

    # --- UBQC-style Circuit ---
    circuit = Circuit(n)

    # MBQC initialization
    for i in range(n):
        circuit.h(i)

    # Add gates for algorithm
    circuit.h(0)
    circuit.cnot([0, 1])
    circuit.h(2)
    circuit.h(3)
    circuit.h(4)

    unitary_circuit = circuit

    # Add measurements to support UBQC logic
    for i in range(n):
        circuit.measure(i)

    # Use Qiskit execution of a regular unitary quantum algorithm to compare the outcome of the BQC protocol
    qc, state_vector = utils.QCompute_circuit_to_qiskit_statevector(unitary_circuit)

    # --- Convert to Brickwork for UBQC Execution ---
    print("\nStart conversion to brickwork")

    mc = MCalculus()
    circuit.simplify_by_merging(True)
    circuit.to_brickwork()
    mc.set_circuit(circuit)
    mc.to_brickwork_pattern()
    mc.standardize()
    bw_pattern = mc.get_pattern()

    # Visualise brickwork graph
    visualiser.plot_brickwork_graph_bfk_format(bw_pattern)

    # --- Client-Server UBQC Execution ---
    client = UBQCClient(bw_pattern)
    server = UBQCServer(bw_pattern)

    # Step 1: Client prepares and sends qubits
    qubit_states = client.prepare_qubits()

    # Step 2: Server entangles qubits
    server.entangle_graph()

    # Step 3: Measurement rounds
    print("\nMeasurement interaction started")
    for _ in range(len(client.phi) or 1):
        deltas = client.compute_delta()
        raw_results = server.measure_qubits(deltas)
        for ij, raw in raw_results.items():
            corrected = client.correct_result(ij, raw)
            client.outcomes[ij] = corrected
            print(f"Measured qubit {ij}, raw = {raw}, corrected = {corrected}")

    # Step 4: Compare results
    print("\nFinal quantum state vector of regular unitary execution:")
    print(state_vector)


if __name__ == "__main__":
    main()

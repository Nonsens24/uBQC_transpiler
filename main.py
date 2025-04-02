import networkx as nx
from matplotlib import pyplot as plt

import example_circuits.qft
import visualiser

#Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT

# QCompute
from QCompute import *
from QCompute.OpenService import ModuleErrorCode
from QCompute.QPlatform import Error
from QCompute.OpenService.service_ubqc.client.transpiler import transpile_to_brickwork

from QCompute.OpenService.service_ubqc.client.qobject import Circuit
from QCompute.OpenService.service_ubqc.client.mcalculus import MCalculus

from UBQCClient import UBQCClient
from UBQCServer import UBQCServer
from utils import print_attributes_M


# from mbqc_transpiler.visualization import plot_cluster_state

def main():


    """ Create circuit for the client to execute """
    n = 2

    # Create a 3-qubit circuit
    circuit = Circuit(n)

    # Apply H gate to all qubits (needed for MBQC initialization)
    for i in range(n):
        circuit.h(i)

    # Add more gates to build your algorithm
    circuit.h(0)
    circuit.cnot([0, 1])



    # This version of QCompute doesn't support quantum outputs so has to measure in the end
    circuit.measure(0)
    circuit.measure(1)


    # Convert to brickwork graph using the QCompute library
    mc = MCalculus()
    circuit.simplify_by_merging(True)
    circuit.to_brickwork()
    mc.set_circuit(circuit)
    mc.to_brickwork_pattern()
    mc.standardize()
    bw_pattern = mc.get_pattern()

    # Visualise brickwork graph
    visualiser.plot_brickwork_graph_bfk_format(bw_pattern)

    # See attributes of QCompute commands
    # print_attributes_M(bw_pattern)

    # Assume `pattern = mc.get_pattern()` from earlier MCalculus steps

    client = UBQCClient(bw_pattern)
    server = UBQCServer(bw_pattern)

    # Step 1: Client sends qubits
    qubit_states = client.prepare_qubits()

    # Step 2: Server entangles brickwork graph
    server.entangle_graph()

    # Step 3: Interactive measurement round
    client_outcomes = {}

    print("Measurement interaction started")
    for _ in range(len(client.phi) or 1):  # loop through one layer
        deltas = client.compute_delta()
        raw_results = server.measure_qubits(deltas)
        for ij, raw in raw_results.items():
            corrected = client.correct_result(ij, raw)
            client.outcomes[ij] = corrected
            print(f"Measured qubit {ij}, raw = {raw}, corrected = {corrected}")




if __name__ == "__main__":
    main()

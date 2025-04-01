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

from visualiser import plot_brickwork_graph_from_pattern


# from mbqc_transpiler.visualization import plot_cluster_state

def main():

    #QCompute
    # Define.hubToken = ""
    #
    # env = QEnv()
    # env.backend(BackendName.LocalBaiduSim2)  # Local simulator
    # print("backend loaded")

    n = 4

    # Create a 3-qubit circuit
    circuit = Circuit(n)

    # Apply H gate to all qubits (needed for MBQC initialization)
    for i in range(n):
        circuit.h(i)

    # Add more gates to build your algorithm
    circuit.h(0)
    circuit.cnot([0, 1])
    circuit.h(2)
    circuit.cnot([3, 2])


    #This version doesn't support quantum outputs so has to measure in the end
    circuit.measure(0)
    circuit.measure(1)
    circuit.measure(2)
    circuit.measure(3)


    mc = MCalculus()
    circuit.simplify_by_merging(True)
    circuit.to_brickwork()
    mc.set_circuit(circuit)
    mc.to_brickwork_pattern()
    mc.standardize()
    bw_pattern = mc.get_pattern()

    for cmd in bw_pattern.commands:
        if cmd.__class__.__name__ == "CommandE":
            print(cmd.__dict__)
            break

    visualiser.plot_brickwork_graph_bfk_format(bw_pattern)

    # mc = MCalculus()
    #
    # print("Circuit:", circuit)
    #
    # circuit.simplify_by_merging(True)
    # print("Circuit simplify merging: ", circuit)
    # circuit.to_brickwork()
    # print("Circuit to brickwork: ", circuit)
    # mc.set_circuit(circuit)
    # print("Circuit set circuit mc?: ", circuit)
    # mc.to_brickwork_pattern()
    # print("Converted to brickwork pattern: ", circuit)
    # mc.standardize()
    # print("Standardize")
    # pattern = mc.get_pattern()
    # print("pattern: ", pattern)
    #
    # pattern.print_command_list()


    # # Make such a circuit
    # qc = env.Q.createList(2)
    # H(qc[0])
    # H(qc[1])
    # CZ(qc[0], qc[1])
    #
    # print("circuit created")
    #
    # bw_graph = transpile_to_brickwork(qc)
    #
    # print("Circuit transpiled")
    # print(bw_graph)
    #
    # # Choose a backend and compile
    #
    # # Get optimized DAG
    #
    #
    # #Measure outcome
    # MeasureZ(*env.Q.toListPair())
    # print("Measure Z")
    # taskResult = env.commit(1024, fetchMeasure=True)
    # print("The sample counts are:", taskResult['counts'])
    #
    # #Visualisation qcompute
    # # === Main Execution ===
    # extracted_graph = extract_graph_from_qcompute_circuit(env)
    # visualiser.visualize_graph(extracted_graph)

if __name__ == "__main__":
    main()

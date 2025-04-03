import visualiser
from UBQCClient import UBQCClient
from UBQCServer import UBQCServer
from QCompute.OpenService.service_ubqc.client.qobject import Circuit
from QCompute.OpenService.service_ubqc.client.mcalculus import MCalculus

from math import pi


def simulate_protocol_1(client, server, pattern):
    measured_positions = [cmd.which_qubit for cmd in pattern.commands if cmd.name == 'M']
    for pos in sorted(measured_positions, key=lambda x: (x[1], x[0])):  # col-major order
        # print("posistion: ", pos)
        delta = client.get_delta(pos)
        result = server.measure(pos, delta)
        client.receive_result(pos, result)


def main():

    # 1. Input quantum circuit
    n = 2

    circuit = Circuit(n)
    circuit.h(0)
    circuit.t(1)
    circuit.cnot([0, 1])
    circuit.ry(pi / 2, 1)
    circuit.measure()

    # 2. MBQC brickwork pattern
    circuit.simplify_by_merging()
    circuit.to_brickwork()
    mc = MCalculus()
    mc.set_circuit(circuit)
    mc.to_brickwork_pattern()
    mc.standardize()
    pattern = mc.get_pattern() #MBQC brickwork pattern with actual measurement angles

    # 3. Setup UBQC protocol
    client = UBQCClient(pattern) # Also obscures measurement angles
    server = UBQCServer(pattern)

    # 4. Execute Protocol 1
    simulate_protocol_1(client, server, pattern)

    # 5. Output only the final column of outcomes
    print("\nFinal measurement outcomes (only last column):")
    max_col = max(pos[1] for pos in client.s)
    for pos in sorted(client.s):
        if pos[1] == max_col:
            print("Qubit position: {}, value: {}".format(pos, client.s[pos]))

    # Visualise brickwork graph
    visualiser.plot_brickwork_graph_bfk_format(pattern)

if __name__ == '__main__':
    main()

        # import networkx as nx
# from matplotlib import pyplot as plt
#
# import example_circuits.qft
# import utils
# import visualiser
#
# # Qiskit
# from qiskit import QuantumCircuit, transpile
# from qiskit.circuit.library import QFT
#
# # QCompute
# from QCompute import *
# from QCompute.OpenService.service_ubqc.client.transpiler import transpile_to_brickwork
# from QCompute.OpenService.service_ubqc.client.qobject import Circuit
# from QCompute.OpenService.service_ubqc.client.mcalculus import MCalculus
#
# from UBQCClient import UBQCClient
# from UBQCServer import UBQCServer
# from utils import print_attributes_M
#
#
# def main():
#     """ Create circuit for the client to execute """
#     n = 5
#
#     # --- UBQC-style Circuit ---
#     circuit = Circuit(n)
#
#     # MBQC initialization
#     for i in range(n):
#         circuit.h(i)
#
#     # Add gates for algorithm
#     circuit.h(0)
#     circuit.cnot([0, 1])
#     circuit.h(2)
#     circuit.h(3)
#     circuit.h(4)
#
#     unitary_circuit = circuit
#
#     # Add measurements to support UBQC logic
#     for i in range(n):
#         circuit.measure(i)
#
#     # Use Qiskit execution of a regular unitary quantum algorithm to compare the outcome of the BQC protocol
#     qc, state_vector = utils.QCompute_circuit_to_qiskit_statevector(unitary_circuit)
#
#     # --- Convert to Brickwork for UBQC Execution ---
#     print("\nStart conversion to brickwork")
#
#     mc = MCalculus()
#     circuit.simplify_by_merging(True)
#     circuit.to_brickwork()
#     mc.set_circuit(circuit)
#     mc.to_brickwork_pattern()
#     mc.standardize()
#     bw_pattern = mc.get_pattern() # This pattern only contains MBQC phi' angles
#
#     # Visualise brickwork graph
#     visualiser.plot_brickwork_graph_bfk_format(bw_pattern)
#
#     # --- Client-Server UBQC Execution ---
#     client = UBQCClient(bw_pattern)
#     client.obscure_angles() # Change phi' to deltas in the bw pattern
#
#     # Send fully finished brickwork graph to server
#     server = UBQCServer(bw_pattern)
#
#     # # Step 1: Client prepares and sends qubits
#     qubit_states = client.prepare_qubits() # Just to indicate protocol steps
#
#     # Step 2: Server entangles qubits
#     server.entangle_graph() # Just to indicate protocol steps
#
#     # Step 3: Measurement rounds
#     print("\nMeasurement interaction started")
#
#
#
# if __name__ == "__main__":
#     main()
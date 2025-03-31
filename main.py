from qiskit import QuantumCircuit
from qiskit_aer.backends.compatibility import Statevector
from qiskit import QuantumCircuit, transpile

#Graphix
from graphix import Circuit
import transpiler as tp

import example_circuits.qft
from example_circuits.qft import qft
from transpiler import circuit_to_brickwork


# from mbqc_transpiler.visualization import plot_cluster_state

def main():

    n = 1
    circuit = Circuit(n)

    # Example circuit
    circuit.h(0)
    circuit.z(0)

    # n = 5
    # m = 13  # Example satisfying m ≡ 5 mod 8
    # brickwork_graph = tp.create_brickwork_state(n, m)
    # tp.visualize_brickwork(brickwork_graph)

    circuit = Circuit(2)
    circuit.h(0)
    circuit.cnot(0, 1)

    brickwork_graph = tp.circuit_to_brickwork(circuit)
    tp.visualize_brickwork(brickwork_graph)

    #Qiskit


    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.t(1)

    # Decompose into universal gates explicitly
    basis_gates = ['h', 't', 'cx']
    qc_decomposed = transpile(qc, basis_gates=basis_gates, optimization_level=3)
    print(qc_decomposed)

    circuit_to_brickwork(qc)

    # pattern = circuit.transpile().pattern
    # # pattern.standardize()
    # # pattern.shift_signals()
    #
    # pattern.draw_graph()

if __name__ == "__main__":
    main()

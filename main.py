from qiskit import QuantumCircuit
from qiskit_aer.backends.compatibility import Statevector

#Graphix
from graphix import Circuit

import example_circuits.qft
from example_circuits.qft import qft


# from mbqc_transpiler.visualization import plot_cluster_state

def main():

    n = 1
    circuit = Circuit(n)

    qft(circuit, n)

    pattern = circuit.transpile().pattern
    pattern.standardize()
    pattern.shift_signals()

    pattern.draw_graph()

if __name__ == "__main__":
    main()

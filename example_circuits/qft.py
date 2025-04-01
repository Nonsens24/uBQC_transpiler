import numpy as np

def cp(circuit, theta, control, target):
    circuit.rz(control, theta / 2)
    circuit.rz(target, theta / 2)
    circuit.cnot(control, target)
    circuit.rz(target, -1 * theta / 2)
    circuit.cnot(control, target)


def qft_rotations(circuit, n):
    circuit.h(n)
    for qubit in range(n + 1, circuit.width):
        cp(circuit, np.pi / 2 ** (qubit - n), qubit, n)


def swap_registers(circuit, n):
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)
    return circuit


def qft(circuit, n):
    for i in range(n):
        qft_rotations(circuit, i)
    swap_registers(circuit, n)

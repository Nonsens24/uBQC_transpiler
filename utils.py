from QCompute.OpenService.service_ubqc.client.qobject import Circuit
from QCompute import *

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def print_attributes_M(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "M":
            print(cmd.__dict__)

def print_attributes_N(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "N":
            print(cmd.__dict__)

def print_attributes_E(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "E":
            print(cmd.__dict__)

def print_attributes_C(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "C":
            print(cmd.__dict__)


def QCompute_circuit_to_qiskit_statevector(circuit):
    """Convert QCompute UBQC-style Circuit to Qiskit circuit and simulate the state vector."""
    n = circuit.get_width()
    qc = QuantumCircuit(n)

    for op in circuit.get_circuit():
        name = op[0].lower()
        qubits = op[1]

        if name == 'h':
            qc.h(qubits[0])
        elif name == 'x':
            qc.x(qubits[0])
        elif name == 'y':
            qc.y(qubits[0])
        elif name == 'z':
            qc.z(qubits[0])
        elif name == 's':
            qc.s(qubits[0])
        elif name == 't':
            qc.t(qubits[0])
        elif name == 'sdg':
            qc.sdg(qubits[0])
        elif name == 'tdg':
            qc.tdg(qubits[0])
        elif name == 'rx':
            qc.rx(op[2], qubits[0])
        elif name == 'ry':
            qc.ry(op[2], qubits[0])
        elif name == 'rz':
            qc.rz(op[2], qubits[0])
        elif name == 'cnot':
            qc.cx(qubits[0], qubits[1])
        elif name == 'cz':
            qc.cz(qubits[0], qubits[1])
        elif name == 'm':
            continue  # Skip measurement gates
        else:
            raise NotImplementedError(f"Unsupported gate: {name}")

    # Simulate the final statevector
    final_sv = Statevector.from_instruction(qc)
    return qc, final_sv


def apply_get_circuit_to_env(gate_list: list, qlist: list):
    """
    Applies gates from Circuit.get_circuit() format to QEnv-based qubits.
    """
    for gate in gate_list:
        name = gate[0].lower()
        qubits = gate[1]

        if name == 'h':
            H(qlist[qubits[0]])
        elif name == 'x':
            X(qlist[qubits[0]])
        elif name == 'y':
            Y(qlist[qubits[0]])
        elif name == 'z':
            Z(qlist[qubits[0]])
        elif name == 's':
            S(qlist[qubits[0]])
        elif name == 't':
            T(qlist[qubits[0]])
        elif name == 'sdg':
            SDG(qlist[qubits[0]])
        elif name == 'tdg':
            TDG(qlist[qubits[0]])
        elif name == 'rx':
            RX(qlist[qubits[0]], gate[2])  # angle in meta field
        elif name == 'ry':
            RY(qlist[qubits[0]], gate[2])
        elif name == 'rz':
            RZ(qlist[qubits[0]], gate[2])
        elif name == 'cnot':
            CX(qlist[qubits[0]], qlist[qubits[1]])
        elif name == 'cz':
            CZ(qlist[qubits[0]], qlist[qubits[1]])
        elif name == 'm':
            continue  # Skip measurements for state vector/unitary simulation
        else:
            raise NotImplementedError(f"Gate '{name}' not supported.")

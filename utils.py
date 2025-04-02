from QCompute.OpenService.service_ubqc.client.qobject import Circuit
from QCompute import *


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


from QCompute import *

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

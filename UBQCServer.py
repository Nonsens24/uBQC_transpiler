import random

class UBQCServer:
    def __init__(self, pattern):
        self.pattern = pattern
        self.entangled = False

    def entangle_graph(self):
        # Server applies CZ gates according to pattern structure
        # (handled implicitly by to_brickwork(), so just mark)
        self.entangled = True

    def measure_qubits(self, deltas):
        results = {}
        for cmd in self.pattern.commands:
            if cmd.__dict__['name'] == 'M':
                i, j = cmd.__dict__['which_qubits'][0]
                δ = deltas[(i, j)]
                # Simulate outcome (realistic: use state backend)
                outcome = random.randint(0, 1)  # replace with proper simulation if needed
                results[(i, j)] = outcome
        return results
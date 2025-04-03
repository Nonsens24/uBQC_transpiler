import math

class UBQCServer:
    def __init__(self, pattern):
        self.pattern = pattern
        self.outcomes = {}  # {(x,y): 0 or 1}

    def measure(self, pos, delta):
        """Measure one qubit at pos using angle δ."""
        result = self._simulate_measurement(delta)
        self.outcomes[pos] = result
        return result

    def _simulate_measurement(self, delta):
        """Simulate outcome based on δ (placeholder)."""
        return int(abs(math.sin(delta)) * 10000) % 2







# import random
#
# class UBQCServer:
#     def __init__(self, pattern):
#         self.pattern = pattern
#         self.entangled = False
#
#     def entangle_graph(self):
#         # Server applies CZ gates according to pattern structure
#         # (handled implicitly by to_brickwork(), so just mark)
#         self.entangled = True
#
#     def measure_qubits(self):
#         results = {}
#         for cmd in self.pattern.commands:
#             if cmd.__dict__['name'] == 'M':
#                 i, j = cmd.__dict__['which_qubit']
#
#                 outcome = random.randint(0, 1)  # replace with proper simulation if needed
#                 results[(i, j)] = outcome
#         return results

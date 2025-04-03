import math
import random

class UBQCClient:
    def __init__(self, pattern):
        self.pattern = pattern
        self.phi_angles = {}   # {(x, y): φ} from pattern
        self.theta = {}        # {(x, y): θ}
        self.r = {}            # {(x, y): r}
        self.s = {}            # {(x, y): s outcome received}

        for cmd in self.pattern.commands:
            if cmd.name == 'M':
                pos = cmd.which_qubit
                self.phi_angles[pos] = cmd.angle
                self.theta[pos] = random.choice([k * math.pi / 4 for k in range(8)])
                self.r[pos] = random.choice([0, 1])

                cmd.angle = self.theta[pos] # Change to correct theta angles to be sent to the server

    def get_delta(self, pos):
        """Compute δ_{x,y} for a single qubit."""
        phi_prime = self._apply_dependencies(pos)
        theta = self.theta[pos]
        r = self.r[pos]
        delta = (phi_prime + theta + math.pi * r) % (2 * math.pi)
        return delta

    def receive_result(self, pos, result):
        """Update measurement outcome for a single qubit."""
        self.s[pos] = result

    def _apply_dependencies(self, pos):
        """Apply domain_s and domain_t to get φ'."""
        for cmd in self.pattern.commands:
            if cmd.name == 'M' and cmd.which_qubit == pos:
                phi = self.phi_angles[pos]
                s_domain = sum(self.s.get(q, 0) for q in cmd.domain_s) % 2
                t_domain = sum(self.s.get(q, 0) for q in cmd.domain_t) % 2
                sign = (-1) ** s_domain
                phi_prime = (sign * phi + t_domain * math.pi) % (2 * math.pi)
                return phi_prime
        raise ValueError(f"No measurement command found for {pos}")






# import numpy as np
# import random
#
# class UBQCClient:
#     def __init__(self, pattern):
#         self.pattern = pattern
#         self.theta = {}      # Random angle offsets
#         self.r = {}          # Random bits for hiding results
#         self.phi = {}        # Measurement angles from the pattern
#         self.outcomes = {}   # Corrected measurement outcomes
#
#         # Initialize θ, r, and φ for all measured qubits
#         self._prepare_qubits()
#
#     def _prepare_qubits(self):
#         """
#         Simulates client-side preparation of qubits |+_θ⟩.
#         Populates θ, r, and φ for each measured qubit in the brickwork pattern.
#         """
#         for cmd in self.pattern.commands:
#                 d = cmd.__dict__
#                 if d['name'] == 'M':
#                     i, j = d['which_qubit']  # This is already a tuple like (i, j)
#
#                     theta = random.choice([k * np.pi / 4 for k in range(8)])
#                     r = random.randint(0, 1)
#                     phi = cmd.angle
#
#                     self.theta[(i, j)] = theta
#                     self.r[(i, j)] = r
#                     self.phi[(i, j)] = phi
#
#     def prepare_qubits(self):
#         """
#         Returns the θ values for each qubit.
#         These represent the initial states |+_θ⟩ the client would prepare.
#         """
#         return self.theta
#
#     def compute_delta(self):
#         """
#         Computes δ_ij = φ'_ij + θ_ij + π r_ij
#         """
#         delta = {}
#         for ij in self.phi:
#             phi_prime = self.phi[ij]  # placeholder: φ′ = φ (no dependency correction yet)
#             delta[ij] = phi_prime + self.theta[ij] + self.r[ij] * np.pi
#         return delta
#
#     def obscure_angles(self):
#         """
#         Obscures the brickwork pattern phi' angles and replaces them with deltas
#         """
#         deltas = self.compute_delta()
#
#         for cmd in self.pattern.commands:
#             d = cmd.__dict__
#             if d['name'] == 'M':
#                 # print("bw angle before: ", cmd.angle) #For unit testing
#                 cmd.angle = deltas[d['which_qubit']]
#                 # print("bw angle after delta: {}, from cmd.angle: {}".format(deltas[d['which_qubit']], cmd.angle)) #Unit test to see if they are the same!!!
#
#
#
#     def correct_result(self, ij, raw_result):
#         """
#         Corrects server's raw result by flipping it if r_ij = 1
#         """
#         return raw_result ^ self.r[ij]
#
#

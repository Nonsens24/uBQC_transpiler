# import random
# import numpy as np
#
# class UBQCClient:
#     def __init__(self, pattern):
#         self.pattern = pattern
#         self.theta = {}    # Random phase per qubit
#         self.r = {}        # Random bit flips
#         self.phi = {}      # Target measurement angles from pattern
#         self.delta = {}    # Encrypted angles sent to server
#         self.outcomes = {} # Corrected measurement outcomes
#
#     def prepare_qubits(self):
#         print("preparing r and theta for all qubits")
#         qubits = []
#         for cmd in self.pattern.commands:
#             if cmd.__dict__['name'] == 'N':
#                 ij = cmd.__dict__['which_qubits'][0]
#                 θ = random.choice([k * np.pi/4 for k in range(8)])
#                 r = random.randint(0, 1)
#                 self.theta[ij] = θ
#                 self.r[ij] = r
#                 # Send |+_θ⟩ to Bob (omitted: assumed logical transfer)
#                 qubits.append((ij, θ, r))
#
#         print("Finished preparing r and theta for all qubits")
#         return qubits
#
#     def compute_delta(self):
#         print("Computing deltas")
#         for cmd in self.pattern.commands:
#             d = cmd.__dict__
#             if d['name'] == 'M':
#                 ij = d['which_qubit']  # This is already a tuple like (i, j)
#                 φ = d['angle']
#                 self.phi[ij] = φ
#
#                 domain_s = d.get('domain_s', [])
#                 domain_t = d.get('domain_t', [])
#
#                 sX = sum(self.outcomes.get(dep, 0) for dep in domain_s) % 2
#                 sZ = sum(self.outcomes.get(dep, 0) for dep in domain_t) % 2
#
#                 φ_prime = ((-1) ** sX) * φ + sZ * np.pi
#                 δ = φ_prime + self.theta[ij] + self.r[ij] * np.pi
#                 self.delta[ij] = δ % (2 * np.pi)  # Normalize to [0, 2π)
#
#         print("Finished computing deltas")
#         return self.delta
#
#     def correct_result(self, ij, raw_outcome):
#         if self.r[ij] == 1:
#             return (raw_outcome ^ 1)
#         return raw_outcome
#
#
import numpy as np
import random

class UBQCClient:
    def __init__(self, pattern):
        self.pattern = pattern
        self.theta = {}      # Random angle offsets
        self.r = {}          # Random bits for hiding results
        self.phi = {}        # Measurement angles from the pattern
        self.outcomes = {}   # Corrected measurement outcomes

        # Initialize θ, r, and φ for all measured qubits
        self._prepare_qubits()

    def _prepare_qubits(self):
        """
        Simulates client-side preparation of qubits |+_θ⟩.
        Populates θ, r, and φ for each measured qubit in the brickwork pattern.
        """
        for cmd in self.pattern.commands:
                d = cmd.__dict__
                if d['name'] == 'M':
                    i, j = d['which_qubit']  # This is already a tuple like (i, j)

                    theta = random.choice([k * np.pi / 4 for k in range(8)])
                    r = random.randint(0, 1)
                    phi = cmd.angle

                    self.theta[(i, j)] = theta
                    self.r[(i, j)] = r
                    self.phi[(i, j)] = phi

    def prepare_qubits(self):
        """
        Returns the θ values for each qubit.
        These represent the initial states |+_θ⟩ the client would prepare.
        """
        return self.theta

    def compute_delta(self):
        """
        Computes δ_ij = φ'_ij + θ_ij + π r_ij
        """
        delta = {}
        for ij in self.phi:
            phi_prime = self.phi[ij]  # placeholder: φ′ = φ (no dependency correction yet)
            delta[ij] = phi_prime + self.theta[ij] + self.r[ij] * np.pi
        return delta

    def correct_result(self, ij, raw_result):
        """
        Corrects server's raw result by flipping it if r_ij = 1
        """
        return raw_result ^ self.r[ij]



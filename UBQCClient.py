import random
import numpy as np

class UBQCClient:
    def __init__(self, pattern):
        self.pattern = pattern
        self.theta = {}    # Random phase per qubit
        self.r = {}        # Random bit flips
        self.phi = {}      # Target measurement angles from pattern
        self.delta = {}    # Encrypted angles sent to server
        self.outcomes = {} # Corrected measurement outcomes

    def prepare_qubits(self):
        print("preparing r and theta for all qubits")
        qubits = []
        for cmd in self.pattern.commands:
            if cmd.__dict__['name'] == 'N':
                ij = cmd.__dict__['which_qubits'][0]
                θ = random.choice([k * np.pi/4 for k in range(8)])
                r = random.randint(0, 1)
                self.theta[ij] = θ
                self.r[ij] = r
                # Send |+_θ⟩ to Bob (omitted: assumed logical transfer)
                qubits.append((ij, θ, r))

        print("Finished preparing r and theta for all qubits")
        return qubits

    def compute_delta(self):
        print("Computing deltas")
        for cmd in self.pattern.commands:
            d = cmd.__dict__
            if d['name'] == 'M':
                ij = d['which_qubit']  # This is already a tuple like (i, j)
                φ = d['angle']
                self.phi[ij] = φ

                domain_s = d.get('domain_s', [])
                domain_t = d.get('domain_t', [])

                sX = sum(self.outcomes.get(dep, 0) for dep in domain_s) % 2
                sZ = sum(self.outcomes.get(dep, 0) for dep in domain_t) % 2

                φ_prime = ((-1) ** sX) * φ + sZ * np.pi
                δ = φ_prime + self.theta[ij] + self.r[ij] * np.pi
                self.delta[ij] = δ % (2 * np.pi)  # Normalize to [0, 2π)

        print("Finished computing deltas")
        return self.delta

    def correct_result(self, ij, raw_outcome):
        if self.r[ij] == 1:
            return (raw_outcome ^ 1)
        return raw_outcome

    # def compute_delta(self):
    #     print("Computing deltas")
    #     for cmd in self.pattern.commands:
    #         if cmd.__dict__['name'] == 'M':
    #             ij = cmd.__dict__['which_qubit'][0]
    #             φ = cmd.__dict__['angle']
    #             self.phi[ij] = φ
    #             sX = sum(self.outcomes.get((s.i, s.j), 0) for s in cmd.__dict__['signal_list_x']) % 2
    #             sZ = sum(self.outcomes.get((s.i, s.j), 0) for s in cmd.__dict__['signal_list_z']) % 2
    #             φ_prime = ((-1)**sX) * φ + sZ * np.pi
    #             δ = φ_prime + self.theta[ij] + self.r[ij] * np.pi
    #             self.delta[ij] = δ % (2*np.pi)  # normalize angle
    #     print("Finished computing deltas")
    #     return self.delta


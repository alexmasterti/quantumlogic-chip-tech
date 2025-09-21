from __future__ import annotations
import numpy as np
from .sim_circuit import SearchConfig, build_search_circuit, statevector_probs

def amplitude_estimate(n_qubits: int = 3, target: int = 0b101, shots: int = 1000) -> float:
    cfg = SearchConfig(n_qubits=n_qubits, target=target)
    qc = build_search_circuit(cfg)
    probs = statevector_probs(qc)
    samples = np.random.choice(len(probs), size=shots, p=probs)
    return float((samples == target).mean())

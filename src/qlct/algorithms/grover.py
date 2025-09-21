from __future__ import annotations
from .sim_circuit import SearchConfig, build_search_circuit, statevector_probs

def grover_score(n_qubits: int = 3, target: int = 0b101) -> float:
    cfg = SearchConfig(n_qubits=n_qubits, target=target)
    qc = build_search_circuit(cfg)
    probs = statevector_probs(qc)
    return float(probs[target])

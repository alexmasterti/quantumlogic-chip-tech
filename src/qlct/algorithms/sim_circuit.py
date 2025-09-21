from __future__ import annotations
from dataclasses import dataclass
import numpy as np
try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
except Exception as e:
    raise SystemExit("Qiskit is required. Install with: pip install qiskit") from e

@dataclass
class SearchConfig:
    n_qubits: int = 3
    target: int = 0b101

def build_search_circuit(cfg: SearchConfig) -> QuantumCircuit:
    n = cfg.n_qubits
    t = cfg.target
    qc = QuantumCircuit(n, name="search")
    for q in range(n):
        qc.h(q)
    for q in range(n):
        if ((t >> q) & 1) == 0:
            qc.x(q)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for q in range(n):
        if ((t >> q) & 1) == 0:
            qc.x(q)
    for q in range(n):
        qc.h(q); qc.x(q)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for q in range(n):
        qc.x(q); qc.h(q)
    return qc

def statevector_probs(qc: QuantumCircuit):
    sv = Statevector.from_instruction(qc)
    return abs(sv.data) ** 2

from qlct.algorithms.sim_circuit import SearchConfig, build_search_circuit, statevector_probs
from qlct.algorithms.grover import grover_score
from qlct.algorithms.amp_est import amplitude_estimate
from qlct.pipeline.service import protect_payload, restore_payload

def test_probs_sum():
    cfg = SearchConfig(n_qubits=3, target=0b101)
    qc = build_search_circuit(cfg)
    probs = statevector_probs(qc)
    assert abs(float(probs.sum()) - 1.0) < 1e-9

def test_scores():
    s = grover_score(3, 0b101)
    est = amplitude_estimate(3, 0b101, shots=1000)
    assert 0.0 <= s <= 1.0
    assert 0.0 <= est <= 1.0

def test_roundtrip():
    obj = {"x": 1}
    protected = protect_payload(obj)
    restored = restore_payload(protected["ciphertext_hex"], protected["key"])
    assert restored == obj

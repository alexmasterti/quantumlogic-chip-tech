from __future__ import annotations
import json
from .service import compute_quantum_score, estimate_amplitude, protect_payload, restore_payload
def main():
    sample = {"sensor":"qchip","ts":"2025-09-21T12:00:00Z","data":[1,0,1,0,1]}
    s = compute_quantum_score(3, 0b101)
    est = estimate_amplitude(3, 0b101, 3000)
    protected = protect_payload(sample)
    restored = restore_payload(protected["ciphertext_hex"])
    print(json.dumps({"score": s, "amp_est": est, "protected": protected, "restored": restored}, indent=2))
if __name__ == "__main__":
    main()

from __future__ import annotations
import json
from typing import Dict, Any
from ..algorithms.grover import grover_score
from ..algorithms.amp_est import amplitude_estimate
from ..crypto.pqc_adapter import kem_keypair, kem_encapsulate
from ..crypto.symmetric import xor_encrypt, xor_decrypt

def compute_quantum_score(bits: int, target: int) -> float:
    return grover_score(n_qubits=bits, target=target)
def estimate_amplitude(bits: int, target: int, shots: int = 2000) -> float:
    return amplitude_estimate(n_qubits=bits, target=target, shots=shots)
def protect_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    pk, _ = kem_keypair()
    ct, ss = kem_encapsulate(pk)
    key = ss[:16] if ss else b"quantumlogic-key"
    data = json.dumps(payload).encode()
    ctext = xor_encrypt(data, key)
    return {"ciphertext_hex": ctext.hex(), "kem_ct_len": len(ct), "key_len": len(key), "key": key.hex()}

def restore_payload(ciphertext_hex: str, key_hex: str = None) -> Dict[str, Any]:
    if key_hex:
        key = bytes.fromhex(key_hex)
    else:
        # Fallback for legacy calls - use stub key
        key = b"0123456789abcdef"  # First 16 bytes of stub shared secret
    c = bytes.fromhex(ciphertext_hex)
    p = xor_decrypt(c, key)
    return json.loads(p.decode())

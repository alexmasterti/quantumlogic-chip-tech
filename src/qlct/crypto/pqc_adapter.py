from __future__ import annotations
from typing import Tuple

def kem_keypair() -> Tuple[bytes, bytes]:
    try:
        import oqs
    except Exception:
        return b"stub-public-key", b"stub-secret-key"
    with oqs.KeyEncapsulation("ML-KEM-768") as kem:
        pk = kem.generate_keypair()
        return pk, b""

def kem_encapsulate(pk: bytes) -> Tuple[bytes, bytes]:
    try:
        import oqs
    except Exception:
        ct = b"stub-ciphertext"
        ss = b"0123456789abcdef0123456789abcdef"
        return ct, ss
    with oqs.KeyEncapsulation("ML-KEM-768") as kem:
        ct, ss = kem.encap_secret(pk)
        return ct, ss

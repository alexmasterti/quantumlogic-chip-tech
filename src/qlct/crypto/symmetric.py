from __future__ import annotations
def xor_encrypt(plaintext: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(plaintext)])
def xor_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return xor_encrypt(ciphertext, key)

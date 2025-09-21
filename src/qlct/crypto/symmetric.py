from __future__ import annotations

def xor_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Symmetric encryption using XOR cipher (for demonstration purposes)
    
    XOR encryption is used here for simplicity and educational purposes.
    In production systems, use AES-GCM, ChaCha20-Poly1305, or similar.
    
    How XOR encryption works:
    - Each byte of plaintext is XORed with corresponding key byte
    - Key bytes are repeated cyclically if key is shorter than plaintext
    - XOR is its own inverse: encrypt(decrypt(data)) = data
    
    Args:
        plaintext: Data to encrypt as bytes
        key: Encryption key as bytes (should be random and secret)
        
    Returns:
        Encrypted data as bytes
        
    Example:
        plaintext = b"Hello"
        key = b"key123"
        ciphertext = xor_encrypt(plaintext, key)
        # Each byte: plaintext[i] XOR key[i % len(key)]
    """
    # XOR each plaintext byte with corresponding key byte (cycling through key)
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(plaintext)])

def xor_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Symmetric decryption using XOR cipher
    
    Since XOR is self-inverse, decryption is identical to encryption.
    This property makes XOR convenient for demonstrations.
    
    Args:
        ciphertext: Encrypted data as bytes
        key: Decryption key as bytes (must match encryption key)
        
    Returns:
        Decrypted plaintext as bytes
        
    Mathematical property:
        If C = P ⊕ K (ciphertext = plaintext XOR key)
        Then P = C ⊕ K (plaintext = ciphertext XOR key)
        This is because A ⊕ B ⊕ B = A for any values A, B
    """
    # XOR decryption is identical to XOR encryption due to XOR properties
    return xor_encrypt(ciphertext, key)

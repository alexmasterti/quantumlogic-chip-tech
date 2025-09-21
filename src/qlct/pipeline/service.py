from __future__ import annotations
import json
from typing import Dict, Any

# Import quantum algorithm implementations
from ..algorithms.grover import grover_score                    # Quantum search algorithm
from ..algorithms.amp_est import amplitude_estimate             # Quantum amplitude estimation
# Import post-quantum cryptography functions
from ..crypto.pqc_adapter import kem_keypair, kem_encapsulate  # Post-quantum key exchange
from ..crypto.symmetric import xor_encrypt, xor_decrypt        # Symmetric encryption

def compute_quantum_score(bits: int, target: int) -> float:
    """Service interface for Grover's quantum search algorithm
    
    This function provides a clean API interface to the quantum search
    algorithm, abstracting the quantum circuit details from the web service.
    
    Args:
        bits: Number of qubits (determines search space = 2^bits)
        target: Target state to search for (0 to 2^bits - 1)
        
    Returns:
        Probability of successfully finding the target state
        
    Example:
        compute_quantum_score(3, 5) searches for state |101⟩ in 3-qubit space
        Returns ~0.781 (78.1% success probability with quantum advantage)
    """
    return grover_score(n_qubits=bits, target=target)

def estimate_amplitude(bits: int, target: int, shots: int = 2000) -> float:
    """Service interface for quantum amplitude estimation
    
    Provides API access to quantum amplitude estimation for probability
    analysis, risk assessment, and Monte Carlo acceleration.
    
    Args:
        bits: Number of qubits (state space size)
        target: Target state for amplitude estimation
        shots: Number of measurement samples (accuracy vs. speed trade-off)
        
    Returns:
        Estimated probability of measuring target state
        
    Applications:
        - Financial risk analysis (market event probabilities)
        - Scientific simulation (molecular behavior probabilities)
        - Optimization (solution quality assessment)
    """
    return amplitude_estimate(n_qubits=bits, target=target, shots=shots)

def protect_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt data using post-quantum cryptography
    
    This function demonstrates complete post-quantum encryption workflow:
    1. Generate post-quantum key pair (ML-KEM-768)
    2. Encapsulate shared secret using public key
    3. Use shared secret for symmetric encryption
    4. Return encrypted data + metadata
    
    This approach provides "hybrid" encryption:
    - Asymmetric: Post-quantum key exchange (quantum-resistant)
    - Symmetric: Fast data encryption using derived key
    
    Args:
        payload: Dictionary of data to encrypt (JSON-serializable)
        
    Returns:
        Dictionary containing:
        - ciphertext_hex: Encrypted data as hexadecimal string
        - kem_ct_len: Length of KEM ciphertext
        - key_len: Length of symmetric key used
        - key: Shared secret key (hex) - normally not returned in production
        
    Security Features:
        - Quantum-resistant key exchange (safe against Shor's algorithm)
        - NIST-standardized cryptography (ML-KEM-768)
        - Forward secrecy (new key per encryption)
    """
    # Step 1: Generate post-quantum cryptographic key pair
    pk, _ = kem_keypair()  # pk = public key, secret key managed internally
    
    # Step 2: Encapsulate shared secret using public key
    ct, ss = kem_encapsulate(pk)  # ct = ciphertext, ss = shared secret
    
    # Step 3: Derive symmetric encryption key from shared secret
    key = ss[:16] if ss else b"quantumlogic-key"  # Use first 16 bytes as AES key
    
    # Step 4: Serialize payload to JSON and convert to bytes
    data = json.dumps(payload).encode()  # Convert dict → JSON → bytes
    
    # Step 5: Encrypt data using symmetric cipher (XOR for demo)
    # In production, would use AES-GCM or ChaCha20-Poly1305
    ctext = xor_encrypt(data, key)
    
    # Step 6: Return encrypted result with metadata
    return {
        "ciphertext_hex": ctext.hex(),    # Encrypted data as hex string
        "kem_ct_len": len(ct),           # KEM ciphertext length (for verification)
        "key_len": len(key),             # Symmetric key length
        "key": key.hex()                 # Shared secret (demo only - don't return in prod!)
    }

def restore_payload(ciphertext_hex: str, key_hex: str = None) -> Dict[str, Any]:
    """Decrypt data encrypted with protect_payload()
    
    Reverses the encryption process to recover original payload data.
    In production, the key would be derived from KEM decapsulation.
    
    Args:
        ciphertext_hex: Encrypted data as hexadecimal string
        key_hex: Decryption key as hex (optional, uses fallback if None)
        
    Returns:
        Original payload dictionary
        
    Process:
        1. Convert hex strings back to bytes
        2. Decrypt using symmetric cipher
        3. Deserialize JSON back to dictionary
    """
    # Step 1: Prepare decryption key
    if key_hex:
        key = bytes.fromhex(key_hex)  # Convert hex string to bytes
    else:
        # Fallback for legacy calls - use stub key
        key = b"0123456789abcdef"  # First 16 bytes of stub shared secret
    
    # Step 2: Convert encrypted data from hex to bytes
    c = bytes.fromhex(ciphertext_hex)
    
    # Step 3: Decrypt using symmetric cipher
    p = xor_decrypt(c, key)  # Decrypt to get original JSON bytes
    
    # Step 4: Deserialize JSON back to Python dictionary
    return json.loads(p.decode())  # bytes → string → JSON → dict

from __future__ import annotations
import numpy as np
# Import quantum circuit components for amplitude estimation
from .sim_circuit import SearchConfig, build_search_circuit, statevector_probs

def amplitude_estimate(n_qubits: int = 3, target: int = 0b101, shots: int = 1000) -> float:
    """Quantum Amplitude Estimation using statistical sampling
    
    This algorithm estimates the amplitude (and thus probability) of finding
    a target state in a quantum superposition. It's used for:
    - Risk analysis in financial models
    - Monte Carlo method acceleration  
    - Probability distribution estimation
    
    The algorithm uses the quantum circuit to prepare the state, then
    performs statistical sampling to estimate the target amplitude.
    
    Args:
        n_qubits: Number of quantum bits (determines state space size)
        target: Target state to estimate amplitude for
        shots: Number of measurement samples (higher = more accurate)
        
    Returns:
        Estimated probability of measuring target state
        
    Example:
        For financial risk analysis:
        - Each quantum state represents a market scenario
        - Target state represents a specific risk event
        - Amplitude estimation gives probability of risk event
        - Quantum advantage: faster than classical Monte Carlo
    """
    # Configure quantum circuit for amplitude estimation
    cfg = SearchConfig(n_qubits=n_qubits, target=target)
    
    # Build quantum circuit (same as Grover but used for amplitude estimation)
    qc = build_search_circuit(cfg)
    
    # Get exact probability distribution from quantum simulation
    probs = statevector_probs(qc)
    
    # Simulate quantum measurement process with statistical sampling
    # This mimics real quantum hardware measurement with inherent noise
    samples = np.random.choice(
        len(probs),           # Choose from all possible states (0 to 2^n - 1)
        size=shots,           # Number of measurement shots
        p=probs              # Probability distribution from quantum circuit
    )
    
    # Calculate empirical probability: fraction of measurements = target
    # This estimates the quantum amplitude through statistical sampling
    return float((samples == target).mean())

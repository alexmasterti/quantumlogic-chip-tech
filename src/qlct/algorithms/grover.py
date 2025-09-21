from __future__ import annotations
# Import the quantum circuit simulation components
from .sim_circuit import SearchConfig, build_search_circuit, statevector_probs

def grover_score(n_qubits: int = 3, target: int = 0b101) -> float:
    """Executes Grover's quantum search algorithm and returns success probability
    
    Grover's algorithm provides quadratic speedup for unstructured search:
    - Classical search: O(N) time complexity
    - Grover's search: O(√N) time complexity
    
    Args:
        n_qubits: Number of quantum bits (search space = 2^n states)
        target: Target state in binary format (e.g., 0b101 = state |101⟩)
        
    Returns:
        Probability of measuring the target state after Grover iteration
        
    Example:
        For 3 qubits searching for state |101⟩:
        - Search space: 8 states (000, 001, 010, 011, 100, 101, 110, 111)
        - Classical: ~4 queries average, worst case 8
        - Grover: ~2.4 queries with ~78% success probability
    """
    # Configure the quantum search parameters
    cfg = SearchConfig(n_qubits=n_qubits, target=target)
    
    # Build the complete Grover quantum circuit
    # This includes: superposition + oracle + diffusion operator
    qc = build_search_circuit(cfg)
    
    # Execute quantum simulation to get probability distribution
    probs = statevector_probs(qc)
    
    # Return probability of finding target state
    # probs[target] gives P(measuring target state)
    return float(probs[target])

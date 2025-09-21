from __future__ import annotations
from dataclasses import dataclass
import numpy as np

# Import Qiskit quantum computing framework with error handling
try:
    from qiskit import QuantumCircuit              # Core quantum circuit construction
    from qiskit.quantum_info import Statevector   # Quantum state vector manipulation
except Exception as e:
    raise SystemExit("Qiskit is required. Install with: pip install qiskit") from e

@dataclass
class SearchConfig:
    """Configuration for quantum search algorithms
    
    n_qubits: Number of quantum bits (determines search space size = 2^n)
    target: Binary representation of the target state to find
    """
    n_qubits: int = 3      # Default: 3 qubits = 8 possible states (000 to 111)
    target: int = 0b101    # Default target: binary 101 = decimal 5

def build_search_circuit(cfg: SearchConfig) -> QuantumCircuit:
    """Constructs Grover's quantum search algorithm circuit
    
    This implements the complete Grover algorithm with:
    1. Superposition initialization
    2. Oracle marking (marks target state with phase flip)
    3. Diffusion operator (amplifies marked state amplitude)
    """
    n = cfg.n_qubits  # Extract number of qubits
    t = cfg.target    # Extract target state to search for
    
    # Create quantum circuit with n qubits
    qc = QuantumCircuit(n, name="search")
    
    # STEP 1: Initialize equal superposition of all states
    # Apply Hadamard gates to all qubits: |0⟩ → (|0⟩ + |1⟩)/√2
    for q in range(n):
        qc.h(q)  # Hadamard gate creates superposition
    
    # STEP 2: Oracle implementation - marks target state with phase flip
    # Flip bits that are 0 in target (preparation for controlled operation)
    for q in range(n):
        if ((t >> q) & 1) == 0:  # Check if bit q in target is 0
            qc.x(q)  # Apply X (NOT) gate to flip 0→1
    
    # Apply controlled-Z operation (phase flip for target state)
    qc.h(n - 1)                              # Convert last qubit to computational basis
    qc.mcx(list(range(n - 1)), n - 1)       # Multi-controlled NOT gate
    qc.h(n - 1)                              # Convert back (creates phase flip)
    
    # Restore original bit values (undo bit flips from preparation)
    for q in range(n):
        if ((t >> q) & 1) == 0:  # Undo the X gates applied earlier
            qc.x(q)  # Restore original state
    
    # STEP 3: Diffusion operator - amplifies marked state amplitude
    # This performs inversion about average amplitude
    
    # Transform to |+⟩ state basis for diffusion
    for q in range(n):
        qc.h(q)  # Hadamard transforms computational basis
        qc.x(q)  # Flip all bits (prepares for diffusion)
    
    # Apply controlled phase flip about |000...0⟩ state
    qc.h(n - 1)                              # Prepare control qubit
    qc.mcx(list(range(n - 1)), n - 1)       # Multi-controlled operation
    qc.h(n - 1)                              # Complete phase flip
    
    # Transform back to computational basis
    for q in range(n):
        qc.x(q)  # Undo bit flips
        qc.h(q)  # Final Hadamard transformation
    
    return qc  # Return complete Grover circuit

def statevector_probs(qc: QuantumCircuit):
    """Computes probability distribution from quantum circuit
    
    Args:
        qc: Quantum circuit to analyze
        
    Returns:
        Array of probabilities for each computational basis state
        Index i corresponds to probability of measuring state |i⟩
    """
    # Execute circuit and get quantum state vector
    sv = Statevector.from_instruction(qc)
    
    # Convert complex amplitudes to probabilities: |amplitude|²
    # This gives probability of measuring each basis state
    return abs(sv.data) ** 2

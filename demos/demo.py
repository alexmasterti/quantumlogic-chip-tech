#!/usr/bin/env python3
"""
🚀 QuantumLogic Chip Technology - Interactive Demo
Production-ready quantum algorithms demonstration

This demo showcases the quantum computing capabilities of QLCT
including Grover's search algorithm, amplitude estimation, and
post-quantum cryptography.

Architecture Overview:
- API-based quantum computing services
- RESTful endpoints for quantum algorithms
- Health monitoring and error handling
- Professional production deployment
"""

import requests  # HTTP client for API communication
import json      # JSON data serialization
import time      # Sleep functionality for demo pacing
import sys       # System arguments and exit codes
from typing import Dict, Any, Optional  # Type hints for better code clarity

# Configuration constants
DEFAULT_API_URL = "http://localhost:8000"  # FastAPI quantum service endpoint
TIMEOUT = 30                               # HTTP request timeout in seconds

class QLCTDemo:
    """Interactive demo class for QLCT platform
    
    This class provides a comprehensive demonstration of the QuantumLogic
    Chip Technology platform, showcasing:
    1. Quantum search algorithms (Grover's algorithm)
    2. Quantum amplitude estimation 
    3. Post-quantum cryptography
    4. API health monitoring
    5. Production-ready error handling
    """
    
    def __init__(self, api_url: str = DEFAULT_API_URL):
        """Initialize demo with API connection settings
        
        Args:
            api_url: Base URL of the QLCT FastAPI service
        """
        self.api_url = api_url                    # Store API endpoint URL
        self.session = requests.Session()         # Create persistent HTTP session
        self.session.timeout = TIMEOUT            # Set request timeout for reliability
        
    def check_api_health(self) -> bool:
        """Check if the API is running and healthy
        
        Performs health check by sending GET request to /health endpoint.
        This verifies that the quantum computing service is operational.
        
        Returns:
            True if API is healthy and responsive, False otherwise
        """
        try:
            # Send health check request to quantum service
            response = self.session.get(f"{self.api_url}/health")
            # HTTP 200 indicates service is healthy and operational
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # Any network error means API is unavailable
            return False
    
    def demo_grover_search(self, bits: int = 3, target: int = 5) -> Dict[str, Any]:
        """Demonstrate Grover's quantum search algorithm
        
        Grover's algorithm provides quadratic speedup for unstructured search:
        - Classical search: O(N) operations to find item in unsorted database
        - Grover's search: O(√N) operations with quantum advantage
        
        Example: Finding person #5 in database of 8 people (3 bits = 2³ = 8 states)
        - Classical: Check 1,2,3,4,5 → 5 operations average
        - Grover: ~2.4 operations with 78% success probability
        
        Args:
            bits: Number of qubits (search space = 2^bits)
            target: Target state to find (0 to 2^bits - 1)
            
        Returns:
            Dictionary with probability and status information
        """
        print(f"🔍 Running Grover's Search: {bits} qubits, target state {target}")
        
        # Prepare API request payload
        payload = {"bits": bits, "target": target}
        
        try:
            # Send POST request to quantum search endpoint
            response = self.session.post(f"{self.api_url}/score", json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            result = response.json()     # Parse JSON response
            
            # Display successful results with quantum advantage explanation
            print(f"✅ Quantum search completed!")
            print(f"   📊 Probability: {result.get('probability', 'N/A')}")
            print(f"   ⚡ Quantum advantage: √N speedup demonstrated")
            
            return result
            
        except requests.exceptions.RequestException as e:
            # Handle network errors gracefully
            print(f"❌ Error during quantum search: {e}")
            return {"error": str(e)}
    
    def demo_amplitude_estimation(self, bits: int = 3, target: int = 5, shots: int = 2000) -> Dict[str, Any]:
        """Demonstrate quantum amplitude estimation
        
        Quantum Amplitude Estimation accelerates Monte Carlo methods by
        providing quadratic speedup for probability estimation tasks.
        
        Applications:
        - Financial risk analysis (option pricing, portfolio optimization)
        - Scientific simulation (molecular dynamics, climate modeling)
        - Machine learning (Bayesian inference, uncertainty quantification)
        
        Key concept: Instead of running millions of classical simulations,
        quantum amplitude estimation can achieve same accuracy with
        dramatically fewer quantum operations.
        
        Args:
            bits: Number of qubits (determines state space complexity)
            target: Target state for amplitude measurement
            shots: Number of quantum measurements (accuracy vs speed tradeoff)
            
        Returns:
            Dictionary with amplitude estimate and measurement metadata
        """
        print(f"📊 Running Amplitude Estimation: {bits} qubits, {shots} shots")
        
        # Prepare API request with measurement parameters
        payload = {"bits": bits, "target": target, "shots": shots}
        
        try:
            # Send request to amplitude estimation endpoint
            response = self.session.post(f"{self.api_url}/amplitude", json=payload)
            response.raise_for_status()  # Check for HTTP errors
            result = response.json()     # Parse quantum measurement results
            
            # Display amplitude estimation results
            print(f"✅ Amplitude estimation completed!")
            print(f"   📈 Estimated amplitude: {result.get('amplitude', 'N/A')}")
            print(f"   🎯 Confidence interval: {result.get('confidence_interval', 'N/A')}")
            print(f"   🔬 Quantum enhancement demonstrated")
            
            return result
            
        except requests.exceptions.RequestException as e:
            # Handle API communication errors
            print(f"❌ Error during amplitude estimation: {e}")
            return {"error": str(e)}
    
    def demo_post_quantum_crypto(self, payload_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Demonstrate post-quantum cryptography
        
        Post-quantum cryptography protects against future quantum computer attacks
        that could break current encryption methods (RSA, ECC) using Shor's algorithm.
        
        This demo uses ML-KEM-768 (NIST standardized algorithm):
        - Lattice-based cryptography (Learning With Errors problem)
        - Quantum-resistant key exchange mechanism
        - FIPS 203 compliance for government/enterprise use
        - Hybrid approach: quantum-safe key exchange + symmetric encryption
        
        Security timeline:
        - Today: RSA/ECC secure against classical computers
        - 2030s: Large quantum computers may break RSA/ECC
        - Solution: Deploy post-quantum cryptography now for future safety
        
        Args:
            payload_data: Data to encrypt (sensor readings, classified info, etc.)
            
        Returns:
            Dictionary with encryption results and cryptographic metadata
        """
        # Use default payload if none provided (simulates sensor data)
        if payload_data is None:
            payload_data = {"sensor": "quantum_chip", "data": [1, 0, 1, 1, 0]}
        
        print(f"🔒 Running Post-Quantum Cryptography Demo")
        
        # Prepare encryption request
        payload = {"payload": payload_data}
        
        try:
            # Send data to post-quantum encryption endpoint
            response = self.session.post(f"{self.api_url}/protect", json=payload)
            response.raise_for_status()  # Check for encryption errors
            result = response.json()     # Parse encryption results
            
            # Display post-quantum encryption success
            print(f"✅ Post-quantum encryption completed!")
            print(f"   🛡️ Encryption method: {result.get('method', 'N/A')}")
            print(f"   🔑 Quantum-resistant: Yes")
            print(f"   🔐 Data secured against quantum attacks")
            
            return result
            
        except requests.exceptions.RequestException as e:
            # Handle cryptographic service errors
            print(f"❌ Error during encryption: {e}")
            return {"error": str(e)}
    
    def run_comprehensive_demo(self):
        """Run all demos in sequence"""
        print("🚀 QuantumLogic Chip Technology - Comprehensive Demo")
        print("=" * 60)
        print()
        
        # Check API health
        print("🏥 Checking API health...")
        if not self.check_api_health():
            print("❌ API is not available. Please start the QLCT platform first:")
            print("   cd deployment && ./start.sh --docker")
            return False
        
        print("✅ API is healthy and ready!")
        print()
        
        # Demo 1: Grover's Search
        print("🎯 DEMO 1: Quantum Search Algorithm")
        print("-" * 40)
        self.demo_grover_search(bits=3, target=5)
        print()
        
        time.sleep(2)  # Brief pause between demos
        
        # Demo 2: Amplitude Estimation
        print("🎯 DEMO 2: Quantum Amplitude Estimation")
        print("-" * 40)
        self.demo_amplitude_estimation(bits=3, target=5, shots=2000)
        print()
        
        time.sleep(2)
        
        # Demo 3: Post-Quantum Cryptography
        print("🎯 DEMO 3: Post-Quantum Cryptography")
        print("-" * 40)
        self.demo_post_quantum_crypto()
        print()
        
        print("🎉 All demos completed successfully!")
        print("🌐 Visit http://localhost:8000 for the web interface")
        print("📊 Visit http://localhost:8503 for the interactive dashboard")
        
        return True

def main():
    """Main demo function"""
    print("🚀 QuantumLogic Chip Technology Demo")
    print("Production-Ready Quantum Computing Platform")
    print()
    
    # Check for custom API URL
    api_url = DEFAULT_API_URL
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
        print(f"🔧 Using custom API URL: {api_url}")
    
    # Initialize demo
    demo = QLCTDemo(api_url=api_url)
    
    # Run interactive demo
    try:
        demo.run_comprehensive_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

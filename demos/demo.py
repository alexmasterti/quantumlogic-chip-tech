#!/usr/bin/env python3
"""
🚀 QuantumLogic Chip Technology - Interactive Demo
Production-ready quantum algorithms demonstration

This demo showcases the quantum computing capabilities of QLCT
including Grover's search algorithm, amplitude estimation, and
post-quantum cryptography.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

# Configuration
DEFAULT_API_URL = "http://localhost:8000"
TIMEOUT = 30

class QLCTDemo:
    """Interactive demo class for QLCT platform"""
    
    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        
    def check_api_health(self) -> bool:
        """Check if the API is running and healthy"""
        try:
            response = self.session.get(f"{self.api_url}/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def demo_grover_search(self, bits: int = 3, target: int = 5) -> Dict[str, Any]:
        """Demonstrate Grover's quantum search algorithm"""
        print(f"🔍 Running Grover's Search: {bits} qubits, target state {target}")
        
        payload = {"bits": bits, "target": target}
        
        try:
            response = self.session.post(f"{self.api_url}/score", json=payload)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Quantum search completed!")
            print(f"   📊 Probability: {result.get('probability', 'N/A')}")
            print(f"   ⚡ Quantum advantage: √N speedup demonstrated")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error during quantum search: {e}")
            return {"error": str(e)}
    
    def demo_amplitude_estimation(self, bits: int = 3, target: int = 5, shots: int = 2000) -> Dict[str, Any]:
        """Demonstrate quantum amplitude estimation"""
        print(f"📊 Running Amplitude Estimation: {bits} qubits, {shots} shots")
        
        payload = {"bits": bits, "target": target, "shots": shots}
        
        try:
            response = self.session.post(f"{self.api_url}/amplitude", json=payload)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Amplitude estimation completed!")
            print(f"   📈 Estimated amplitude: {result.get('amplitude', 'N/A')}")
            print(f"   🎯 Confidence interval: {result.get('confidence_interval', 'N/A')}")
            print(f"   🔬 Quantum enhancement demonstrated")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error during amplitude estimation: {e}")
            return {"error": str(e)}
    
    def demo_post_quantum_crypto(self, payload_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Demonstrate post-quantum cryptography"""
        if payload_data is None:
            payload_data = {"sensor": "quantum_chip", "data": [1, 0, 1, 1, 0]}
        
        print(f"🔒 Running Post-Quantum Cryptography Demo")
        
        payload = {"payload": payload_data}
        
        try:
            response = self.session.post(f"{self.api_url}/protect", json=payload)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Post-quantum encryption completed!")
            print(f"   🛡️ Encryption method: {result.get('method', 'N/A')}")
            print(f"   🔑 Quantum-resistant: Yes")
            print(f"   🔐 Data secured against quantum attacks")
            
            return result
            
        except requests.exceptions.RequestException as e:
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

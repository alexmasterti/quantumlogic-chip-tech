import subprocess
import time
import httpx
import json
import sys
import os

def test_api():
    # Start the API server in background
    # Start the API server in background
    print("Starting API server...")
    # Use sys.executable to ensure we use the same python environment
    proc = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'qlct.pipeline.fastapi_app:app', '--host', '0.0.0.0', '--port', '8000'])
    # Poll for server health
    print("Waiting for server to start...")
    base_url = 'http://localhost:8000'
    server_ready = False
    
    for i in range(30):  # Try for 30 seconds
        try:
            with httpx.Client(base_url=base_url, timeout=2.0) as client:
                response = client.get('/health')
                if response.status_code == 200:
                    print("Server is ready!")
                    server_ready = True
                    break
        except:
            time.sleep(1)
            
    if not server_ready:
        print("Server failed to start in time")
        proc.terminate()
        sys.exit(1)

    try:
        # Test endpoints
        print(f"Testing endpoints at {base_url}")
        
        with httpx.Client(base_url=base_url, timeout=10.0) as client:
            # Check health first (already done but good for consistency)
            response = client.get('/health')

            # Test score endpoint
            print("Testing /score...")
            response = client.post('/score', json={'bits': 3, 'target': 5})
            assert response.status_code == 200, f"Score failed: {response.text}"
            data = response.json()
            assert 'score' in data
            print(f'Score endpoint: {data}')
            
            # Test amplitude endpoint  
            print("Testing /amplitude...")
            response = client.post('/amplitude', json={'bits': 3, 'target': 5, 'shots': 1000})
            assert response.status_code == 200, f"Amplitude failed: {response.text}"
            data = response.json()
            assert 'estimated_probability' in data
            print(f'Amplitude endpoint: {data}')
            
            # Test protect endpoint
            print("Testing /protect...")
            response = client.post('/protect', json={'payload': {'test': 'data'}})
            assert response.status_code == 200, f"Protect failed: {response.text}"
            data = response.json()
            assert 'ciphertext_hex' in data
            print(f'Protect endpoint: {data}')
            
        print('All API tests passed!')
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)
        
    finally:
        print("Stopping API server...")
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_api()

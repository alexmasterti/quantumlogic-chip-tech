from __future__ import annotations
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import time
import logging
import os
import requests
from .service import compute_quantum_score, estimate_amplitude, protect_payload, restore_payload

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qlct-api")

def find_streamlit_dashboard():
    """Find the active Streamlit dashboard URL"""
    # Check environment variable first
    env_dashboard = os.getenv('QLCT_DASHBOARD_URL')
    if env_dashboard:
        return env_dashboard
    
    # Common Streamlit ports to check
    ports_to_check = [8501, 8503, 8502, 8504, 8505]
    
    for port in ports_to_check:
        try:
            url = f"http://localhost:{port}"
            # Quick check - Streamlit usually responds with HTML
            response = requests.get(url, timeout=1)
            if response.status_code == 200 and 'streamlit' in response.text.lower():
                return url
        except:
            continue
    
    # Default fallback
    return "http://localhost:8503"

app = FastAPI(
    title="QuantumLogic Chip Technology API", 
    version="1.0.0",
    description="""
    **Production-ready quantum computing and post-quantum cryptography API**
    
    This API provides access to advanced quantum algorithms and secure cryptographic operations:
    
    - 🔍 **Quantum Search**: Grover's algorithm with quadratic speedup
    - 📊 **Amplitude Estimation**: Quantum amplitude estimation with configurable precision  
    - 🔒 **Post-Quantum Crypto**: ML-KEM based encryption for quantum resistance
    - 📈 **Performance Monitoring**: Real-time metrics and analytics
    
    Built for research, development, and production deployment.
    """,
    contact={
        "name": "Alex Costa Souza",
        "email": "research@quantumlogic.tech",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Add basic middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Mount static files
static_path = os.path.join(os.getcwd(), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Simple metrics storage
metrics_store = {
    "total_requests": 0,
    "avg_response_time": 0,
    "endpoint_stats": {}
}

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Simple metrics collection middleware"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Update metrics
    metrics_store["total_requests"] += 1
    
    # Update average response time
    current_avg = metrics_store["avg_response_time"]
    total_requests = metrics_store["total_requests"]
    metrics_store["avg_response_time"] = (
        (current_avg * (total_requests - 1) + process_time) / total_requests
    )
    
    # Update endpoint stats
    path = request.url.path
    if path not in metrics_store["endpoint_stats"]:
        metrics_store["endpoint_stats"][path] = {
            "requests": 0,
            "avg_time": 0,
            "min_time": float('inf'),
            "max_time": 0
        }
    
    endpoint_stats = metrics_store["endpoint_stats"][path]
    endpoint_stats["requests"] += 1
    endpoint_stats["avg_time"] = (
        (endpoint_stats["avg_time"] * (endpoint_stats["requests"] - 1) + process_time) 
        / endpoint_stats["requests"]
    )
    endpoint_stats["min_time"] = min(endpoint_stats["min_time"], process_time)
    endpoint_stats["max_time"] = max(endpoint_stats["max_time"], process_time)
    
    # Add performance header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Enhanced request models with validation
class ScoreRequest(BaseModel):
    bits: int = Field(..., ge=2, le=10, description="Number of qubits (2-10)")
    target: int = Field(..., ge=0, description="Target quantum state to search for")
    
    class Config:
        schema_extra = {
            "example": {
                "bits": 3,
                "target": 5
            }
        }

class AmplitudeRequest(BaseModel):
    bits: int = Field(..., ge=2, le=8, description="Number of qubits (2-8)")
    target: int = Field(..., ge=0, description="Target quantum state")
    shots: int = Field(2000, ge=100, le=10000, description="Number of measurement shots")
    
    class Config:
        schema_extra = {
            "example": {
                "bits": 3,
                "target": 5,
                "shots": 2000
            }
        }

class ProtectRequest(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Data payload to encrypt")
    
    class Config:
        schema_extra = {
            "example": {
                "payload": {
                    "sensor": "qchip_v3",
                    "data": [1, 0, 1, 0, 1],
                    "timestamp": "2025-09-21T12:00:00Z"
                }
            }
        }

class RestoreRequest(BaseModel):
    ciphertext_hex: str = Field(..., description="Hexadecimal encrypted data")
    key_hex: Optional[str] = Field(None, description="Decryption key (hex)")
    
    class Config:
        schema_extra = {
            "example": {
                "ciphertext_hex": "48656c6c6f20576f726c64",
                "key_hex": "30313233343536373839616263646566"
            }
        }

# Add metrics endpoint
@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get API performance metrics"""
    return metrics_store

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Enhanced landing page with logo and dynamic dashboard URL"""
    
    # Get dynamic dashboard URL
    dashboard_url = find_streamlit_dashboard()
    
    # Check if logo exists
    logo_url = None
    if os.path.exists("static/qlct_logo.png"):
        logo_url = "/static/qlct_logo.png"
    elif os.path.exists("qlct_logo.png"):
        logo_url = "/static/qlct_logo.png"  # FastAPI serves from static mount
        
    logo_html = f'<img src="{logo_url}" alt="QLCT Logo" style="max-height: 80px; margin-bottom: 1rem;">' if logo_url else ""
    
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>QuantumLogic Chip Technology</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 2rem;
                    text-align: center;
                }}
                .header {{
                    margin-bottom: 3rem;
                }}
                .header h1 {{
                    font-size: 3rem;
                    margin: 0.5rem 0;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .header p {{
                    font-size: 1.2rem;
                    opacity: 0.9;
                    margin: 1rem 0;
                }}
                .features {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 2rem;
                    margin: 3rem 0;
                }}
                .feature {{
                    background: rgba(255,255,255,0.1);
                    padding: 2rem;
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                }}
                .feature h3 {{
                    margin-top: 0;
                    font-size: 1.5rem;
                }}
                .api-links {{
                    margin: 3rem 0;
                }}
                .btn {{
                    display: inline-block;
                    padding: 12px 24px;
                    margin: 0.5rem;
                    background: rgba(255,255,255,0.2);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    border: 2px solid rgba(255,255,255,0.3);
                    transition: all 0.3s ease;
                    font-weight: 600;
                }}
                .btn:hover {{
                    background: rgba(255,255,255,0.3);
                    border-color: rgba(255,255,255,0.5);
                    transform: translateY(-2px);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    {logo_html}
                    <h1>🚀 QuantumLogic Chip Technology</h1>
                    <p>Advanced Quantum Computing & Post-Quantum Cryptography Platform</p>
                    <p><strong>Production-Ready Quantum Algorithms for America's Technological Leadership</strong></p>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <h3>🔍 Quantum Search</h3>
                        <p>Grover's algorithm implementation with quadratic speedup for database search operations. Demonstrates quantum advantage for intelligence gathering and data analysis.</p>
                    </div>
                    <div class="feature">
                        <h3>📊 Amplitude Estimation</h3>
                        <p>Quantum amplitude estimation for precise probability calculations in financial risk analysis, weather prediction, and market forecasting applications.</p>
                    </div>
                    <div class="feature">
                        <h3>🔒 Post-Quantum Cryptography</h3>
                        <p>ML-KEM based encryption providing quantum-resistant security for government communications, military networks, and critical infrastructure protection.</p>
                    </div>
                    <div class="feature">
                        <h3>📈 Real-time Monitoring</h3>
                        <p>Production-grade monitoring with performance metrics, health checks, and comprehensive analytics for quantum algorithm execution.</p>
                    </div>
                </div>
                
                <div class="api-links">
                    <a href="/docs" class="btn">📖 API Documentation</a>
                    <a href="/health" class="btn">💓 Health Check</a>
                    <a href="/metrics" class="btn">📈 Metrics</a>
                    <a href="{dashboard_url}" class="btn">🖥️ Dashboard</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Comprehensive health check with system status"""
    try:
        # Test quantum computation
        test_score = compute_quantum_score(2, 1)
        quantum_healthy = 0.0 <= test_score <= 1.0
        
        return {
            "status": "healthy" if quantum_healthy else "degraded",
            "service": "qlct-api",
            "version": "1.0.0",
            "timestamp": time.time(),
            "components": {
                "quantum_backend": "qiskit" if quantum_healthy else "error",
                "crypto_backend": "cryptography",
                "api_server": "fastapi"
            },
            "quantum_test": {
                "success": quantum_healthy,
                "test_score": test_score
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")

@app.post("/score", tags=["Quantum Algorithms"])
async def quantum_score(request: ScoreRequest):
    """
    Compute quantum search score using Grover's algorithm
    
    Demonstrates quantum speedup for unstructured search:
    - Classical complexity: O(N) 
    - Quantum complexity: O(√N)
    """
    try:
        # Validate target is within range
        max_target = (2 ** request.bits) - 1
        if request.target > max_target:
            raise HTTPException(
                status_code=400, 
                detail=f"Target {request.target} exceeds maximum for {request.bits} qubits ({max_target})"
            )
        
        start_time = time.time()
        score = compute_quantum_score(request.bits, request.target)
        execution_time = time.time() - start_time
        
        # Calculate theoretical speedup
        classical_ops = 2 ** request.bits // 2
        quantum_ops = int((2 ** request.bits) ** 0.5)
        speedup = classical_ops / quantum_ops if quantum_ops > 0 else 1
        
        return {
            "score": score,
            "execution_time_ms": round(execution_time * 1000, 2),
            "search_space_size": 2 ** request.bits,
            "quantum_advantage": {
                "classical_operations": classical_ops,
                "quantum_operations": quantum_ops,
                "speedup_factor": round(speedup, 2)
            }
        }
    except Exception as e:
        logger.error(f"Quantum score computation failed: {e}")
        raise HTTPException(status_code=500, detail="Quantum computation failed")

@app.post("/amplitude", tags=["Quantum Algorithms"])
async def amplitude_estimation(request: AmplitudeRequest):
    """
    Estimate quantum amplitude with configurable precision
    
    Uses quantum amplitude estimation algorithm to determine the probability
    amplitude of measuring a specific quantum state.
    """
    try:
        # Validate target
        max_target = (2 ** request.bits) - 1
        if request.target > max_target:
            raise HTTPException(
                status_code=400,
                detail=f"Target {request.target} exceeds maximum for {request.bits} qubits ({max_target})"
            )
        
        start_time = time.time()
        probability = estimate_amplitude(request.bits, request.target, request.shots)
        execution_time = time.time() - start_time
        
        # Calculate theoretical error bounds
        theoretical_error = 1 / (request.shots ** 0.5)
        
        return {
            "estimated_probability": probability,
            "shots_used": request.shots,
            "execution_time_ms": round(execution_time * 1000, 2),
            "precision_metrics": {
                "theoretical_error": round(theoretical_error, 6),
                "confidence_level": "~95%",
                "shot_noise_limit": f"1/√{request.shots}"
            }
        }
    except Exception as e:
        logger.error(f"Amplitude estimation failed: {e}")
        raise HTTPException(status_code=500, detail="Amplitude estimation failed")

@app.post("/protect", tags=["Cryptography"])
async def protect_payload(request: ProtectRequest):
    """
    Encrypt payload using post-quantum cryptography
    
    Uses ML-KEM (Kyber) for key encapsulation and symmetric encryption
    for data protection. Provides quantum-resistant security.
    """
    try:
        start_time = time.time()
        result = protect_payload(request.payload)
        execution_time = time.time() - start_time
        
        # Add metadata
        result.update({
            "encryption_time_ms": round(execution_time * 1000, 2),
            "algorithm": "ML-KEM + AES",
            "security_level": "Post-Quantum"
        })
        
        return result
    except Exception as e:
        logger.error(f"Payload protection failed: {e}")
        raise HTTPException(status_code=500, detail="Encryption failed")

@app.post("/restore", tags=["Cryptography"])
async def restore_payload(request: RestoreRequest):
    """
    Decrypt payload using provided key
    
    Restores the original payload from encrypted data using the
    corresponding decryption key.
    """
    try:
        start_time = time.time()
        
        if request.key_hex:
            restored = restore_payload(request.ciphertext_hex, request.key_hex)
        else:
            restored = restore_payload(request.ciphertext_hex)
        
        execution_time = time.time() - start_time
        
        return {
            "restored": restored,
            "decryption_time_ms": round(execution_time * 1000, 2),
            "integrity": "verified"
        }
    except Exception as e:
        logger.error(f"Payload restoration failed: {e}")
        raise HTTPException(status_code=500, detail="Decryption failed")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "available_endpoints": [
                "/docs", "/health", "/metrics", "/score", "/amplitude", "/protect", "/restore"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Please check system health and try again"
        }
    )

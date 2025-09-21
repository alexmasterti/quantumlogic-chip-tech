"""
Advanced FastAPI middleware and monitoring enhancements
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from typing import Dict, Any
import asyncio

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("qlct-api")

class PerformanceMiddleware:
    """Middleware to track API performance metrics"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.metrics: Dict[str, Any] = {
            "total_requests": 0,
            "avg_response_time": 0,
            "endpoint_stats": {}
        }
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = time.time() - start_time
                self.update_metrics(scope["path"], process_time)
                message["headers"].append([b"x-process-time", str(process_time).encode()])
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
    
    def update_metrics(self, path: str, response_time: float):
        self.metrics["total_requests"] += 1
        
        # Update average response time
        current_avg = self.metrics["avg_response_time"]
        total_requests = self.metrics["total_requests"]
        self.metrics["avg_response_time"] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )
        
        # Update endpoint-specific stats
        if path not in self.metrics["endpoint_stats"]:
            self.metrics["endpoint_stats"][path] = {
                "requests": 0,
                "avg_time": 0,
                "min_time": float('inf'),
                "max_time": 0
            }
        
        endpoint_stats = self.metrics["endpoint_stats"][path]
        endpoint_stats["requests"] += 1
        endpoint_stats["avg_time"] = (
            (endpoint_stats["avg_time"] * (endpoint_stats["requests"] - 1) + response_time) 
            / endpoint_stats["requests"]
        )
        endpoint_stats["min_time"] = min(endpoint_stats["min_time"], response_time)
        endpoint_stats["max_time"] = max(endpoint_stats["max_time"], response_time)

class QuantumRateLimiter:
    """Advanced rate limiting for quantum computations"""
    
    def __init__(self, max_requests_per_minute: int = 30):
        self.max_requests = max_requests_per_minute
        self.requests = {}
    
    async def is_allowed(self, client_ip: str) -> bool:
        current_time = time.time()
        minute_window = int(current_time // 60)
        
        if client_ip not in self.requests:
            self.requests[client_ip] = {}
        
        client_requests = self.requests[client_ip]
        
        # Clean old windows
        for window in list(client_requests.keys()):
            if window < minute_window:
                del client_requests[window]
        
        # Check current window
        current_requests = client_requests.get(minute_window, 0)
        
        if current_requests >= self.max_requests:
            return False
        
        client_requests[minute_window] = current_requests + 1
        return True

async def quantum_computation_limiter(request: Request, call_next):
    """Middleware to prevent quantum computation overload"""
    limiter = QuantumRateLimiter()
    client_ip = request.client.host
    
    if request.url.path in ["/score", "/amplitude"]:
        if not await limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded for quantum computations"
            )
    
    response = await call_next(request)
    return response

def setup_enhanced_app(app: FastAPI):
    """Setup enhanced FastAPI with middleware and monitoring"""
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Add performance monitoring
    performance_middleware = PerformanceMiddleware(app)
    app.middleware("http")(performance_middleware)
    
    # Add rate limiting
    app.middleware("http")(quantum_computation_limiter)
    
    # Add metrics endpoint
    @app.get("/metrics")
    async def get_metrics():
        """Get API performance metrics"""
        return performance_middleware.metrics
    
    return app

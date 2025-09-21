"""
Database schema and models for QLCT metrics storage
Optional: For production deployments requiring persistent metrics
"""
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class QuantumExecution(Base):
    """Store quantum algorithm execution metrics"""
    __tablename__ = 'quantum_executions'
    
    id = Column(Integer, primary_key=True)
    algorithm = Column(String(50), nullable=False)  # 'grover', 'amplitude_estimation'
    qubits = Column(Integer, nullable=False)
    target = Column(Integer, nullable=False)
    result = Column(Float, nullable=False)
    execution_time_ms = Column(Float, nullable=False)
    shots = Column(Integer, nullable=True)  # For amplitude estimation
    timestamp = Column(DateTime, default=datetime.utcnow)
    client_ip = Column(String(45), nullable=True)
    
class CryptoOperation(Base):
    """Store cryptographic operation metrics"""
    __tablename__ = 'crypto_operations'
    
    id = Column(Integer, primary_key=True)
    operation = Column(String(20), nullable=False)  # 'encrypt', 'decrypt'
    algorithm = Column(String(50), default='ML-KEM')
    payload_size_bytes = Column(Integer, nullable=False)
    execution_time_ms = Column(Float, nullable=False)
    success = Column(Integer, default=1)  # Boolean as integer
    timestamp = Column(DateTime, default=datetime.utcnow)
    client_ip = Column(String(45), nullable=True)

class APIMetrics(Base):
    """Store general API performance metrics"""
    __tablename__ = 'api_metrics'
    
    id = Column(Integer, primary_key=True)
    endpoint = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    client_ip = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

class SystemHealth(Base):
    """Store system health check results"""
    __tablename__ = 'system_health'
    
    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)  # 'healthy', 'degraded', 'down'
    quantum_backend_status = Column(String(20), nullable=False)
    crypto_backend_status = Column(String(20), nullable=False)
    response_time_ms = Column(Float, nullable=False)
    error_details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database setup functions
def create_database(database_url: str = "sqlite:///qlct_metrics.db"):
    """Create database and tables"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()

# Example usage for production deployments:
"""
# In your FastAPI app:
from .database import create_database, get_session, QuantumExecution

engine = create_database()

@app.post("/score")
async def quantum_score(request: ScoreRequest):
    start_time = time.time()
    score = compute_quantum_score(request.bits, request.target)
    execution_time = (time.time() - start_time) * 1000
    
    # Store metrics
    session = get_session(engine)
    metric = QuantumExecution(
        algorithm='grover',
        qubits=request.bits,
        target=request.target,
        result=score,
        execution_time_ms=execution_time,
        client_ip=request.client.host
    )
    session.add(metric)
    session.commit()
    session.close()
    
    return {"score": score, "execution_time_ms": execution_time}
"""

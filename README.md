# 🚀 QuantumLogic Chip Technology (QLCT)

**Production-Ready Quantum Computing & Post-Quantum Cryptography Platform**  
*Research prototype for NIW endeavor by Alex Costa Souza*

This platform demonstrates advanced quantum algorithms, enterprise-grade software architecture, and production-ready deployment capabilities.

## 📁 **Project Structure**

```
quantumlogic-chip-tech/
├── 📊 presentations/          # Presentation materials & pitch decks
├── 📚 documentation/          # Technical documentation & guides  
├── 🎮 demos/                  # Demo scripts & examples
├── 🐳 deployment/             # Docker & deployment configuration
├── 📦 src/qlct/               # Core quantum algorithms & services
├── 🧪 tests/                  # Test suite
├── 📁 static/                 # Assets & logo files
├── 🗂️ temp/                   # Temporary files
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
└── pyproject.toml            # Project configuration
```

## 🚀 **Quick Start**

### **One-Command Deployment**
```bash
# Navigate to deployment folder
cd deployment

# Start the complete platform
docker compose up --build

# Or use the automated script
./start.sh --docker
```

### **Access Points**
- **🌐 Landing Page:** http://localhost:8000
- **📊 Interactive Dashboard:** http://localhost:8503
- **📖 API Documentation:** http://localhost:8000/docs
- **❤️ Health Check:** http://localhost:8000/health

## 🛠️ **Local Development Setup**

```bash
# Option 1: Automated startup script (RECOMMENDED)
cd deployment
./start.sh

# Option 2: Manual setup
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

# Run tests
pytest -v

# Start FastAPI service
uvicorn qlct.pipeline.fastapi_app:app --reload

# Start Streamlit UI (in another terminal)
streamlit run app.py
```

## 🔧 Smart Configuration

The platform now includes intelligent configuration:

- **Auto-detection**: Automatically finds available API servers
- **Environment support**: Set `QLCT_API_URL` to override defaults
- **Port conflict resolution**: Automatically finds available ports
- **Connection testing**: Real-time API health verification
- **Troubleshooting**: Built-in diagnostics and error resolution

## 🧪 API Testing

```bash
# Test quantum scoring
curl -X POST http://127.0.0.1:8000/score -H "Content-Type: application/json" -d '{"bits":3,"target":5}'

# Test amplitude estimation  
curl -X POST http://127.0.0.1:8000/amplitude -H "Content-Type: application/json" -d '{"bits":3,"target":5,"shots":2000}'

# Test payload encryption
curl -X POST http://127.0.0.1:8000/protect -H "Content-Type: application/json" -d '{"payload":{"sensor":"qchip","data":[1,0,1]}}'
```

## 🏗️ Architecture & Features

### Quantum Algorithms
- **Grover's Algorithm**: Quantum search for unstructured databases
- **Amplitude Estimation**: Quantum amplitude estimation with configurable precision
- **Quantum Circuit Simulation**: Statevector-based probability calculations

### Cryptography & Security  
- **Post-Quantum Cryptography**: ML-KEM integration for quantum-resistant encryption
- **Symmetric Encryption**: XOR-based payload protection
- **Key Encapsulation**: Quantum-safe key establishment

### Production-Ready Infrastructure
- **FastAPI**: Modern, high-performance API with automatic OpenAPI docs
- **Streamlit**: Interactive web UI for algorithm demonstration  
- **Docker**: Containerized deployment for any environment
- **CI/CD**: Automated testing and deployment with GitHub Actions
- **Multi-Python**: Tested on Python 3.9, 3.10, 3.11

## 📋 For USCIS Officers / Technical Reviewers

This project demonstrates advanced software engineering capabilities in quantum computing and cybersecurity:

1. **🔬 Research Impact**: Novel quantum algorithms for practical applications
2. **🏭 Production Quality**: Containerized, tested, and documented like enterprise software  
3. **🔒 National Security**: Post-quantum cryptography implementations
4. **🚀 Scalability**: Microservices architecture with API-first design
5. **🤖 Automation**: Complete CI/CD pipeline with automated testing

**One-Command Demo**: `docker compose up --build` - No complex setup required!

## 📁 Project Structure

```
quantumlogic-chip-tech/
├── src/qlct/                  # Core quantum logic package
│   ├── algorithms/            # Quantum algorithms (Grover, AmpEst)
│   ├── crypto/               # Post-quantum cryptography
│   └── pipeline/             # FastAPI service & pipeline
├── tests/                    # Comprehensive test suite  
├── docs/                     # Technical documentation
├── .github/workflows/        # CI/CD automation
├── Dockerfile.api            # API container
├── Dockerfile.streamlit      # UI container  
├── docker-compose.yml        # Multi-service deployment
└── app.py                    # Streamlit demo application
```

## 🔄 CI/CD Pipeline

- **Continuous Integration**: Tests on every push/PR across Python 3.9-3.11
- **Docker Publishing**: Automatic image builds on tagged releases
- **Quality Assurance**: Linting, testing, and API integration checks
- **Documentation**: Auto-generated API docs and technical specifications

See [README_DOCKER_CI.md](README_DOCKER_CI.md) for detailed deployment instructions.

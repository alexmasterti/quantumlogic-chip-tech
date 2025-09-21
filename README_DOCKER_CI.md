# Docker and CI Guide

## Quick Start with Docker Compose

The easiest way to run the complete QLCT stack is with Docker Compose:

```bash
# Build and run both API and Streamlit UI
docker compose up --build

# Run in background
docker compose up -d --build
```

Then open:
- **Streamlit UI**: http://localhost:8501
- **FastAPI API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Individual Docker Containers

### Run API Only
```bash
# Build API container
docker build -f Dockerfile.api -t qlct-api .

# Run API container
docker run -p 8000:8000 qlct-api
```

### Run UI Only
```bash
# Build UI container  
docker build -f Dockerfile.streamlit -t qlct-ui .

# Run UI container (assumes API at localhost:8000)
docker run -p 8501:8501 -e QLCT_API_BASE=http://host.docker.internal:8000 qlct-ui
```

## GitHub Actions CI/CD

### Continuous Integration (`.github/workflows/ci.yml`)
Automatically runs on every push and PR to main:
- ✅ Tests across Python 3.9, 3.10, 3.11
- ✅ Linting with flake8
- ✅ Unit tests with pytest  
- ✅ API integration tests
- ✅ Multi-version compatibility

### Docker Publishing (`.github/workflows/docker.yml`)
Automatically builds and publishes Docker images on tag pushes:
- 🐳 Builds both API and UI containers
- 📦 Publishes to GitHub Container Registry (GHCR)
- 🧪 Tests Docker Compose deployment
- 🏷️ Semantic versioning with tags

## Production Deployment

### Using Published Images
```bash
# Pull latest images from GHCR
docker pull ghcr.io/alexmasterti/quantumlogic-chip-tech-api:latest
docker pull ghcr.io/alexmasterti/quantumlogic-chip-tech-ui:latest

# Run with published images
docker run -p 8000:8000 ghcr.io/alexmasterti/quantumlogic-chip-tech-api:latest
docker run -p 8501:8501 ghcr.io/alexmasterti/quantumlogic-chip-tech-ui:latest
```

### Environment Variables
- `QLCT_API_BASE`: Base URL for API (default: http://api:8000 in compose, http://localhost:8000 standalone)

## For USCIS Officers / Reviewers

This project demonstrates production-ready software engineering practices:

1. **Containerization**: Anyone can run `docker compose up` without complex setup
2. **Automated Testing**: CI runs comprehensive tests on every change
3. **Multi-environment**: Tested across Python 3.9-3.11 for compatibility  
4. **Production Deployment**: Automated Docker image publishing
5. **Documentation**: Clear setup and usage instructions

The quantum algorithms and cryptography implementations showcase advanced technical skills in emerging technologies relevant to U.S. national interests.

## Development

### Local Development
```bash
# Traditional setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .

# Run services
uvicorn qlct.pipeline.fastapi_app:app --reload
streamlit run app.py
```

### Running Tests
```bash
# Run all tests
pytest -v

# Run with coverage
pip install pytest-cov
pytest --cov=src/qlct --cov-report=html
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐
│   Streamlit UI  │────│   FastAPI API    │────│ Quantum Logic  │
│   (Port 8501)   │    │   (Port 8000)    │    │   Algorithms   │
└─────────────────┘    └──────────────────┘    └────────────────┘
       │                        │                       │
       │                        │                       │
   ┌───▼────┐              ┌────▼────┐             ┌────▼────┐
   │Docker  │              │Docker   │             │ Qiskit  │
   │UI      │              │API      │             │ Crypto  │
   │Image   │              │Image    │             │ Utils   │
   └────────┘              └─────────┘             └─────────┘
```

# 🐳 Deployment

This folder contains all deployment and containerization files for the QuantumLogic Chip Technology platform.

## 🚀 **Deployment Files**

### **Docker Configuration**
- `docker-compose.yml` - **Main deployment configuration**
- `Dockerfile.api` - FastAPI backend container
- `Dockerfile.streamlit` - Streamlit dashboard container

### **Startup Scripts**
- `start.sh` - Automated deployment script with health checks

## 🎯 **Quick Start**

### **One-Command Deployment**
```bash
cd deployment
docker compose up --build
```

### **Local Development**
```bash
cd deployment
./start.sh
```

## 🌐 **Access Points**
After deployment, access the platform at:
- **🌐 Landing Page:** http://localhost:8000
- **📊 Interactive Dashboard:** http://localhost:8503
- **📖 API Documentation:** http://localhost:8000/docs
- **❤️ Health Check:** http://localhost:8000/health

## ⚙️ **Configuration**

### **Environment Variables**
- `QLCT_DASHBOARD_URL` - Override dashboard URL
- `DOCKER_COMPOSE_PROFILES` - Select deployment profiles

### **Port Configuration**
- **8000** - FastAPI backend
- **8503** - Streamlit dashboard (auto-detected)

## 🔧 **Features**
- **Health Checks** - Automatic service monitoring
- **Port Detection** - Smart port conflict resolution
- **Error Recovery** - Graceful failure handling
- **Multi-Environment** - Development and production ready

## 📊 **Monitoring**
- Real-time performance metrics at `/metrics`
- Service health status at `/health`
- Interactive monitoring in Streamlit dashboard

#!/bin/bash

# QuantumLogic Chip Technology Startup Script
# Production-ready deployment automation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_API_PORT=8000
DEFAULT_UI_PORT=8503
VENV_PATH="../.venv"

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "🚀 QuantumLogic Chip Technology (QLCT) Startup"
    echo "Production-Ready Quantum Computing Platform"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    if ! command -v pip &> /dev/null; then
        print_error "pip is required but not installed"
        exit 1
    fi
    
    print_success "Dependencies check passed"
}

setup_venv() {
    echo "🐍 Setting up Python virtual environment..."
    
    if [ ! -d "$VENV_PATH" ]; then
        python3 -m venv "$VENV_PATH"
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    pip install -r ../requirements.txt
    pip install -e ..
    
    print_success "Virtual environment configured"
}

check_ports() {
    local api_port=$1
    local ui_port=$2
    
    if lsof -Pi :$api_port -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port $api_port is already in use"
        return 1
    fi
    
    if lsof -Pi :$ui_port -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port $ui_port is already in use" 
        return 1
    fi
    
    return 0
}

start_api() {
    echo "🔌 Starting FastAPI backend..."
    cd ..
    source "$VENV_PATH/bin/activate"
    uvicorn qlct.pipeline.fastapi_app:app --reload --host 0.0.0.0 --port $DEFAULT_API_PORT &
    API_PID=$!
    cd deployment
    sleep 5
    
    if kill -0 $API_PID 2>/dev/null; then
        print_success "FastAPI backend started (PID: $API_PID)"
        return 0
    else
        print_error "Failed to start FastAPI backend"
        return 1
    fi
}

start_ui() {
    echo "📊 Starting Streamlit UI..."
    cd ..
    source "$VENV_PATH/bin/activate"
    streamlit run app.py --server.port $DEFAULT_UI_PORT --server.address 0.0.0.0 &
    UI_PID=$!
    cd deployment
    sleep 5
    
    if kill -0 $UI_PID 2>/dev/null; then
        print_success "Streamlit UI started (PID: $UI_PID)"
        return 0
    else
        print_error "Failed to start Streamlit UI"
        return 1
    fi
}

start_docker() {
    echo "🐳 Starting with Docker Compose..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is required but not installed"
        exit 1
    fi
    
    # Use docker compose if available, fallback to docker-compose
    if docker compose version &> /dev/null; then
        docker compose up --build
    else
        docker-compose up --build
    fi
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --docker     Start using Docker Compose (recommended)"
    echo "  --local      Start using local Python environment"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --docker     # Start complete platform with Docker"
    echo "  $0 --local      # Start with local Python setup"
    echo "  $0              # Interactive mode"
}

cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
        print_success "FastAPI backend stopped"
    fi
    
    if [ ! -z "$UI_PID" ]; then
        kill $UI_PID 2>/dev/null || true
        print_success "Streamlit UI stopped"
    fi
    
    echo "👋 Goodbye!"
}

# Main execution
main() {
    print_header
    
    case "${1:-}" in
        --docker)
            start_docker
            ;;
        --local)
            check_dependencies
            check_ports $DEFAULT_API_PORT $DEFAULT_UI_PORT || exit 1
            setup_venv
            
            trap cleanup EXIT
            
            start_api || exit 1
            start_ui || exit 1
            
            echo ""
            print_success "🚀 QLCT Platform is running!"
            echo ""
            echo "📍 Access Points:"
            echo "   🌐 Landing Page:    http://localhost:$DEFAULT_API_PORT"
            echo "   📊 Dashboard:       http://localhost:$DEFAULT_UI_PORT"
            echo "   📖 API Docs:        http://localhost:$DEFAULT_API_PORT/docs"
            echo "   ❤️  Health Check:   http://localhost:$DEFAULT_API_PORT/health"
            echo ""
            echo "Press Ctrl+C to stop all services"
            
            wait
            ;;
        --help)
            show_usage
            ;;
        *)
            echo "🚀 QuantumLogic Chip Technology Startup"
            echo ""
            echo "How would you like to start the platform?"
            echo ""
            echo "1) Docker Compose (recommended)"
            echo "2) Local Python environment"
            echo "3) Show help"
            echo ""
            read -p "Choose an option [1-3]: " choice
            
            case $choice in
                1)
                    start_docker
                    ;;
                2)
                    main --local
                    ;;
                3)
                    show_usage
                    ;;
                *)
                    print_error "Invalid option. Use --help for usage information."
                    exit 1
                    ;;
            esac
            ;;
    esac
}

# Run main function with all arguments
main "$@"

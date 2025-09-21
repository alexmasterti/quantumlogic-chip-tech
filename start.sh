#!/bin/bash

# 🚀 QuantumLogic Chip Technology Startup Script
# Automated setup for visual demonstrations

set -e  # Exit on any error

echo "🚀 Starting QuantumLogic Chip Technology Platform..."
echo "======================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the quantumlogic-chip-tech directory"
    exit 1
fi

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is available
    fi
}

# Function to find available port
find_available_port() {
    local base_port=$1
    local port=$base_port
    while ! check_port $port; do
        echo "⚠️  Port $port is in use, trying $((port + 1))..."
        port=$((port + 1))
        if [ $port -gt $((base_port + 10)) ]; then
            echo "❌ Could not find available port after $base_port"
            exit 1
        fi
    done
    echo $port
}

# Check startup method preference
if [ "$1" = "--docker" ] || [ "$1" = "-d" ]; then
    echo "🐳 Starting with Docker..."
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker first."
        exit 1
    fi
    
    # Stop any existing containers
    echo "🧹 Cleaning up existing containers..."
    docker compose down >/dev/null 2>&1 || true
    
    # Build and start
    echo "🔨 Building and starting services..."
    docker compose up --build -d
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 5
    
    # Check API health
    for i in {1..30}; do
        if curl -s http://localhost:8000/health >/dev/null 2>&1; then
            echo "✅ API server is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ API server failed to start within 30 seconds"
            docker compose logs api
            exit 1
        fi
        sleep 1
    done
    
    # Check Streamlit
    for i in {1..30}; do
        if curl -s http://localhost:8501 >/dev/null 2>&1; then
            echo "✅ Streamlit dashboard is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ Streamlit failed to start within 30 seconds"
            docker compose logs ui
            exit 1
        fi
        sleep 1
    done
    
    echo ""
    echo "🎉 SUCCESS! QuantumLogic Platform is running!"
    echo "======================================================="
    echo "📊 Streamlit Dashboard: http://localhost:8501"
    echo "🚀 FastAPI Documentation: http://localhost:8000/docs"
    echo "🏥 API Health Check: http://localhost:8000/health"
    echo ""
    echo "💡 To stop services: docker compose down"
    echo "📋 To view logs: docker compose logs -f"
    
else
    echo "🔧 Starting with local Python environment..."
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    echo "🔌 Activating virtual environment..."
    source .venv/bin/activate
    
    # Install dependencies
    echo "📚 Installing dependencies..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    pip install -q -e .
    
    # Find available ports
    API_PORT=$(find_available_port 8000)
    STREAMLIT_PORT=$(find_available_port 8501)
    
    echo "🌐 Using ports - API: $API_PORT, Streamlit: $STREAMLIT_PORT"
    
    # Set environment variable for API URL
    export QLCT_API_URL="http://127.0.0.1:$API_PORT"
    
    # Start API server in background
    echo "🚀 Starting FastAPI server on port $API_PORT..."
    uvicorn qlct.pipeline.fastapi_app:app --reload --host 127.0.0.1 --port $API_PORT > api.log 2>&1 &
    API_PID=$!
    
    # Wait for API to be ready
    echo "⏳ Waiting for API server..."
    for i in {1..30}; do
        if curl -s http://127.0.0.1:$API_PORT/health >/dev/null 2>&1; then
            echo "✅ API server is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ API server failed to start"
            cat api.log
            kill $API_PID 2>/dev/null || true
            exit 1
        fi
        sleep 1
    done
    
    # Start Streamlit
    echo "📊 Starting Streamlit dashboard on port $STREAMLIT_PORT..."
    echo ""
    echo "🎉 QuantumLogic Platform is starting!"
    echo "======================================================="
    echo "📊 Streamlit Dashboard: http://localhost:$STREAMLIT_PORT"
    echo "🚀 FastAPI Documentation: http://localhost:$API_PORT/docs"
    echo "🏥 API Health Check: http://localhost:$API_PORT/health"
    echo ""
    echo "💡 Press Ctrl+C to stop all services"
    echo ""
    
    # Function to cleanup on exit
    cleanup() {
        echo ""
        echo "🧹 Shutting down services..."
        kill $API_PID 2>/dev/null || true
        echo "✅ Cleanup complete!"
        exit 0
    }
    
    # Set trap for cleanup
    trap cleanup SIGINT SIGTERM
    
    # Start Streamlit (foreground)
    streamlit run app.py --server.port $STREAMLIT_PORT --server.headless false
fi

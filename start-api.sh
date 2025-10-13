#!/bin/bash

# 🚀 REST API Startup Script
# Starts the API server with authentication

set -e

echo "🚀 Starting Secure REST API..."
echo "================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating virtual environment...${NC}"
source venv/bin/activate

# Install/upgrade dependencies
echo -e "${BLUE}📥 Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r api/requirements.txt

# Generate SECRET_KEY if not set
if [ -z "$SECRET_KEY" ]; then
    echo -e "${YELLOW}⚠️  SECRET_KEY not set - generating one...${NC}"
    export SECRET_KEY=$(openssl rand -hex 32)
    echo -e "${GREEN}✅ Generated SECRET_KEY: $SECRET_KEY${NC}"
    echo ""
    echo -e "${YELLOW}💡 For production, set this in your environment:${NC}"
    echo "   export SECRET_KEY=\"$SECRET_KEY\""
fi

# Check if port 8000 is available
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use${NC}"
    echo "Killing existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

echo ""
echo -e "${GREEN}✅ All checks passed!${NC}"
echo ""
echo "================================"
echo -e "${GREEN}🎯 API Starting...${NC}"
echo "================================"
echo ""
echo -e "${BLUE}📍 API will be available at:${NC}"
echo "   🌐 http://localhost:8000"
echo "   📚 Docs: http://localhost:8000/docs"
echo "   📖 ReDoc: http://localhost:8000/redoc"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the API server
cd "$(dirname "$0")"
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload


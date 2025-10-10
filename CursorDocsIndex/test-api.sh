#!/bin/bash
# 🧪 Test Docs-Agent API Server Locally

echo "🧪 Testing Docs-Agent API Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start server in background
echo "🚀 Starting API server..."
source venv/bin/activate
python api_server.py &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Test endpoints
echo ""
echo "━━━ Testing Endpoints ━━━"
echo ""

echo "1️⃣  Health Check:"
curl -s http://localhost:8000/health | python -m json.tool
echo ""

echo ""
echo "2️⃣  Stats:"
curl -s http://localhost:8000/stats | python -m json.tool
echo ""

echo ""
echo "3️⃣  Search:"
curl -s "http://localhost:8000/search?q=authentication&top_k=3" | python -m json.tool
echo ""

echo ""
echo "4️⃣  Lookup:"
curl -s "http://localhost:8000/lookup?q=rate%20limiting" | python -m json.tool
echo ""

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Tests complete!"
echo ""
echo "📖 Swagger docs available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "🛑 To stop server:"
echo "   kill $SERVER_PID"
echo ""
echo "Press Ctrl+C to stop server and exit..."

# Wait for user interrupt
wait $SERVER_PID


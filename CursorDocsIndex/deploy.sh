#!/bin/bash
# 🚀 Docs-Agent Cloud Deployment Script

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 Docs-Agent Cloud Deployment 🚀                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "api_server.py" ]; then
    echo "❌ Error: Run this from ~/CursorDocsIndex/"
    exit 1
fi

echo "Choose deployment platform:"
echo "1) Railway (Recommended - easiest)"
echo "2) Render"
echo "3) Docker local test"
echo "4) Fly.io"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚂 Deploying to Railway..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Check if railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo "📦 Installing Railway CLI..."
            npm install -g @railway/cli
        fi
        
        echo "✅ Railway CLI installed"
        echo ""
        echo "📋 Next steps:"
        echo "1. Login to Railway:"
        echo "   railway login"
        echo ""
        echo "2. Initialize project:"
        echo "   railway init"
        echo ""
        echo "3. Deploy:"
        echo "   railway up"
        echo ""
        echo "4. Set environment variables in Railway dashboard:"
        echo "   - DOCS_API_KEY (for authentication)"
        echo "   - OPENROUTER_API_KEY (optional, for semantic search)"
        echo ""
        echo "5. Your API will be at:"
        echo "   https://your-project.railway.app"
        echo ""
        ;;
    
    2)
        echo ""
        echo "🎨 Deploying to Render..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "📋 Steps:"
        echo "1. Push code to GitHub:"
        echo "   git init"
        echo "   git add ."
        echo "   git commit -m 'Docs-Agent API'"
        echo "   gh repo create docs-agent-api --private --source=. --push"
        echo ""
        echo "2. Go to: https://render.com"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Connect your GitHub repo"
        echo "5. Render will auto-detect render.yaml"
        echo "6. Click 'Create Web Service'"
        echo ""
        echo "7. Set environment variables:"
        echo "   - DOCS_API_KEY"
        echo "   - OPENROUTER_API_KEY (optional)"
        echo ""
        echo "✅ render.yaml already configured!"
        ;;
    
    3)
        echo ""
        echo "🐳 Testing Docker locally..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Build Docker image
        echo "🔨 Building Docker image..."
        docker build -t docs-agent-api .
        
        echo ""
        echo "✅ Image built successfully!"
        echo ""
        echo "🚀 Starting container..."
        docker run -d \
            --name docs-agent-api \
            -p 8000:8000 \
            -v "$(pwd)/index:/app/index" \
            -e DOCS_API_KEY="${DOCS_API_KEY:-test-key}" \
            docs-agent-api
        
        echo ""
        echo "✅ Container started!"
        echo ""
        echo "📊 Access your API:"
        echo "   http://localhost:8000"
        echo "   http://localhost:8000/docs (Swagger UI)"
        echo ""
        echo "🧪 Test it:"
        echo "   curl http://localhost:8000/health"
        echo "   curl http://localhost:8000/stats"
        echo ""
        echo "🛑 Stop container:"
        echo "   docker stop docs-agent-api"
        echo "   docker rm docs-agent-api"
        ;;
    
    4)
        echo ""
        echo "🪁 Deploying to Fly.io..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Check if flyctl is installed
        if ! command -v flyctl &> /dev/null; then
            echo "📦 Installing Fly CLI..."
            curl -L https://fly.io/install.sh | sh
            echo 'export FLYCTL_INSTALL="$HOME/.fly"' >> ~/.zshrc
            echo 'export PATH="$FLYCTL_INSTALL/bin:$PATH"' >> ~/.zshrc
        fi
        
        echo "📋 Next steps:"
        echo "1. Login to Fly:"
        echo "   flyctl auth login"
        echo ""
        echo "2. Launch app:"
        echo "   flyctl launch"
        echo ""
        echo "3. Set secrets:"
        echo "   flyctl secrets set DOCS_API_KEY=your-key"
        echo "   flyctl secrets set OPENROUTER_API_KEY=your-key"
        echo ""
        echo "4. Deploy:"
        echo "   flyctl deploy"
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              📚 Deployment Guide Ready! 📚                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 See CLOUD-DEPLOYMENT.md for detailed instructions"
echo "🔐 Don't forget to set API keys in your deployment platform!"
echo ""


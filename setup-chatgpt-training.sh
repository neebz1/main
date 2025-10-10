#!/bin/bash
# Setup script for ChatGPT Model Training
# This script sets up your environment and runs a test training

set -e  # Exit on error

echo "========================================="
echo "🤖 ChatGPT Model Training Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Check if Python 3.8+
required_version="3.8"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}❌ Python 3.8 or higher required${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python version OK${NC}"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "chatgpt_training_env" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
    read -p "   Remove and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf chatgpt_training_env
        python3 -m venv chatgpt_training_env
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        echo "   Using existing environment"
    fi
else
    python3 -m venv chatgpt_training_env
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source chatgpt_training_env/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✅ Pip upgraded${NC}"
echo ""

# Install requirements
echo "📦 Installing requirements (this may take a few minutes)..."
if [ -f "requirements_chatgpt_training.txt" ]; then
    pip install -r requirements_chatgpt_training.txt --quiet
    echo -e "${GREEN}✅ Requirements installed${NC}"
else
    echo -e "${RED}❌ requirements_chatgpt_training.txt not found${NC}"
    exit 1
fi
echo ""

# Check for GPU
echo "🎮 Checking for GPU..."
python3 -c "import torch; print('GPU Available:', torch.cuda.is_available()); print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')" 2>/dev/null || echo "PyTorch not installed correctly"
echo ""

# Ask if user wants to run test training
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
read -p "🚀 Run test training on example data? (Y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "🏋️  Starting test training..."
    echo "   This will train a small model on example data"
    echo "   Takes about 5-15 minutes depending on your hardware"
    echo ""
    
    if [ -f "example_chatgpt_data.json" ] && [ -f "train_chatgpt_model.py" ]; then
        python3 train_chatgpt_model.py \
            --data example_chatgpt_data.json \
            --model gpt2 \
            --epochs 2 \
            --batch-size 2 \
            --max-length 256 \
            --output ./test-chatbot
        
        echo ""
        echo "========================================="
        echo -e "${GREEN}✅ Test training complete!${NC}"
        echo "========================================="
        echo ""
        echo "🎉 Your test model is ready!"
        echo ""
        echo "Try it out:"
        echo "  python3 demo_chatbot.py ./test-chatbot"
        echo ""
    else
        echo -e "${RED}❌ Training files not found${NC}"
    fi
else
    echo ""
    echo "========================================="
    echo "✅ Setup Complete!"
    echo "========================================="
    echo ""
fi

# Show next steps
echo "📚 Next Steps:"
echo ""
echo "1. Test the chatbot:"
echo "   python3 demo_chatbot.py ./test-chatbot"
echo ""
echo "2. Train with your own data:"
echo "   python3 convert_chatgpt_export.py conversations.json my_data.json"
echo "   python3 train_chatgpt_model.py --data my_data.json"
echo ""
echo "3. Read the guides:"
echo "   - README-CHATGPT-TRAINING.md (start here)"
echo "   - QUICK-START-CHATGPT-TRAINING.md (quick guide)"
echo "   - HUGGINGFACE-TRAINING-GUIDE.md (complete guide)"
echo ""
echo "🎓 To activate the environment in the future:"
echo "   source chatgpt_training_env/bin/activate"
echo ""
echo "Happy training! 🚀🤖"


#!/bin/bash
# Launch Advanced AI Development Environment
# Starts all services and provides interactive menu

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🚀 ADVANCED AI DEVELOPMENT ENVIRONMENT 🚀            ║
║                                                           ║
║     Elite AI Development Tools                           ║
║     Used by <1000 developers worldwide                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This environment is designed for macOS${NC}"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo -e "${GREEN}🐍 Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo -e "${YELLOW}   Run: python3.11 -m venv venv${NC}"
    echo -e "${YELLOW}   Then: source venv/bin/activate && pip install -r requirements_advanced_ai_dev.txt${NC}"
fi

# Start services
start_services() {
    echo -e "\n${BLUE}🚀 Starting AI services...${NC}"
    
    # Redis
    if command -v redis-server &> /dev/null; then
        echo -e "${GREEN}  ✓ Starting Redis...${NC}"
        brew services start redis 2>/dev/null || redis-server --daemonize yes
    fi
    
    # PostgreSQL
    if command -v postgres &> /dev/null; then
        echo -e "${GREEN}  ✓ Starting PostgreSQL...${NC}"
        brew services start postgresql@15 2>/dev/null || true
    fi
    
    # Ollama
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}  ✓ Starting Ollama...${NC}"
        brew services start ollama 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✅ Services started${NC}"
}

# Stop services
stop_services() {
    echo -e "\n${BLUE}🛑 Stopping AI services...${NC}"
    
    brew services stop redis 2>/dev/null || true
    brew services stop postgresql@15 2>/dev/null || true
    brew services stop ollama 2>/dev/null || true
    
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Check status
check_status() {
    echo -e "\n${BLUE}📊 System Status${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    
    if [ -d "venv" ]; then
        python advanced_ai_cli.py status
    else
        echo -e "${RED}Virtual environment not found${NC}"
    fi
}

# Interactive menu
show_menu() {
    echo -e "\n${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                    MAIN MENU                              ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo -e ""
    echo -e "  ${GREEN}1.${NC} 🎯 Start All Services"
    echo -e "  ${GREEN}2.${NC} 📊 Check System Status"
    echo -e "  ${GREEN}3.${NC} 🤖 Launch Interactive Agent"
    echo -e "  ${GREEN}4.${NC} 🔍 Analyze Code (Current Directory)"
    echo -e "  ${GREEN}5.${NC} 🚀 Serve Model"
    echo -e "  ${GREEN}6.${NC} 🔧 Fine-Tune Model"
    echo -e "  ${GREEN}7.${NC} 📈 Monitor System"
    echo -e "  ${GREEN}8.${NC} 🧪 Run Demos"
    echo -e "  ${GREEN}9.${NC} 🛑 Stop All Services"
    echo -e "  ${GREEN}0.${NC} 🚪 Exit"
    echo -e ""
    echo -e -n "${YELLOW}Select option [0-9]: ${NC}"
}

# Launch agent
launch_agent() {
    echo -e "\n${BLUE}🤖 Available Agents:${NC}"
    echo -e "  1. Architect - System design and architecture"
    echo -e "  2. Researcher - Research and analysis"
    echo -e "  3. Coder - Code implementation"
    echo -e "  4. Reviewer - Code review"
    echo -e "  5. Optimizer - Performance optimization"
    echo -e ""
    echo -e -n "${YELLOW}Select agent [1-5]: ${NC}"
    read agent_choice
    
    case $agent_choice in
        1) agent_name="Architect" ;;
        2) agent_name="Researcher" ;;
        3) agent_name="Coder" ;;
        4) agent_name="Reviewer" ;;
        5) agent_name="Optimizer" ;;
        *) echo -e "${RED}Invalid choice${NC}"; return ;;
    esac
    
    echo -e "${GREEN}Launching ${agent_name}...${NC}"
    python advanced_ai_cli.py agent-run "$agent_name" --interactive
}

# Serve model
serve_model() {
    echo -e "\n${BLUE}🚀 Available Models:${NC}"
    echo -e "  1. llama2:70b (Large, slow, accurate)"
    echo -e "  2. codellama:34b (Code-optimized)"
    echo -e "  3. mistral:latest (Fast, good quality)"
    echo -e "  4. neural-chat (Chat-optimized)"
    echo -e ""
    echo -e -n "${YELLOW}Select model [1-4]: ${NC}"
    read model_choice
    
    case $model_choice in
        1) model="llama2:70b" ;;
        2) model="codellama:34b" ;;
        3) model="mistral:latest" ;;
        4) model="neural-chat" ;;
        *) echo -e "${RED}Invalid choice${NC}"; return ;;
    esac
    
    echo -e "${GREEN}Serving ${model}...${NC}"
    python advanced_ai_cli.py serve "$model" --port 8000 --gpu
}

# Run demos
run_demos() {
    echo -e "\n${BLUE}🧪 Available Demos:${NC}"
    echo -e "  1. Agent System Demo"
    echo -e "  2. Model Serving Demo"
    echo -e "  3. Fine-Tuning Demo"
    echo -e "  4. Code Intelligence Demo"
    echo -e "  5. Monitoring Demo"
    echo -e "  6. Experimental Tools Demo"
    echo -e ""
    echo -e -n "${YELLOW}Select demo [1-6]: ${NC}"
    read demo_choice
    
    case $demo_choice in
        1) python advanced_ai_tools/advanced_agent_system.py ;;
        2) python advanced_ai_tools/model_serving_advanced.py ;;
        3) python advanced_ai_tools/fine_tuning_system.py ;;
        4) python advanced_ai_tools/code_intelligence.py ;;
        5) python advanced_ai_tools/ai_monitoring_system.py ;;
        6) python advanced_ai_tools/experimental_tools.py ;;
        *) echo -e "${RED}Invalid choice${NC}" ;;
    esac
}

# Main loop
while true; do
    show_menu
    read choice
    
    case $choice in
        1) start_services ;;
        2) check_status ;;
        3) launch_agent ;;
        4) 
            echo -e "${GREEN}Analyzing code...${NC}"
            python advanced_ai_cli.py code-analyze . --deep
            ;;
        5) serve_model ;;
        6) 
            echo -e "${YELLOW}Enter base model (e.g., meta-llama/Llama-2-7b-hf): ${NC}"
            read base_model
            echo -e "${YELLOW}Enter dataset path: ${NC}"
            read dataset_path
            python advanced_ai_cli.py finetune "$base_model" "$dataset_path"
            ;;
        7) python advanced_ai_cli.py monitor ;;
        8) run_demos ;;
        9) stop_services ;;
        0) 
            echo -e "\n${GREEN}👋 Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac
    
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
done


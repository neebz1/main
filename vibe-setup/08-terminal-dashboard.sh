#!/usr/bin/env bash
# 📊 Terminal Dashboard Setup - System, Mood & AI Load Monitoring

set -e

echo "📊 Setting up terminal dashboard..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create dashboard directory
mkdir -p "$HOME/.config/vibe-coding/dashboard"

# ━━━ Fastfetch Configuration (System Info) ━━━
echo "📝 Configuring fastfetch..."

mkdir -p "$HOME/.config/fastfetch"

cat > "$HOME/.config/fastfetch/config.jsonc" << 'EOF'
{
  "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
  "logo": {
    "type": "auto",
    "padding": {
      "top": 1,
      "left": 2
    }
  },
  "display": {
    "separator": " → ",
    "color": {
      "keys": "magenta",
      "title": "cyan"
    }
  },
  "modules": [
    {
      "type": "title",
      "format": "{#cyan}🎨 Vibe Coding Environment{#}"
    },
    "break",
    {
      "type": "os",
      "key": "  OS",
      "keyColor": "blue"
    },
    {
      "type": "host",
      "key": " 󰇄 Host",
      "keyColor": "blue"
    },
    {
      "type": "kernel",
      "key": "  Kernel",
      "keyColor": "blue"
    },
    {
      "type": "uptime",
      "key": "  Uptime",
      "keyColor": "blue"
    },
    "break",
    {
      "type": "shell",
      "key": "  Shell",
      "keyColor": "green"
    },
    {
      "type": "terminal",
      "key": "  Term",
      "keyColor": "green"
    },
    {
      "type": "terminalfont",
      "key": "  Font",
      "keyColor": "green"
    },
    "break",
    {
      "type": "cpu",
      "key": " 󰻠 CPU",
      "keyColor": "yellow"
    },
    {
      "type": "gpu",
      "key": " 󰍛 GPU",
      "keyColor": "yellow"
    },
    {
      "type": "memory",
      "key": "  RAM",
      "keyColor": "yellow"
    },
    {
      "type": "disk",
      "key": "  Disk",
      "keyColor": "yellow"
    },
    "break",
    {
      "type": "battery",
      "key": "  Battery",
      "keyColor": "red"
    },
    {
      "type": "localip",
      "key": "  Local IP",
      "keyColor": "red"
    },
    "break",
    {
      "type": "colors",
      "paddingLeft": 2,
      "symbol": "circle"
    }
  ]
}
EOF

# ━━━ Vibe Dashboard Script ━━━
cat > "$HOME/.config/vibe-coding/dashboard/vibe-dashboard.sh" << 'EOF'
#!/usr/bin/env bash
# 🎨 Vibe Coding Dashboard - Complete System Overview

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Mood emojis based on time
get_mood() {
    hour=$(date +%H)
    
    if [ "$hour" -ge 5 ] && [ "$hour" -lt 12 ]; then
        echo "🌅 Morning Vibes"
    elif [ "$hour" -ge 12 ] && [ "$hour" -lt 17 ]; then
        echo "☀️ Afternoon Flow"
    elif [ "$hour" -ge 17 ] && [ "$hour" -lt 21 ]; then
        echo "🌆 Evening Code"
    else
        echo "🌙 Night Owl Mode"
    fi
}

# Check AI tool status
check_ai_status() {
    local status=""
    
    [ -n "$OPENROUTER_API_KEY" ] && status="${status}✅ OpenRouter  " || status="${status}❌ OpenRouter  "
    [ -n "$OPENAI_API_KEY" ] && status="${status}✅ OpenAI  " || status="${status}❌ OpenAI  "
    [ -n "$ANTHROPIC_API_KEY" ] && status="${status}✅ Anthropic  " || status="${status}❌ Anthropic  "
    [ -n "$HF_TOKEN" ] && status="${status}✅ HuggingFace" || status="${status}❌ HuggingFace"
    
    echo "$status"
}

# Check running services
check_services() {
    local services=""
    
    pgrep -x "Cursor" > /dev/null && services="${services}🎯 Cursor  "
    pgrep -x "Docker" > /dev/null && services="${services}🐋 Docker  "
    pgrep -x "Spotify" > /dev/null && services="${services}🎵 Spotify  "
    pgrep -x "Logic Pro" > /dev/null && services="${services}🎹 Logic  "
    
    [ -z "$services" ] && services="None running"
    echo "$services"
}

# Get CPU and Memory usage
get_system_load() {
    # CPU usage
    cpu=$(ps -A -o %cpu | awk '{s+=$1} END {print s}')
    cpu_rounded=$(printf "%.0f" $cpu)
    
    # Memory usage
    mem=$(vm_stat | grep "Pages active" | awk '{print $3}' | sed 's/\.//')
    mem_total=$(sysctl -n hw.memsize)
    mem_percent=$(echo "scale=1; $mem * 4096 / $mem_total * 100" | bc)
    
    echo "CPU: ${cpu_rounded}% | RAM: ${mem_percent}%"
}

# Main dashboard
clear

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}          ${PURPLE}🎨 Vibe Coding Dashboard${NC}                        ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Mood & Time
echo -e "${YELLOW}⏰ $(date '+%A, %B %d, %Y - %H:%M:%S')${NC}"
echo -e "${PURPLE}💭 $(get_mood)${NC}"
echo ""

# System Info
echo -e "${CYAN}━━━ System Status ━━━${NC}"
fastfetch --config ~/.config/fastfetch/config.jsonc 2>/dev/null || neofetch 2>/dev/null || echo "System info tools not available"
echo ""

# Live stats
echo -e "${CYAN}━━━ Live Metrics ━━━${NC}"
echo -e "${GREEN}📊 $(get_system_load)${NC}"
echo -e "${GREEN}💿 Disk: $(df -h / | awk 'NR==2 {print $5 " used (" $4 " free)"}')"
echo -e "${GREEN}🌡️  Temp: $(sudo powermetrics --samplers smc -i1 -n1 2>/dev/null | grep -i "CPU die temperature" | awk '{print $4" "$5}' || echo "N/A")${NC}"
echo ""

# AI Tools Status
echo -e "${CYAN}━━━ AI Tools Status ━━━${NC}"
echo -e "$(check_ai_status)"
echo ""

# Running Services
echo -e "${CYAN}━━━ Active Services ━━━${NC}"
echo -e "$(check_services)"
echo ""

# Network
echo -e "${CYAN}━━━ Network ━━━${NC}"
echo -e "${GREEN}🌐 Local IP: $(ipconfig getifaddr en0 2>/dev/null || echo "Not connected")${NC}"
echo -e "${GREEN}🌍 Public IP: $(curl -s https://api.ipify.org || echo "Offline")${NC}"
echo ""

# Git Status (if in a git repo)
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${CYAN}━━━ Git Status ━━━${NC}"
    echo -e "${GREEN}📁 Repo: $(basename $(git rev-parse --show-toplevel))${NC}"
    echo -e "${GREEN}🌿 Branch: $(git branch --show-current)${NC}"
    echo -e "${GREEN}📝 Changes: $(git status --short | wc -l | xargs) files${NC}"
    echo ""
fi

# Quick Actions
echo -e "${CYAN}━━━ Quick Actions ━━━${NC}"
echo -e "${YELLOW}⌘⌥D${NC} - Dashboard | ${YELLOW}⌘⌥M${NC} - Music | ${YELLOW}⌘⌥G${NC} - Copilot | ${YELLOW}⌘⌥S${NC} - AI Status"
echo ""

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}Type 'vibe-help' for all commands${NC}  ${CYAN}║${NC}  ${PURPLE}Happy Coding! 🚀${NC}      ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
EOF

chmod +x "$HOME/.config/vibe-coding/dashboard/vibe-dashboard.sh"

# ━━━ AI Load Monitor ━━━
cat > "$HOME/.config/vibe-coding/dashboard/ai-monitor.sh" << 'EOF'
#!/usr/bin/env bash
# 🤖 AI Load Monitor - Track API usage and costs

# Create logs directory
mkdir -p "$HOME/.config/vibe-coding/logs"

LOG_FILE="$HOME/.config/vibe-coding/logs/ai-usage.log"

# Log AI API call
log_ai_call() {
    local tool="$1"
    local tokens="${2:-0}"
    local cost="${3:-0}"
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $tool | Tokens: $tokens | Cost: \$$cost" >> "$LOG_FILE"
}

# Show AI usage stats
show_stats() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "📊 No AI usage data yet"
        return
    fi
    
    echo "🤖 AI Usage Statistics"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Today's calls
    today=$(date '+%Y-%m-%d')
    today_calls=$(grep "$today" "$LOG_FILE" | wc -l | xargs)
    echo "📅 Today's API calls: $today_calls"
    
    # This week's calls
    week_start=$(date -v-7d '+%Y-%m-%d')
    week_calls=$(awk -v start="$week_start" '$1 >= start' "$LOG_FILE" | wc -l | xargs)
    echo "📊 This week's calls: $week_calls"
    
    # Most used tool
    most_used=$(awk -F'|' '{print $2}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -1 | awk '{print $2}' | xargs)
    echo "🥇 Most used: ${most_used:-N/A}"
    
    echo ""
    echo "📜 Recent calls:"
    tail -5 "$LOG_FILE" | while read line; do
        echo "  $line"
    done
}

# Export functions
export -f log_ai_call
export -f show_stats

# Execute based on argument
case "${1:-stats}" in
    log)
        log_ai_call "$2" "$3" "$4"
        ;;
    stats)
        show_stats
        ;;
    reset)
        > "$LOG_FILE"
        echo "✅ AI usage log reset"
        ;;
    *)
        echo "Usage: ai-monitor [stats|log|reset]"
        ;;
esac
EOF

chmod +x "$HOME/.config/vibe-coding/dashboard/ai-monitor.sh"

# ━━━ Help System ━━━
cat > "$HOME/.config/vibe-coding/dashboard/vibe-help.sh" << 'EOF'
#!/usr/bin/env bash
# 📚 Vibe Coding Help System

echo ""
echo "🎨 Vibe Coding Environment - Command Reference"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Quick Start:"
echo "  vibe_start         - Initialize vibe coding session"
echo "  vibe-dash          - Show full dashboard"
echo "  vibe-help          - Show this help"
echo ""
echo "🤖 AI Tools:"
echo "  vibe-ai or <prompt>      - OpenRouter query"
echo "  vibe-ai kimi <prompt>    - Kimi K2 query"
echo "  ai-ask <prompt>          - Quick AI question"
echo "  ai-code <prompt>         - Code-focused AI"
echo "  ai-review                - Review git diff"
echo "  ai_status                - Show AI tools status"
echo "  ai-monitor               - Show AI usage stats"
echo ""
echo "🎵 Music:"
echo "  vibe-music [lofi|chillhop|synthwave]"
echo "  lofi                     - Quick start lofi"
echo "  sp play/pause/next       - Spotify controls"
echo ""
echo "📁 Workspace:"
echo "  ws                       - Go to main workspace"
echo "  cursor                   - Open Cursor"
echo "  logic                    - Open Logic Pro"
echo ""
echo "🔐 Security:"
echo "  bwload                   - Load API keys from Bitwarden"
echo "  bw unlock                - Unlock Bitwarden"
echo ""
echo "⌨️  Global Shortcuts (Hammerspoon):"
echo "  ⌘ ⌥ G    - GitHub Copilot Chat"
echo "  ⌘ ⌥ A    - AI Console (Terminal)"
echo "  ⌘ ⌥ C    - Cursor"
echo "  ⌘ ⌥ V    - VS Code Insiders"
echo "  ⌘ ⌥ W    - Windsurf"
echo "  ⌘ ⌥ L    - Logic Pro"
echo "  ⌘ ⌥ M    - Start Music"
echo "  ⌘ ⌥ D    - Dashboard"
echo "  ⌘ ⌥ S    - AI Status"
echo ""
echo "📊 System:"
echo "  btop                     - System monitor"
echo "  fastfetch                - System info"
echo "  ports                    - Show listening ports"
echo "  myip                     - Show public IP"
echo ""
echo "🔧 File Management:"
echo "  ls/ll/la                 - Enhanced directory listing (eza)"
echo "  cat                      - Enhanced cat (bat)"
echo "  lt                       - Tree view"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
EOF

chmod +x "$HOME/.config/vibe-coding/dashboard/vibe-help.sh"

# ━━━ Dashboard Aliases ━━━
cat > "$HOME/.config/vibe-coding/dashboard/aliases.sh" << 'EOF'
# 📊 Dashboard Aliases

alias vibe-dash='$HOME/.config/vibe-coding/dashboard/vibe-dashboard.sh'
alias ai-monitor='$HOME/.config/vibe-coding/dashboard/ai-monitor.sh'
alias vibe-help='$HOME/.config/vibe-coding/dashboard/vibe-help.sh'

# Quick system monitors
alias sysmon='btop'
alias netmon='sudo nettop -m tcp'
EOF

echo ""
echo "✅ Terminal dashboard configured!"
echo ""
echo "📊 Available Dashboard Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  vibe-dash       → Full vibe dashboard"
echo "  vibe-help       → Command reference"
echo "  ai-monitor      → AI usage statistics"
echo "  btop            → System resource monitor"
echo "  fastfetch       → System information"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Dashboard will auto-load on terminal startup"


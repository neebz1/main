#!/usr/bin/env bash
# ⌨️ Global Shortcuts Setup using Hammerspoon

set -e

echo "⌨️ Setting up global shortcuts with Hammerspoon..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Install Hammerspoon if not present
if [ ! -d "/Applications/Hammerspoon.app" ]; then
    echo "📦 Installing Hammerspoon..."
    brew install --cask hammerspoon
fi

# Create Hammerspoon config directory
mkdir -p "$HOME/.hammerspoon"

# Create init.lua with vibe shortcuts
cat > "$HOME/.hammerspoon/init.lua" << 'EOF'
-- 🎨 Vibe Coding Global Shortcuts
-- Hammerspoon Configuration

hs.hotkey.alertDuration = 0
hs.hints.showTitleThresh = 0

-- ━━━ Global Shortcuts ━━━

-- ⌘ ⌥ G - Launch GitHub Copilot Chat (in Cursor)
hs.hotkey.bind({"cmd", "alt"}, "G", function()
    local cursor = hs.application.find("Cursor")
    if cursor then
        cursor:activate()
        hs.eventtap.keyStroke({"cmd", "shift"}, "I")  -- Open Copilot
    else
        hs.alert.show("Cursor not running")
    end
end)

-- ⌘ ⌥ A - AI Console (Terminal with AI context)
hs.hotkey.bind({"cmd", "alt"}, "A", function()
    local terminal = hs.application.find("iTerm") or hs.application.find("Terminal")
    if terminal then
        terminal:activate()
    else
        hs.application.launchOrFocus("Terminal")
    end
end)

-- ⌘ ⌥ C - Cursor
hs.hotkey.bind({"cmd", "alt"}, "C", function()
    hs.application.launchOrFocus("Cursor")
end)

-- ⌘ ⌥ V - VS Code Insiders
hs.hotkey.bind({"cmd", "alt"}, "V", function()
    hs.application.launchOrFocus("Visual Studio Code - Insiders")
end)

-- ⌘ ⌥ W - Windsurf
hs.hotkey.bind({"cmd", "alt"}, "W", function()
    hs.application.launchOrFocus("Windsurf")
end)

-- ⌘ ⌥ L - Logic Pro
hs.hotkey.bind({"cmd", "alt"}, "L", function()
    hs.application.launchOrFocus("Logic Pro")
end)

-- ⌘ ⌥ B - Browser (for AI tools)
hs.hotkey.bind({"cmd", "alt"}, "B", function()
    hs.application.launchOrFocus("Google Chrome") or hs.application.launchOrFocus("Safari")
end)

-- ⌘ ⌥ D - Vibe Dashboard (btop)
hs.hotkey.bind({"cmd", "alt"}, "D", function()
    local terminal = hs.application.find("iTerm") or hs.application.find("Terminal")
    if terminal then
        terminal:activate()
        hs.timer.doAfter(0.3, function()
            hs.eventtap.keyStroke({}, "return")
            hs.timer.doAfter(0.1, function()
                hs.eventtap.keyStrokes("btop\n")
            end)
        end)
    else
        hs.application.launchOrFocus("Terminal")
        hs.timer.doAfter(1, function()
            hs.eventtap.keyStrokes("btop\n")
        end)
    end
end)

-- ⌘ ⌥ M - Vibe Music (start lo-fi)
hs.hotkey.bind({"cmd", "alt"}, "M", function()
    hs.execute("open 'https://www.youtube.com/watch?v=jfKfPfyJRdk'")
    hs.alert.show("🎵 Lo-fi vibes starting...")
end)

-- ⌘ ⌥ S - AI Status
hs.hotkey.bind({"cmd", "alt"}, "S", function()
    local terminal = hs.application.find("iTerm") or hs.application.find("Terminal")
    if terminal then
        terminal:activate()
        hs.timer.doAfter(0.3, function()
            hs.eventtap.keyStrokes("ai_status\n")
        end)
    else
        hs.alert.show("Terminal not running")
    end
end)

-- ━━━ Window Management ━━━

-- ⌘ ⌥ ← - Left Half
hs.hotkey.bind({"cmd", "alt"}, "Left", function()
    local win = hs.window.focusedWindow()
    local f = win:frame()
    local screen = win:screen()
    local max = screen:frame()
    
    f.x = max.x
    f.y = max.y
    f.w = max.w / 2
    f.h = max.h
    win:setFrame(f)
end)

-- ⌘ ⌥ → - Right Half
hs.hotkey.bind({"cmd", "alt"}, "Right", function()
    local win = hs.window.focusedWindow()
    local f = win:frame()
    local screen = win:screen()
    local max = screen:frame()
    
    f.x = max.x + (max.w / 2)
    f.y = max.y
    f.w = max.w / 2
    f.h = max.h
    win:setFrame(f)
end)

-- ⌘ ⌥ ↑ - Maximize
hs.hotkey.bind({"cmd", "alt"}, "Up", function()
    local win = hs.window.focusedWindow()
    win:maximize()
end)

-- ⌘ ⌥ ↓ - Center
hs.hotkey.bind({"cmd", "alt"}, "Down", function()
    local win = hs.window.focusedWindow()
    win:centerOnScreen()
end)

-- ━━━ Startup ━━━

hs.alert.show("🎨 Vibe Coding Shortcuts Loaded")

-- Auto-reload config on change
function reloadConfig(files)
    doReload = false
    for _,file in pairs(files) do
        if file:sub(-4) == ".lua" then
            doReload = true
        end
    end
    if doReload then
        hs.reload()
    end
end

myWatcher = hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon/", reloadConfig):start()

EOF

# Start Hammerspoon
echo ""
echo "🚀 Starting Hammerspoon..."
open -a Hammerspoon

# Wait for Hammerspoon to start
sleep 2

# Load config
if pgrep -x "Hammerspoon" > /dev/null; then
    osascript -e 'tell application "Hammerspoon" to reload config'
fi

echo ""
echo "✅ Global shortcuts configured!"
echo ""
echo "⌨️  Vibe Coding Shortcuts:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⌘ ⌥ G    → GitHub Copilot Chat"
echo "⌘ ⌥ A    → AI Console (Terminal)"
echo "⌘ ⌥ C    → Cursor"
echo "⌘ ⌥ V    → VS Code Insiders"
echo "⌘ ⌥ W    → Windsurf"
echo "⌘ ⌥ L    → Logic Pro"
echo "⌘ ⌥ B    → Browser"
echo "⌘ ⌥ D    → Vibe Dashboard"
echo "⌘ ⌥ M    → Vibe Music"
echo "⌘ ⌥ S    → AI Status"
echo ""
echo "Window Management:"
echo "⌘ ⌥ ←    → Left Half"
echo "⌘ ⌥ →    → Right Half"
echo "⌘ ⌥ ↑    → Maximize"
echo "⌘ ⌥ ↓    → Center"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Hammerspoon menu bar icon should appear"
echo "💡 Config auto-reloads when ~/.hammerspoon/init.lua changes"


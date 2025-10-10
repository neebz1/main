#!/usr/bin/env bash
# 🎵 Lo-fi Music Integration for Vibe Coding

set -e

echo "🎵 Setting up lo-fi music integration..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create music integration directory
mkdir -p "$HOME/.config/vibe-coding/music"

# Create music player script
cat > "$HOME/.config/vibe-coding/music/vibe-player.sh" << 'EOF'
#!/usr/bin/env bash
# 🎵 Vibe Music Player

# Lo-fi playlists
PLAYLISTS=(
    "https://www.youtube.com/watch?v=jfKfPfyJRdk|Lofi Girl - Study Beats"
    "https://open.spotify.com/playlist/0vvXsWCC9xrXsKd4FyS8kM|Spotify Lofi Study"
    "https://www.youtube.com/watch?v=5qap5aO4i9A|Chillhop - Lofi Hip Hop"
    "https://www.youtube.com/watch?v=4xDzrJKXOOY|Synthwave Radio"
)

case "${1:-lofi}" in
    lofi|1)
        echo "🎵 Starting Lofi Girl..."
        open "https://www.youtube.com/watch?v=jfKfPfyJRdk"
        ;;
    spotify|2)
        echo "🎵 Opening Spotify Lofi playlist..."
        open "https://open.spotify.com/playlist/0vvXsWCC9xrXsKd4FyS8kM"
        ;;
    chillhop|3)
        echo "🎵 Starting Chillhop..."
        open "https://www.youtube.com/watch?v=5qap5aO4i9A"
        ;;
    synthwave|4)
        echo "🎵 Starting Synthwave..."
        open "https://www.youtube.com/watch?v=4xDzrJKXOOY"
        ;;
    list)
        echo "Available playlists:"
        echo "1. lofi      - Lofi Girl Study Beats"
        echo "2. spotify   - Spotify Lofi Study"
        echo "3. chillhop  - Chillhop Lofi Hip Hop"
        echo "4. synthwave - Synthwave Radio"
        ;;
    *)
        echo "Usage: vibe-music [lofi|spotify|chillhop|synthwave|list]"
        ;;
esac
EOF

chmod +x "$HOME/.config/vibe-coding/music/vibe-player.sh"

# Create workspace trigger script (launches music when opening workspace)
cat > "$HOME/.config/vibe-coding/music/workspace-trigger.sh" << 'EOF'
#!/usr/bin/env bash
# 🎵 Auto-play music when workspace opens

WORKSPACE_DIRS=(
    "$HOME/main"
    "$HOME/projects"
    "$HOME/code"
)

CURRENT_DIR=$(pwd)

# Check if we're in a workspace directory
for dir in "${WORKSPACE_DIRS[@]}"; do
    if [[ "$CURRENT_DIR" == "$dir"* ]]; then
        # Check if music is already playing (crude check)
        if ! pgrep -f "Music|Spotify|Chrome.*youtube" > /dev/null; then
            echo "🎵 Workspace detected! Starting lo-fi vibes..."
            sleep 1
            "$HOME/.config/vibe-coding/music/vibe-player.sh" lofi > /dev/null 2>&1 &
        fi
        break
    fi
done
EOF

chmod +x "$HOME/.config/vibe-coding/music/workspace-trigger.sh"

# Create AppleScript for Music.app control (if using Apple Music)
cat > "$HOME/.config/vibe-coding/music/music-control.applescript" << 'EOF'
-- Control Music.app for vibe coding

on run argv
    set command to item 1 of argv
    
    tell application "Music"
        if command is "play" then
            play
        else if command is "pause" then
            pause
        else if command is "next" then
            next track
        else if command is "previous" then
            previous track
        else if command is "status" then
            if player state is playing then
                return "Playing: " & name of current track & " by " & artist of current track
            else
                return "Paused"
            end if
        end if
    end tell
end run
EOF

# Create Spotify control script
cat > "$HOME/.config/vibe-coding/music/spotify-control.sh" << 'EOF'
#!/usr/bin/env bash
# Control Spotify via osascript

case "$1" in
    play)
        osascript -e 'tell application "Spotify" to play'
        ;;
    pause)
        osascript -e 'tell application "Spotify" to pause'
        ;;
    next)
        osascript -e 'tell application "Spotify" to next track'
        ;;
    prev|previous)
        osascript -e 'tell application "Spotify" to previous track'
        ;;
    status)
        state=$(osascript -e 'tell application "Spotify" to player state as string')
        if [ "$state" = "playing" ]; then
            track=$(osascript -e 'tell application "Spotify" to name of current track')
            artist=$(osascript -e 'tell application "Spotify" to artist of current track')
            echo "🎵 $track - $artist"
        else
            echo "⏸️  Paused"
        fi
        ;;
    *)
        echo "Usage: spotify-control [play|pause|next|prev|status]"
        ;;
esac
EOF

chmod +x "$HOME/.config/vibe-coding/music/spotify-control.sh"

# Add music aliases to a separate file that can be sourced
cat > "$HOME/.config/vibe-coding/music/aliases.sh" << 'EOF'
# 🎵 Vibe Music Aliases

# Main music command
alias vibe-music='$HOME/.config/vibe-coding/music/vibe-player.sh'

# Quick shortcuts
alias lofi='vibe-music lofi'
alias chillhop='vibe-music chillhop'
alias synthwave='vibe-music synthwave'

# Spotify controls
alias sp='$HOME/.config/vibe-coding/music/spotify-control.sh'
alias spotify-play='sp play'
alias spotify-pause='sp pause'
alias spotify-next='sp next'
alias spotify-prev='sp prev'
alias spotify-status='sp status'

# Music.app controls
alias music-play='osascript -e "tell application \"Music\" to play"'
alias music-pause='osascript -e "tell application \"Music\" to pause"'
alias music-next='osascript -e "tell application \"Music\" to next track"'
alias music-prev='osascript -e "tell application \"Music\" to previous track"'
EOF

echo ""
echo "✅ Music integration setup complete!"
echo ""
echo "🎵 Available Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Main Commands:"
echo "  vibe-music [lofi|spotify|chillhop|synthwave]"
echo "  lofi          → Quick start Lofi Girl"
echo "  chillhop      → Quick start Chillhop"
echo "  synthwave     → Quick start Synthwave"
echo ""
echo "Spotify Controls:"
echo "  sp play       → Play Spotify"
echo "  sp pause      → Pause Spotify"
echo "  sp next       → Next track"
echo "  sp prev       → Previous track"
echo "  sp status     → Show current track"
echo ""
echo "Music.app Controls:"
echo "  music-play    → Play Music.app"
echo "  music-pause   → Pause Music.app"
echo "  music-next    → Next track"
echo "  music-prev    → Previous track"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Music aliases will be available after sourcing .zshrc"
echo "💡 Use ⌘ ⌥ M to start lo-fi from anywhere (Hammerspoon)"


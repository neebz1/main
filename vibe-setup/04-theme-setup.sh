#!/usr/bin/env bash
# 🎨 Tokyo Night Theme & Visual Aesthetic Setup

set -e

echo "🎨 Applying Tokyo Night theme and visual aesthetics..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Install theme for terminal
echo "🖼️  Installing terminal themes..."

# Install Oh My Zsh if not present (optional but recommended)
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "📦 Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Install Powerlevel10k theme (alternative to Starship)
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]; then
    echo "📦 Installing Powerlevel10k theme..."
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
fi

# Create Starship config with Tokyo Night theme
mkdir -p "$HOME/.config"

cat > "$HOME/.config/starship.toml" << 'EOF'
# 🎨 Vibe Coding Starship Config - Tokyo Night Theme

format = """
[╭─](bold purple)\
$username\
$hostname\
$directory\
$git_branch\
$git_status\
$nodejs\
$python\
$rust\
$golang\
$docker_context\
$line_break\
[╰─](bold purple)$character"""

[character]
success_symbol = "[➜](bold green)"
error_symbol = "[✗](bold red)"

[username]
style_user = "bold cyan"
style_root = "bold red"
format = "[$user]($style) "
show_always = true

[hostname]
ssh_only = false
format = "[@$hostname](bold blue) "
disabled = false

[directory]
style = "bold purple"
format = "[$path]($style)[$read_only]($read_only_style) "
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = " "
style = "bold yellow"
format = "[$symbol$branch]($style) "

[git_status]
style = "bold red"
format = "([$all_status$ahead_behind]($style) )"

[nodejs]
symbol = " "
style = "bold green"
format = "[$symbol($version )]($style)"

[python]
symbol = " "
style = "bold yellow"
format = "[$symbol($version )]($style)"

[rust]
symbol = " "
style = "bold orange"
format = "[$symbol($version )]($style)"

[golang]
symbol = " "
style = "bold cyan"
format = "[$symbol($version )]($style)"

[docker_context]
symbol = " "
style = "bold blue"
format = "[$symbol$context]($style) "

[time]
disabled = false
format = "[$time]($style) "
style = "bold white"
time_format = "%T"

[cmd_duration]
min_time = 500
format = "took [$duration](bold yellow) "
EOF

# Create iTerm2 Tokyo Night color scheme
mkdir -p "$HOME/.config/vibe-coding/themes"

cat > "$HOME/.config/vibe-coding/themes/tokyo-night.itermcolors" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Ansi 0 Color</key>
    <dict>
        <key>Color Space</key>
        <string>sRGB</string>
        <key>Red Component</key>
        <real>0.101960784313725</real>
        <key>Green Component</key>
        <real>0.105882352941176</real>
        <key>Blue Component</key>
        <real>0.149019607843137</real>
    </dict>
    <key>Background Color</key>
    <dict>
        <key>Color Space</key>
        <string>sRGB</string>
        <key>Red Component</key>
        <real>0.101960784313725</real>
        <key>Green Component</key>
        <real>0.105882352941176</real>
        <key>Blue Component</key>
        <real>0.149019607843137</real>
    </dict>
    <key>Foreground Color</key>
    <dict>
        <key>Color Space</key>
        <string>sRGB</string>
        <key>Red Component</key>
        <real>0.752941176470588</real>
        <key>Green Component</key>
        <real>0.792156862745098</real>
        <key>Blue Component</key>
        <real>0.960784313725490</real>
    </dict>
</dict>
</plist>
EOF

# Create Terminal.app Tokyo Night profile
cat > "$HOME/.config/vibe-coding/themes/TokyoNight.terminal" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>name</key>
    <string>Tokyo Night</string>
    <key>type</key>
    <string>Window Settings</string>
    <key>BackgroundColor</key>
    <data>
    YnBsaXN0MDDUAQIDBAUGFRZYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS
    AAGGoKMHCA9VJG51bGzTCQoLDA0OVU5TUkdCXE5TQ29sb3JTcGFjZVYkY2xhc3NPECcw
    LjEwMTk2MDc4NDMgMC4xMDU4ODIzNTI5IDAuMTQ5MDE5NjA3OAAQAYAC0hAREhNaJGNs
    YXNzbmFtZVgkY2xhc3Nlc1dOU0NvbG9yohIUWE5TT2JqZWN0XxAPTlNLZXllZEFyY2hp
    dmVy0RcYVHJvb3SAAQgRGiMtMjc7QUhOW2KMjpCVoKmxtL3P0tcAAAAAAAABAQAAAAAA
    AAAZAAAAAAAAAAAAAAAAAAAA2Q==
    </data>
    <key>Font</key>
    <data>
    YnBsaXN0MDDUAQIDBAUGGBlYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS
    AAGGoKQHCBESVSRudWxs1AkKCwwNDg8QVk5TU2l6ZVhOU2ZGbGFnc1ZOU05hbWVWJGNs
    YXNzI0AqAAAAAAAAEBCAAoADXxAYSmV0QnJhaW5zTW9ub05lcmRGb250LTJSZWd1bGFy
    0hMUFRZaJGNsYXNzbmFtZVgkY2xhc3Nlc1ZOU0ZvbnSiFRdYTlNPYmplY3RfEA9OU0tl
    eWVkQXJjaGl2ZXLRGhtUcm9vdIABCBEaIy0yNzxCS1JbYmlydHZ4h4yXoKeqs8XIzQAA
    AAAAAAEBAAAAAAAAHAAAAAAAAAAAAAAAAAAAA88=
    </data>
    <key>FontAntialias</key>
    <true/>
    <key>ProfileCurrentVersion</key>
    <real>2.07</real>
</dict>
</plist>
EOF

echo ""
echo "📦 Installing IDE themes and extensions..."

# List of extensions to install
EXTENSIONS=(
    "enkia.tokyo-night"
    "vscode-icons-team.vscode-icons"
    "miguelsolorio.fluent-icons"
)

# Try to install for Cursor
if command -v cursor &> /dev/null; then
    echo "📦 Installing extensions for Cursor..."
    for ext in "${EXTENSIONS[@]}"; do
        cursor --install-extension "$ext" 2>/dev/null || true
    done
fi

# Try to install for VS Code Insiders
if command -v code-insiders &> /dev/null; then
    echo "📦 Installing extensions for VS Code Insiders..."
    for ext in "${EXTENSIONS[@]}"; do
        code-insiders --install-extension "$ext" 2>/dev/null || true
    done
fi

echo ""
echo "✅ Theme setup complete!"
echo ""
echo "📋 Manual Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "For Terminal.app:"
echo "1. Open Terminal > Preferences"
echo "2. Import: ~/.config/vibe-coding/themes/TokyoNight.terminal"
echo "3. Set as default"
echo ""
echo "For iTerm2:"
echo "1. Open iTerm2 > Preferences > Profiles > Colors"
echo "2. Import: ~/.config/vibe-coding/themes/tokyo-night.itermcolors"
echo ""
echo "For IDEs:"
echo "• Restart Cursor/VS Code Insiders"
echo "• Select 'Tokyo Night' theme from settings"
echo "• Select 'VSCode Icons' icon theme"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


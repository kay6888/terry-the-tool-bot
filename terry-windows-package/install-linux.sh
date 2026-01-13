#!/bin/bash
# Terry-the-Tool-Bot Linux Installer

echo "🚀 Installing Terry-the-Tool-Bot on Linux..."

# Create directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons

# Copy files
cp -r . ~/.local/share/terry-the-tool-bot/
chmod +x ~/.local/share/terry-the-tool-bot/terry
chmod +x ~/.local/share/terry-the-tool-bot/terry_gui.py

# Create symlink
ln -sf ~/.local/share/terry-the-tool-bot/terry ~/.local/bin/terry
ln -sf ~/.local/share/terry-the-tool-bot/terry_gui.py ~/.local/bin/terry-gui

# Create desktop entry
cat > ~/.local/share/applications/terry.desktop << 'EOF'
[Desktop Entry]
Version=2.0.0
Type=Application
Name=Terry-the-Tool-Bot
Comment=AI Coding Assistant
Exec=~/.local/bin/terry-gui
Icon=~/.local/share/icons/terry.png
Terminal=false
Categories=Development;
EOF

# Install dependencies
pip3 install -r ~/.local/share/terry-the-tool-bot/requirements.txt --user

echo "✅ Installation complete!"
echo "Run 'terry' for CLI or 'terry-gui' for GUI"
echo "Or find Terry in your applications menu"

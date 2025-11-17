#!/bin/bash
# WireGuard GUI Manager Installation Script

set -e

echo "🔐 WireGuard GUI Manager Installation"
echo "======================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please do not run this script as root"
    echo "   The script will ask for sudo password when needed"
    exit 1
fi

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Please install Python 3: sudo apt install python3 python3-tk"
    exit 1
fi

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Error: tkinter is not installed"
    echo "   Installing tkinter..."
    sudo apt install python3-tk -y
fi

# Check if WireGuard is installed
if ! command -v wg &> /dev/null; then
    echo "⚠️  Warning: WireGuard (wg) is not installed"
    echo "   Install it with: sudo apt install wireguard"
    read -p "   Do you want to install WireGuard now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install wireguard -y
    else
        echo "   Continuing without WireGuard..."
    fi
fi

# Create desktop entry directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make the Python script and launcher executable
chmod +x "${SCRIPT_DIR}/wireguard-gui.py"
chmod +x "${SCRIPT_DIR}/wireguard-gui-launcher.sh"

# Create desktop entry
cat > ~/.local/share/applications/wireguard-gui.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WireGuard Manager
Comment=GUI Manager for WireGuard VPN
Exec=${SCRIPT_DIR}/wireguard-gui-launcher.sh
Icon=${SCRIPT_DIR}/wireguard-gui.svg
Terminal=false
Categories=Network;System;
EOF

echo "✅ Desktop entry created at ~/.local/share/applications/wireguard-gui.desktop"

# Make start.sh executable
chmod +x "${SCRIPT_DIR}/start.sh"

# Create symlink in /usr/local/bin for command-line access
echo ""
echo "Creating command-line shortcut..."
sudo ln -sf "${SCRIPT_DIR}/start.sh" /usr/local/bin/wireguard-gui

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now run WireGuard GUI Manager by:"
echo "  1. Searching for 'WireGuard Manager' in your application menu"
echo "  2. Running 'wireguard-gui' from the terminal"
echo "  3. Running './start.sh' from this directory"
echo ""
echo "Note: The application requires sudo privileges to manage WireGuard connections"

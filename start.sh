#!/bin/bash
# WireGuard Manager Launcher

# Resolve symlinks and change to the script's actual directory
SCRIPT_PATH="$(readlink -f "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Run the WireGuard GUI
sudo python3 wireguard-gui.py

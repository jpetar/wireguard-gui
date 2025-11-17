#!/bin/bash
# WireGuard GUI Launcher Wrapper for pkexec
# This script preserves the DISPLAY environment variable for GUI applications

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

# Run with pkexec, passing display environment variables
exec pkexec env DISPLAY="$DISPLAY" XAUTHORITY="$XAUTHORITY" python3 "${SCRIPT_DIR}/wireguard-gui.py"

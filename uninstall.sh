#!/bin/bash
# WireGuard GUI Manager Uninstallation Script

set -e

echo "🔐 WireGuard GUI Manager Uninstallation"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please do not run this script as root"
    echo "   The script will ask for sudo password when needed"
    exit 1
fi

# Confirm uninstallation
read -p "Are you sure you want to uninstall WireGuard GUI Manager? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Removing WireGuard GUI Manager..."

# Remove desktop entry
if [ -f ~/.local/share/applications/wireguard-gui.desktop ]; then
    rm ~/.local/share/applications/wireguard-gui.desktop
    echo "✅ Removed desktop entry"
else
    echo "ℹ️  Desktop entry not found"
fi

# Remove command-line symlink
if [ -L /usr/local/bin/wireguard-gui ]; then
    sudo rm /usr/local/bin/wireguard-gui
    echo "✅ Removed command-line shortcut"
else
    echo "ℹ️  Command-line shortcut not found"
fi

# Ask about user data
echo ""
read -p "Do you want to remove user configuration files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    removed_files=0

    if [ -f ~/.wg_gui_last ]; then
        rm ~/.wg_gui_last
        ((removed_files++))
    fi

    if [ -f ~/.wg_gui_custom_configs ]; then
        rm ~/.wg_gui_custom_configs
        ((removed_files++))
    fi

    if [ $removed_files -gt 0 ]; then
        echo "✅ Removed $removed_files user configuration file(s)"
    else
        echo "ℹ️  No user configuration files found"
    fi
else
    echo "ℹ️  Keeping user configuration files"
fi

echo ""
echo "✅ Uninstallation complete!"
echo ""
echo "Note: The application files in this directory have not been deleted."
echo "      You can safely delete this directory manually if desired."

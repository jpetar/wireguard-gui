# 🔐 WireGuard GUI Manager

A modern, user-friendly graphical interface for managing WireGuard VPN connections on Linux. Features a sleek dark theme and intuitive controls for connecting, disconnecting, and managing WireGuard configurations.

![WireGuard GUI Manager](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)

## Features

- 🎨 **Modern Dark Theme** - Beautiful GitHub-inspired dark UI
- 🔌 **Easy Connection Management** - Connect/disconnect with a single click
- 📁 **Flexible Config Loading** - Use system configs or browse for custom config files
- 📊 **Real-time Status** - Live connection status indicator
- ✏️ **Built-in Config Editor** - Edit configurations directly in the GUI
- 💾 **Config Management** - Save, strip, and manage WireGuard configurations
- 🔄 **Auto-restore** - Remembers your last used interface
- 📟 **Command Output** - View detailed output from WireGuard commands

## Screenshots

The application features:
- Clean, organized interface with card-based layout
- Color-coded buttons for different actions
- Real-time connection status indicator
- Integrated configuration editor with syntax-friendly monospace font

## Requirements

- **Linux** (tested on Ubuntu/Debian-based distributions)
- **Python 3.6+** with tkinter
- **WireGuard** (`wg` and `wg-quick`)
- **pkexec** or **sudo** (required for managing VPN connections with elevated privileges)

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/jpetar/wireguard-gui.git
cd wireguard-gui

# Run the installation script
chmod +x install.sh
./install.sh
```

The installation script will:
1. Check for required dependencies (Python 3, tkinter, WireGuard)
2. Prompt to install missing dependencies
3. Make the Python script executable
4. Create a desktop entry for application menu access (uses `pkexec` for GUI password prompt)
5. Set up a command-line shortcut at `/usr/local/bin/wireguard-gui`

### Uninstallation

To uninstall WireGuard GUI Manager:

```bash
./uninstall.sh
```

This will:
- Remove the desktop entry
- Remove the command-line shortcut
- Optionally remove user configuration files

### Manual Installation

If you prefer to install manually:

```bash
# Install dependencies
sudo apt install python3 python3-tk wireguard

# Make scripts executable
chmod +x wireguard-gui.py start.sh

# Run the application (requires sudo for WireGuard commands)
./start.sh
```

## Usage

### Starting the Application

After installation, you can launch WireGuard GUI Manager in three ways:

1. **Application Menu**: Search for "WireGuard Manager" in your application launcher (uses `pkexec` for graphical password prompt)
2. **Command Line**: Run `wireguard-gui` from any terminal (requires sudo)
3. **Direct**: Navigate to the installation directory and run `./start.sh` (requires sudo)

### Managing Connections

1. **Select Interface**: Choose a WireGuard interface from the dropdown
   - Interfaces from `/etc/wireguard/` are loaded automatically
   - Use "Browse Config" to load custom configuration files

2. **Connect/Disconnect**:
   - Click "▲ Connect" to bring up the VPN connection
   - Click "▼ Disconnect" to tear down the connection
   - Status indicator shows connection state in real-time

3. **View Information**:
   - "📊 Show Status" - Display detailed WireGuard status
   - "📋 Quick Status" - Show quick interface status

4. **Edit Configurations**:
   - "✏️ Edit Config" - Open built-in editor for the selected configuration
   - "💾 Save Config" - Save the current running configuration
   - "🔧 Strip Config" - Strip and display configuration without private data

### Configuration Files

- System configs: `/etc/wireguard/*.conf`
- Custom configs: Use "Browse Config" to load from anywhere
- History: `~/.wg_gui_last` (stores last used interface)
- Custom config list: `~/.wg_gui_custom_configs` (persists custom config paths)

## Troubleshooting

### Permission Denied Errors

The application needs elevated privileges to manage WireGuard connections:
- **From Application Menu**: Uses `pkexec` which prompts graphically for your password
- **From Command Line**: Run with `sudo wireguard-gui` or `sudo ./start.sh`
- Ensure your user has sudo privileges or is in the sudoers file

### Application Menu Not Working

If the application doesn't launch from the application menu:
- Ensure `pkexec` is installed (usually part of `polkit`)
- Try running from terminal to see error messages: `pkexec /path/to/wireguard-gui.py`
- Alternative: Edit `~/.local/share/applications/wireguard-gui.desktop` and change `Exec=pkexec ...` to use a terminal with sudo

### "wg: command not found"

WireGuard is not installed. Install it with:
```bash
sudo apt install wireguard
```

### "tkinter not found"

Python tkinter module is missing:
```bash
sudo apt install python3-tk
```

### Configuration File Not Found

- System configs should be in `/etc/wireguard/`
- Use the "Browse Config" button to load configs from other locations
- Check file permissions if a config exists but won't load

## Development

The project structure:
```
wireguard-gui/
├── wireguard-gui.py    # Main application
├── start.sh            # Launcher script (resolves symlinks, runs with sudo)
├── install.sh          # Installation script
├── uninstall.sh        # Uninstallation script
├── setup.py            # Python package setup
├── requirements.txt    # Python dependencies (tkinter only)
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore patterns
```

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created for easy management of WireGuard VPN connections on Linux.

## Acknowledgments

- Built with Python's tkinter for cross-Linux compatibility
- Uses WireGuard's command-line tools (`wg` and `wg-quick`)
- Inspired by the need for a simple, modern WireGuard GUI on Linux

## Support

If you encounter issues or have suggestions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Include your Python version, Linux distribution, and error messages

---

## Technical Notes

- **Elevated Privileges**: The application requires root privileges to execute WireGuard commands (`wg-quick up/down`, `wg show`, etc.)
- **pkexec vs sudo**: The desktop launcher uses `pkexec` for graphical password prompts; command-line usage requires `sudo`
- **Symlink Resolution**: `start.sh` uses `readlink -f` to resolve symlinks, allowing it to work when called from `/usr/local/bin`
- **No External Dependencies**: Uses only Python standard library + tkinter (usually pre-installed)

**Security Note**: This application requires elevated privileges to manage network interfaces. Always review code that requires elevated privileges before running.

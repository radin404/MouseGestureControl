# Mouse Gesture Control

A Python application that enables mouse gesture control for Windows desktop navigation. Hold both mouse buttons and swipe to perform actions like switching between virtual desktops and opening task view.

## Features

- **Mouse Gesture Detection**: Hold both left and right mouse buttons and swipe in any direction
- **Desktop Navigation**: Switch between virtual desktops with simple gestures
- **Task View Control**: Open and close Windows task view
- **Configurable Settings**: Adjustable threshold, cooldown, and gesture mappings
- **GUI Interface**: Modern graphical interface for easy configuration
- **System Tray Support**: Runs in the background with system tray integration
- **Real-time Settings**: Change settings without restarting the application

## Gesture Actions

| Direction | Default Action | Description |
|-----------|----------------|-------------|
| Up        | Task View     | Opens Windows task view |
| Down      | Close Task View | Closes task view |
| Left      | Desktop Right | Switch to next virtual desktop |
| Right     | Desktop Left  | Switch to previous virtual desktop |

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/MouseGestureControl.git
   cd MouseGestureControl
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Application (Recommended)

Run the GUI application with system tray support:

```bash
python run_gui.py
```

Or on Windows:
```bash
run_gui.bat
```

**Features:**
- **Settings Window**: Configure all gesture mappings and settings
- **System Tray**: Right-click the tray icon for quick access
- **Background Operation**: Runs in the background while you work
- **Real-time Updates**: Settings changes apply immediately

### Command Line Interface

For advanced users, you can still use the original command-line interface:

```bash
python src/app.py
```

### Configuration

Use the built-in configuration tool:

```bash
python setup_config.py
```

## GUI Features

### Main Window
- **Status Display**: Shows whether gestures are enabled/disabled
- **Gesture Mappings**: Configure what each direction does
- **Settings Panel**: Adjust threshold, cooldown, and other options
- **Save/Reset**: Save changes or restore defaults

### System Tray
- **Right-click Menu**: Quick access to settings and controls
- **Enable/Disable**: Toggle gesture detection on/off
- **Show Settings**: Open the configuration window
- **Exit**: Close the application

### Settings

| Setting | Description | Range |
|---------|-------------|-------|
| **Threshold** | Minimum distance for gesture detection | 50-300 pixels |
| **Cooldown** | Time between gestures | 0.1-2.0 seconds |
| **Debug Mode** | Show gesture detection messages | On/Off |
| **Alt instead of Ctrl** | Use Alt key instead of Ctrl for desktop switching | On/Off |

## Configuration File

The application uses `config.json` for settings:

```json
{
    "up": "task_view",
    "down": "close_task_view",
    "left": "desktop_right",
    "right": "desktop_left",
    "debug": false,
    "threshold": 120.0,
    "cooldown": 0.5,
    "use_alt_instead_of_ctrl": true
}
```

## How It Works

1. **Gesture Detection**: The application monitors mouse input globally
2. **Button Combination**: Detects when both left and right mouse buttons are pressed
3. **Direction Analysis**: Calculates swipe direction based on mouse movement
4. **Action Execution**: Performs the configured action using keyboard shortcuts
5. **Cooldown Management**: Prevents accidental repeated gestures

## Requirements

- Windows 10/11
- Python 3.7+
- Virtual desktops enabled (for desktop switching)

## Dependencies

- `pynput`: Global mouse and keyboard input
- `keyboard`: Additional keyboard control
- `pystray`: System tray integration
- `Pillow`: Image processing for tray icon
- `tkinter`: GUI framework (included with Python)

## Troubleshooting

### Gestures Not Working
1. Check if gestures are enabled in the GUI
2. Verify the threshold setting (try increasing it)
3. Make sure you're holding both mouse buttons
4. Check if debug mode shows gesture detection

### Permission Issues
- Run as administrator if needed
- Some antivirus software may block global input monitoring

### Desktop Switching Not Working
- Ensure virtual desktops are enabled in Windows
- Try the "Alt instead of Ctrl" setting
- Check Windows version compatibility

## Development

### Project Structure
```
MouseGestureControl/
├── src/
│   ├── main_gui.py         # Main GUI application (current)
│   ├── app_legacy.py       # Original CLI application (legacy)
│   ├── gui_app_legacy.py   # Legacy GUI components
│   ├── tray_app_legacy.py  # Legacy system tray functionality
│   ├── gesture_controller.py
│   ├── input_listener.py
│   └── actions.py
├── config.json             # Configuration file
├── run_gui.py             # GUI launcher (current)
├── run_gui.bat            # Windows batch launcher
├── setup_config.py        # Configuration tool
├── cleanup_startup.py     # Cleanup script for startup entries
└── requirements.txt       # Dependencies
```

### Adding New Actions

To add new gesture actions, modify the `actions.py` file:

```python
def perform_action(action, debug=False, direction=None, use_alt=False):
    # ... existing code ...
    
    elif action == "your_new_action":
        # Your action implementation here
        pass
```

Then update the GUI combo boxes in `main_gui.py` to include your new action.

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Changelog

### Version 2.1 - Cleanup Release
- Removed old startup entries
- Cleaned up legacy files
- Improved project organization
- Added cleanup script

### Version 2.0 - GUI Release
- Added modern GUI interface
- System tray integration
- Real-time settings configuration
- Background operation
- Improved user experience

### Version 1.0 - Initial Release
- Basic gesture detection
- Command-line interface
- Core functionality

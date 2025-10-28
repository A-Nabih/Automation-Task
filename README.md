# TJM Automation Bot

A Python automation tool that fetches blog posts from an API and automates data entry into Windows Notepad, saving each post as a separate text file.

## Table of Contents

- [Features](#features)
- [Two Implementation Options](#two-implementation-options)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Packaging as Standalone Executable](#packaging-as-standalone-executable)
- [Technical Architecture](#technical-architecture)
- [Limitations & Considerations](#limitations--considerations)
- [Troubleshooting](#troubleshooting)
- [Performance Metrics](#performance-metrics)
- [Security Considerations](#security-considerations)
- [License](#license)
- [Contributing](#contributing)
- [Support](#support)

## Features

- **🔌 API Integration**: Fetches blog posts from JSONPlaceholder API with retry logic
- **🤖 Windows Automation**: Dual-mode automation (GUI or direct file writes)
- **🛡️ Robust Error Handling**: Comprehensive error recovery and logging
- **📊 Professional Logging**: Detailed execution logs and statistics
- **📦 Standalone Executable**: Can be packaged as a standalone .exe file
- **🔒 Instance Locking**: Prevents multiple concurrent executions
- **✔️ File Integrity**: SHA256 verification ensures data integrity
- **💾 Disk Space Validation**: Checks available space before writing files
- **⌨️ Clipboard-based Input**: More reliable text entry via clipboard
- **🔄 Graceful Degradation**: Falls back to direct file writes if GUI fails
- **⚙️ Highly Configurable**: Extensive environment-based configuration
- **🛡️ Failsafe Protection**: Emergency stop mechanism (move mouse to top-left corner)

## Two Implementation Options
The bot supports two execution modes, chosen automatically at runtime:

1. **Robust Implementation (RobustNotepadBot)**
   - Preferred version for production use
   - Located in the `robust/` module directory
   - **Architecture Features:**
     - **Modular Design**: Separate modules for API, file management, GUI automation, clipboard operations
     - **Instance Locking**: Prevents multiple bot instances from running simultaneously
     - **File Integrity Verification**: SHA256 hash verification ensures data integrity after save
     - **Disk Space Validation**: Checks available space before writing files
     - **Graceful Degradation**: Falls back to direct file writes if GUI automation fails
     - **Enhanced Error Handling**: Comprehensive error recovery mechanisms
     - **Structured Logging**: Centralized logger factory with consistent formatting
     - **Filename Sanitization**: Handles special characters and invalid filenames safely
   - **Key Components:**
     - `api.py`: HTTP client with retry logic
     - `files.py`: File operations with conflict resolution
     - `gui.py`: Windows GUI automation using pywinauto
     - `clipboard.py`: Clipboard-based text input for reliability
     - `lock.py`: File-based locking mechanism
     - `logging_setup.py`: Configurable logging system

2. **Legacy Implementation (NotepadAutomationBot)**
   - Used as a fallback if the robust version is not available
   - Implements the same core workflow but with simpler error handling
   - Reliable enough for basic automation but less resilient under heavy load
   - Located in `bot.py` as the main class

The bot will automatically detect and use the robust implementation if the `robust/` module is available. Otherwise, it falls back to the legacy implementation without requiring extra configuration.


## Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **Dependencies**: See requirements.txt
- **Internet Connection**: Required for API calls
- **Notepad**: Windows Notepad application (included with Windows)

## Installation & Setup

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation: `python --version`

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv tjm-automation-env

# Activate virtual environment
# On Windows Command Prompt:
tjm-automation-env\\Scripts\\activate

# On Windows PowerShell:
tjm-automation-env\\Scripts\\Activate.ps1
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install --upgrade -r requirements.txt

# Or install directly
pip install pyautogui pygetwindow pywinauto requests pathlib2 colorlog pillow opencv-python pyinstaller
```

### Step 4: Configure (Optional)

The bot comes with default settings that work out of the box. You can customize behavior by editing `config.env`:

```bash
# Edit configuration file
notepad config.env
```

Key settings you might want to adjust:
- `NUM_POSTS`: Number of posts to process (default: 10)
- `FILE_CONFLICT_ACTION`: How to handle existing files (overwrite/skip/rename)
- `LOG_LEVEL`: Logging verbosity (DEBUG/INFO/WARNING/ERROR)

## Quick Start

Once installed, you can run the bot immediately:

```bash
# Run with default settings
python bot.py

# Or use the provided batch script on Windows
run.bat
```

The bot will:
1. ✅ Fetch posts from the API
2. ✅ Launch Notepad
3. ✅ Type and save each post as a text file
4. ✅ Display a summary of results

**Output**: Files will be saved to `Desktop/tjm-project/` directory.

## Usage

### Running the Script

```bash
# Run the automation bot
python bot.py
```

### What It Does

1. **Fetches Data**: Retrieves the first 10 blog posts from JSONPlaceholder API
2. **Launches Notepad**: Opens Windows Notepad application
3. **Types Content**: Automatically types each blog post with formatted title and body
4. **Saves Files**: Saves each post as `post 1.txt`, `post 2.txt`, etc. in `Desktop/tjm-project/`
5. **Provides Statistics**: Shows execution summary with success/failure rates

### Output Structure

```
Desktop/
└── tjm-project/
    ├── post 1.txt
    ├── post 2.txt
    ├── post 3.txt
    └── ... (up to post 10.txt)
```

## Packaging as Standalone Executable

### Using PyInstaller

```bash
# Build standalone executable
pyinstaller tjm_automation.spec

# Or use direct command
pyinstaller --onefile --console --name TJM_Automation_Bot bot.py
```

### Executable Features

- **Standalone**: No Python installation required on target machines
- **Portable**: Single .exe file that can run anywhere
- **Console Output**: Shows progress and statistics
- **Logging**: Creates `tjm_automation.log` file for detailed logs

## Technical Architecture

### Project Structure

```
TJM-Automation/
├── bot.py                    # Main entry point with legacy implementation
├── robust_automation.py      # Robust implementation re-export
├── robust/                   # Robust implementation modules
│   ├── __init__.py
│   ├── bot_impl.py          # Main RobustNotepadBot class
│   ├── api.py               # API client with retry logic
│   ├── files.py             # File operations and integrity checks
│   ├── gui.py               # Windows GUI automation
│   ├── clipboard.py         # Clipboard operations
│   ├── lock.py              # Instance locking mechanism
│   ├── logging_setup.py     # Logger factory
│   └── waiter.py            # Wait utilities
├── config.env               # Configuration file
├── requirements.txt         # Python dependencies
├── tjm_automation.spec      # PyInstaller spec file
└── README.md                # This file
```

### Core Components

**Legacy Implementation (bot.py):**
1. **NotepadAutomationBot Class**: Main automation controller
2. **API Integration**: HTTP requests to JSONPlaceholder
3. **Window Management**: pygetwindow for Notepad window control
4. **Input Simulation**: pyautogui for keyboard/mouse automation
5. **Error Handling**: Comprehensive try/catch blocks
6. **Logging System**: File and console logging

**Robust Implementation (robust/):**
1. **RobustNotepadBot Class**: Main automation orchestrator
2. **ApiClient**: HTTP requests with retry logic and timeout handling
3. **FileManager**: File operations with conflict resolution and integrity checks
4. **GuiController**: Windows UI automation using pywinauto
5. **ClipboardManager**: Clipboard operations for reliable text input
6. **InstanceLock**: File-based locking to prevent concurrent executions
7. **LoggerFactory**: Centralized, configurable logging system

### Key Methods

**Legacy Implementation:**
- `fetch_posts_from_api()`: Retrieves blog posts from API
- `launch_notepad()`: Opens and activates Notepad window
- `type_text_safely()`: Types formatted content into Notepad
- `save_file()`: Saves current content to specified file
- `run_automation()`: Orchestrates the complete automation process

**Robust Implementation:**
- `run()`: Main orchestration method with integrity verification
- `_process_via_gui()`: GUI-based processing with fallback
- `_verify_file_integrity()`: SHA256 hash verification
- Module-specific methods in each component class

### Robust Implementation Module Details

**`api.py` - API Client**
- HTTP requests with timeout handling
- Automatic retry logic for failed requests
- JSON response parsing and validation
- Error handling and logging

**`files.py` - File Manager**
- Output directory creation and validation
- File conflict resolution (overwrite/skip/rename)
- Filename sanitization for special characters
- SHA256 hash calculation for integrity checks
- Disk space validation before writes
- Direct file write fallback mechanism

**`gui.py` - GUI Controller**
- Windows Notepad launch and window management
- Pywinauto-based window automation
- Text replacement via clipboard for reliability
- Save dialog automation
- Unexpected dialog handling
- Window focus management

**`clipboard.py` - Clipboard Manager**
- Clipboard-based text input (more reliable than keyboard simulation)
- Error handling for clipboard operations
- Fallback mechanisms for clipboard failures

**`lock.py` - Instance Lock**
- File-based locking mechanism
- Prevents multiple concurrent bot executions
- Automatic lock cleanup on exit
- Lock timeout handling

**`logging_setup.py` - Logger Factory**
- Centralized logger creation
- Configurable log levels and formatting
- File and console output support
- Consistent logging across all modules

**`waiter.py` - Wait Utilities**
- Timeout-based waiting functions
- Polling mechanisms for async operations
- Configurable wait intervals

## Configuration

The bot can be configured using the `config.env` file. Create or modify `config.env` with the following options:

### API Configuration
```env
API_URL=https://jsonplaceholder.typicode.com/posts  # API endpoint URL
API_TIMEOUT=30                                       # Request timeout in seconds
NUM_POSTS=10                                         # Number of posts to fetch
```

### Automation Settings
```env
PYAUTOGUI_PAUSE=0.5                                  # Pause between automation actions
TYPING_INTERVAL=0.01                                 # Interval between keystrokes
WINDOW_WAIT_TIME=2                                   # Wait time for window operations
SAVE_DIALOG_WAIT=1                                   # Wait time for save dialogs
```

### File and Directory Settings
```env
OUTPUT_DIR_NAME=tjm-project                          # Output directory name on Desktop
FILE_PREFIX=post                                     # Prefix for generated files
FILE_EXTENSION=txt                                  # File extension for output files
```

### File Handling Options
```env
FILE_CONFLICT_ACTION=overwrite                       # Action when file exists
# Options: overwrite, skip, rename
# overwrite = Replace existing files
# skip = Skip existing files
# rename = Add number suffix (e.g., "post 1 (1).txt")
```

### Logging Configuration
```env
LOG_LEVEL=INFO                                       # Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE=tjm_automation.log                          # Log file path
ENABLE_CONSOLE_LOGGING=true                          # Enable console output
```

### Safety Settings
```env
ENABLE_FAILSAFE=true                                 # Enable failsafe (move mouse to corner to stop)
```

### Development Settings
```env
DEBUG_MODE=false                                     # Enable debug logging
DRY_RUN=false                                        # Simulate without actually processing files
```

## Limitations & Considerations

### UI Automation Limitations

1. **Screen Resolution**: May need adjustment for different resolutions
2. **Window Focus**: Requires Notepad to be the active window
3. **System Performance**: Slower systems may need timing adjustments
4. **Antivirus Software**: May flag automation tools as suspicious

### Robustness Considerations

1. **Timing**: Built-in delays accommodate system variations
2. **Error Recovery**: Continues processing even if individual posts fail
3. **Failsafe**: Move mouse to top-left corner to emergency stop
4. **Logging**: Comprehensive logs for troubleshooting

### Alternative Approaches

Instead of UI automation, you could:
- Write files directly to disk (faster, more reliable)
- Use Windows COM automation (more robust)
- Implement web-based automation (cross-platform)

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**: Install dependencies with `pip install -r requirements.txt`
2. **Notepad not opening**: Ensure Windows Notepad is installed
3. **Files not saving**: Check Desktop permissions and disk space
4. **Slow performance**: Adjust `pyautogui.PAUSE` value in code

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Performance Metrics

- **Processing Speed**: ~2-3 seconds per post
- **Memory Usage**: ~50-100MB during execution
- **File Size**: Standalone executable ~50-100MB
- **Success Rate**: >95% on standard Windows configurations

## Security Considerations

- **API Calls**: Uses HTTPS for secure data transmission
- **File Operations**: Creates files only in designated directory
- **No Data Storage**: Doesn't store sensitive information
- **Failsafe**: Built-in emergency stop mechanism

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the log files
- Create an issue in the repository

---

**TJM Automation Bot**  
*Reliable automation solution for Windows environments*

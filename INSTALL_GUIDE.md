# Installation Guide

AI Prompt Generator Pro can be installed in two ways: using the installer or running from source.

## Method 1: Windows Installer (Recommended)

### Requirements
- Windows 10 or Windows 11
- 100 MB free disk space
- No Python installation required

### Installation Steps

1. **Download the installer**
   - Get `PromptGeneratorPro_Setup_2.0.0.exe` from the release

2. **Run the installer**
   - Double-click the installer file
   - Follow the installation wizard prompts

3. **Installation options**
   - Choose installation directory (default: `C:\Program Files\AI Prompt Generator Pro`)
   - Select additional tasks:
     - Create desktop shortcut
     - Create Quick Launch shortcut
     - Associate .prompt files

4. **Complete installation**
   - Click "Install" to begin
   - Wait for installation to complete
   - Optionally launch the application

### Uninstallation

1. **Via Control Panel**
   - Open "Apps & features" in Windows Settings
   - Find "AI Prompt Generator Pro"
   - Click "Uninstall"

2. **Via Start Menu**
   - Go to Start Menu → AI Prompt Generator Pro
   - Click "Uninstall AI Prompt Generator Pro"

3. **Uninstallation options**
   - Choose whether to keep user data (prompts, settings)
   - Confirm uninstallation

## Method 2: Running from Source

### Requirements
- Python 3.8 or higher
- pip package manager
- 50 MB free disk space

### Installation Steps

1. **Clone or download the source**
   ```bash
   git clone https://github.com/ai-prompt-generator/pro.git
   cd bot1
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run_gui.py
   ```
   Or on Windows:
   ```bash
   start.bat
   ```

### Building Executable (Optional)

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create icon**
   ```bash
   python create_icon.py
   ```

3. **Build executable**
   ```bash
   build.bat
   ```

4. **Create installer (requires Inno Setup)**
   ```bash
   create_installer.bat
   ```

## Troubleshooting

### Common Installation Issues

#### Issue: "Python is not installed or not in PATH"
**Solution:**
1. Download Python from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart your computer

#### Issue: "Failed to install dependencies"
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Issue: "PyQt6 installation fails"
**Solution:**
```bash
pip install PyQt6 --no-cache-dir
```
If that fails, try installing via wheel:
1. Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt6
2. Download the appropriate .whl file
3. Install with: `pip install downloaded_file.whl`

#### Issue: "Application won't start"
**Solution:**
1. Check if all dependencies are installed
2. Run from command line to see error messages:
   ```bash
   python run_gui.py
   ```
3. Check Python version: `python --version`

#### Issue: "Missing DLL errors"
**Solution:**
1. Install Visual C++ Redistributable from Microsoft
2. Update Windows
3. Run as administrator

### Runtime Issues

#### Issue: "File processing fails"
**Solution:**
- Check file permissions
- Ensure file is not corrupted
- Try different file format

#### Issue: "UI looks incorrect"
**Solution:**
- Update graphics drivers
- Try different display scaling
- Check for Windows updates

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit)
- **Processor**: 1 GHz or faster
- **Memory**: 2 GB RAM
- **Storage**: 100 MB available space
- **Display**: 1280x720 resolution

### Recommended Requirements
- **OS**: Windows 10/11 (64-bit)
- **Processor**: 2 GHz dual-core or faster
- **Memory**: 4 GB RAM
- **Storage**: 500 MB available space (for prompts library)
- **Display**: 1920x1080 resolution

## Support

If you encounter issues not covered here:

1. Check the [FAQ](FAQ.md)
2. Search existing [Issues](https://github.com/ai-prompt-generator/pro/issues)
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - System information

## License

AI Prompt Generator Pro is released under the MIT License. See [LICENSE](LICENSE) for details.
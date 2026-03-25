@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    AI Prompt Generator Pro - Complete Build
echo ========================================
echo.
echo This script will:
echo  1. Create application icon
echo  2. Build executable
echo  3. Create Windows installer
echo  4. Generate release package
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

set PROJECT_DIR=%~dp0
set VERSION=2.0.0

:: Step 1: Check dependencies
echo.
echo [1/6] Checking dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

:: Step 2: Install requirements
echo [2/6] Installing requirements...
pip install -r requirements_deploy.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

:: Step 3: Create icon
echo [3/6] Creating application icon...
python create_icon.py
if errorlevel 1 (
    echo WARNING: Icon creation had issues
)

:: Step 4: Build executable
echo [4/6] Building executable...
call build.bat
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

:: Step 5: Create installer
echo [5/6] Creating installer...
call create_installer.bat
if errorlevel 1 (
    echo WARNING: Installer creation had issues
)

:: Step 6: Create release package
echo [6/6] Creating release package...
set RELEASE_DIR=%PROJECT_DIR%release\v%VERSION%
mkdir "%RELEASE_DIR%" 2>nul

:: Copy installer if it exists
if exist "%PROJECT_DIR%dist\installer\PromptGeneratorPro_Setup_%VERSION%.exe" (
    copy "%PROJECT_DIR%dist\installer\PromptGeneratorPro_Setup_%VERSION%.exe" "%RELEASE_DIR%\" >nul
)

:: Copy portable version
if exist "%PROJECT_DIR%dist\PromptGeneratorPro.exe" (
    mkdir "%RELEASE_DIR%\portable" 2>nul
    copy "%PROJECT_DIR%dist\PromptGeneratorPro.exe" "%RELEASE_DIR%\portable\" >nul
    xcopy "%PROJECT_DIR%data\templates" "%RELEASE_DIR%\portable\data\templates\" /E /I /Y >nul 2>nul
    copy "%PROJECT_DIR%README.md" "%RELEASE_DIR%\portable\" >nul
    copy "%PROJECT_DIR%LICENSE" "%RELEASE_DIR%\portable\" >nul
)

:: Copy documentation
mkdir "%RELEASE_DIR%\docs" 2>nul
copy "%PROJECT_DIR%INSTALL_GUIDE.md" "%RELEASE_DIR%\docs\" >nul
copy "%PROJECT_DIR%QUICK_START.md" "%RELEASE_DIR%\docs\" >nul
copy "%PROJECT_DIR%FAQ.md" "%RELEASE_DIR%\docs\" >nul
copy "%PROJECT_DIR%CHANGELOG.md" "%RELEASE_DIR%\docs\" >nul

:: Create checksums
echo Creating checksums...
cd "%RELEASE_DIR%"
if exist "PromptGeneratorPro_Setup_%VERSION%.exe" (
    certutil -hashfile "PromptGeneratorPro_Setup_%VERSION%.exe" SHA256 > "checksums.txt"
    echo. >> "checksums.txt"
)
if exist "portable\PromptGeneratorPro.exe" (
    certutil -hashfile "portable\PromptGeneratorPro.exe" SHA256 >> "checksums.txt"
)

:: Create README for release
(
    echo # AI Prompt Generator Pro v%VERSION%
    echo.
    echo Release Date: %date%
    echo.
    echo ## Contents
    echo.
    echo - **PromptGeneratorPro_Setup_%VERSION%.exe** - Windows installer
    echo - **portable/** - Portable version (no installation required)
    echo - **docs/** - Documentation
    echo - **checksums.txt** - SHA256 checksums for verification
    echo.
    echo ## Installation
    echo.
    echo ### Using Installer
    echo 1. Run `PromptGeneratorPro_Setup_%VERSION%.exe`
    echo 2. Follow the installation wizard
    echo 3. Launch from Start Menu or Desktop shortcut
    echo.
    echo ### Using Portable Version
    echo 1. Extract `portable/` folder to any location
    echo 2. Run `PromptGeneratorPro.exe`
    echo 3. No installation required
    echo.
    echo ## Verification
    echo.
    echo To verify file integrity, compare checksums:
    echo.
    echo ```bash
    echo certutil -hashfile PromptGeneratorPro_Setup_%VERSION%.exe SHA256
    echo ```
    echo.
    echo ## Documentation
    echo.
    echo See `docs/` folder for:
    echo - INSTALL_GUIDE.md - Detailed installation instructions
    echo - QUICK_START.md - Getting started guide
    echo - FAQ.md - Frequently asked questions
    echo - CHANGELOG.md - Version history
    echo.
    echo ## Support
    echo.
    echo - GitHub: https://github.com/ai-prompt-generator/pro
    echo - Issues: Report bugs and request features
    echo - Discord: Join our community
    echo.
    echo ## License
    echo.
    echo MIT License - See LICENSE file for details.
) > "%RELEASE_DIR%\README.txt"

:: Create zip archive
echo Creating zip archive...
cd "%PROJECT_DIR%release"
powershell -command "Compress-Archive -Path 'v%VERSION%' -DestinationPath 'AI_Prompt_Generator_Pro_v%VERSION%.zip' -Force"

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo Release files created in: %RELEASE_DIR%
echo.
echo Contents:
dir "%RELEASE_DIR%" /B
echo.
echo Zip archive: %PROJECT_DIR%release\AI_Prompt_Generator_Pro_v%VERSION%.zip
echo.
echo Next steps:
echo 1. Test the installer on a clean Windows machine
echo 2. Verify all features work
echo 3. Upload to GitHub Releases
echo 4. Update documentation
echo.

pause
endlocal
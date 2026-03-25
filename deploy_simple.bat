@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    AI Prompt Generator Pro - Simple Deploy
echo ========================================
echo.
echo This creates a portable deployment package
echo without requiring PyInstaller or Inno Setup.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

set PROJECT_DIR=%~dp0
set VERSION=2.0.0
set DEPLOY_DIR=%PROJECT_DIR%deploy\v%VERSION%

:: Clean previous deployment
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"

echo [1/5] Creating directory structure...
mkdir "%DEPLOY_DIR%\app"
mkdir "%DEPLOY_DIR%\app\data"
mkdir "%DEPLOY_DIR%\app\data\templates"
mkdir "%DEPLOY_DIR%\app\data\prompts"
mkdir "%DEPLOY_DIR%\app\assets"
mkdir "%DEPLOY_DIR%\app\assets\icons"
mkdir "%DEPLOY_DIR%\docs"

echo [2/5] Copying application files...
copy "%PROJECT_DIR%prompt_generator.py" "%DEPLOY_DIR%\app\" >nul
copy "%PROJECT_DIR%prompt_core.py" "%DEPLOY_DIR%\app\" >nul
copy "%PROJECT_DIR%run_gui.py" "%DEPLOY_DIR%\app\" >nul
copy "%PROJECT_DIR%start.bat" "%DEPLOY_DIR%\app\" >nul
copy "%PROJECT_DIR%requirements.txt" "%DEPLOY_DIR%\app\" >nul

echo [3/5] Copying data files...
if exist "%PROJECT_DIR%data\templates\*" (
    xcopy "%PROJECT_DIR%data\templates\*" "%DEPLOY_DIR%\app\data\templates\" /E /I /Y >nul
)
if exist "%PROJECT_DIR%assets\icons\*" (
    xcopy "%PROJECT_DIR%assets\icons\*" "%DEPLOY_DIR%\app\assets\icons\" /E /I /Y >nul
)

echo [4/5] Copying documentation...
copy "%PROJECT_DIR%README.md" "%DEPLOY_DIR%\docs\" >nul
copy "%PROJECT_DIR%INSTALL_GUIDE.md" "%DEPLOY_DIR%\docs\" >nul
copy "%PROJECT_DIR%QUICK_START.md" "%DEPLOY_DIR%\docs\" >nul
copy "%PROJECT_DIR%FAQ.md" "%DEPLOY_DIR%\docs\" >nul
copy "%PROJECT_DIR%CHANGELOG.md" "%DEPLOY_DIR%\docs\" >nul
copy "%PROJECT_DIR%LICENSE" "%DEPLOY_DIR%\docs\" >nul

echo [5/5] Creating launcher scripts...
:: Create batch launcher
(
    echo @echo off
    echo echo ========================================
    echo echo    AI Prompt Generator Pro v%VERSION%
    echo echo ========================================
    echo echo.
    echo echo Checking Python installation...
    echo python --version ^>nul 2^>^&1
    echo if errorlevel 1 ^(
    echo     echo ERROR: Python is not installed or not in PATH
    echo     echo Please install Python 3.8+ from https://python.org
    echo     pause
    echo     exit /b 1
    echo ^)
    echo.
    echo echo Installing dependencies...
    echo pip install -r requirements.txt --quiet
    echo.
    echo echo Starting application...
    echo python run_gui.py
    echo pause
) > "%DEPLOY_DIR%\Start_Application.bat"

:: Create Python launcher
(
    echo """AI Prompt Generator Pro Launcher"""
    echo import sys
    echo import os
    echo import subprocess
    echo.
    echo def main^(^):
    echo     """Launch the application"""
    echo     print^("AI Prompt Generator Pro v%VERSION%"^)
    echo     print^("=" * 40^)
    echo     print^()
    echo.
    echo     # Check Python version
    echo     if sys.version_info ^< ^(3, 8^):
    echo         print^("ERROR: Python 3.8 or higher is required"^)
    print^("Current version:", sys.version^)
    echo         return
    echo.
    echo     # Install dependencies
    echo     print^("Installing dependencies..."^)
    echo     subprocess.run^([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"]^)
    echo.
    echo     # Launch application
    echo     print^("Starting application..."^)
    echo     try:
    echo         from prompt_generator import main
    echo         main^(^)
    echo     except Exception as e:
    echo         print^(f"Error starting application: {e}"^)
    echo.
    echo if __name__ == "__main__":
    echo     main^(^)
) > "%DEPLOY_DIR%\app\launch.py"

:: Create README for deployment
(
    echo # AI Prompt Generator Pro - Portable Deployment
    echo.
    echo Version: %VERSION%
    echo.
    echo ## Quick Start
    echo.
    echo 1. Make sure Python 3.8+ is installed
    echo 2. Double-click `Start_Application.bat`
    echo 3. The application will install dependencies and start
    echo.
    echo ## Manual Start
    echo.
    echo 1. Open command prompt in `app/` folder
    echo 2. Run: `pip install -r requirements.txt`
    echo 3. Run: `python run_gui.py`
    echo.
    echo ## Documentation
    echo.
    echo See `docs/` folder for detailed documentation.
    echo.
    echo ## System Requirements
    echo.
    echo - Windows 10/11 (64-bit)
    echo - Python 3.8 or higher
    echo - 100 MB free disk space
    echo.
    echo ## Support
    echo.
    echo Visit: https://github.com/ai-prompt-generator/pro
) > "%DEPLOY_DIR%\README.txt"

:: Create zip archive
echo Creating zip archive...
cd "%PROJECT_DIR%deploy"
powershell -command "Compress-Archive -Path 'v%VERSION%' -DestinationPath 'AI_Prompt_Generator_Pro_v%VERSION%_Portable.zip' -Force"

echo.
echo ========================================
echo    Deployment Complete!
echo ========================================
echo.
echo Portable deployment created at: %DEPLOY_DIR%
echo.
echo Zip archive: %PROJECT_DIR%deploy\AI_Prompt_Generator_Pro_v%VERSION%_Portable.zip
echo.
echo To distribute:
echo 1. Send the zip file to users
echo 2. They extract and run Start_Application.bat
echo 3. Python 3.8+ must be installed on their system
echo.
pause
endlocal
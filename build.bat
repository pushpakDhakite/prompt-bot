@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    AI Prompt Generator Pro - Build Script
echo ========================================
echo.

set PROJECT_DIR=%~dp0
set DIST_DIR=%PROJECT_DIR%dist
set BUILD_DIR=%PROJECT_DIR%build
set APP_NAME=PromptGeneratorPro
set VERSION=2.0.0

:: Clean previous builds
echo [1/6] Cleaning previous builds...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
mkdir "%DIST_DIR%"
mkdir "%BUILD_DIR%"

:: Check Python installation
echo [2/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

:: Check PyInstaller
echo [3/6] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

:: Check dependencies
echo [4/6] Checking dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

:: Build executable
echo [5/6] Building executable...
cd /d "%PROJECT_DIR%"
pyinstaller --clean --noconfirm PromptGeneratorPro.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

:: Verify build
echo [6/6] Verifying build...
if not exist "%DIST_DIR%\%APP_NAME%.exe" (
    echo ERROR: Executable not found at %DIST_DIR%\%APP_NAME%.exe
    pause
    exit /b 1
)

:: Copy additional files
echo Copying additional files...
copy "%PROJECT_DIR%README.md" "%DIST_DIR%\" >nul
copy "%PROJECT_DIR%LICENSE" "%DIST_DIR%\" >nul 2>nul
if not exist "%DIST_DIR%\data" mkdir "%DIST_DIR%\data"
if not exist "%DIST_DIR%\data\templates" mkdir "%DIST_DIR%\data\templates"
xcopy "%PROJECT_DIR%data\templates\*" "%DIST_DIR%\data\templates\" /E /I /Y >nul

echo.
echo ========================================
echo    Build completed successfully!
echo ========================================
echo.
echo Output: %DIST_DIR%\%APP_NAME%.exe
echo Version: %VERSION%
echo.
echo To create installer, run: create_installer.bat
echo.
pause
endlocal
@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    AI Prompt Generator Pro - Installer Creator
echo ========================================
echo.

set PROJECT_DIR=%~dp0
set DIST_DIR=%PROJECT_DIR%dist
set INSTALLER_DIR=%PROJECT_DIR%installer
set APP_NAME=PromptGeneratorPro
set VERSION=2.0.0
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

:: Check if executable exists
echo [1/5] Checking executable...
if not exist "%DIST_DIR%\%APP_NAME%.exe" (
    echo ERROR: Executable not found at %DIST_DIR%\%APP_NAME%.exe
    echo Please run build.bat first to create the executable.
    pause
    exit /b 1
)

:: Check Inno Setup installation
echo [2/5] Checking Inno Setup...
if not exist %INNO_SETUP% (
    echo Inno Setup not found at default location.
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isinfo.php
    echo Or update the INNO_SETUP path in this script.
    pause
    exit /b 1
)

:: Create necessary directories
echo [3/5] Creating directories...
if not exist "%INSTALLER_DIR%" mkdir "%INSTALLER_DIR%"
if not exist "%DIST_DIR%\installer" mkdir "%DIST_DIR%\installer"

:: Create placeholder assets if they don't exist
echo [4/5] Checking assets...
if not exist "%PROJECT_DIR%assets\icons\app_icon.ico" (
    echo Creating placeholder icon...
    :: Create a simple placeholder file - in production, use a real icon
    echo Placeholder > "%PROJECT_DIR%assets\icons\app_icon.ico"
)

if not exist "%PROJECT_DIR%assets\license.txt" (
    echo Creating license file...
    (
        echo MIT License
        echo.
        echo Copyright ^(c^) 2026 AI Prompt Generator Pro
        echo.
        echo Permission is hereby granted, free of charge, to any person obtaining a copy
        echo of this software and associated documentation files ^(the "Software"^), to deal
        echo in the Software without restriction, including without limitation the rights
        echo to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        echo copies of the Software, and to permit persons to whom the Software is
        echo furnished to do so, subject to the following conditions:
        echo.
        echo The above copyright notice and this permission notice shall be included in all
        echo copies or substantial portions of the Software.
        echo.
        echo THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        echo IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        echo FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        echo AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        echo LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        echo OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        echo SOFTWARE.
    ) > "%PROJECT_DIR%assets\license.txt"
)

:: Build installer using Inno Setup
echo [5/5] Building installer...
cd /d "%PROJECT_DIR%"
%INNO_SETUP% "installer\setup.iss"

if errorlevel 1 (
    echo ERROR: Installer creation failed
    pause
    exit /b 1
)

:: Verify installer was created
if exist "%DIST_DIR%\installer\%APP_NAME%_Setup_%VERSION%.exe" (
    echo.
    echo ========================================
    echo    Installer created successfully!
    echo ========================================
    echo.
    echo Installer: %DIST_DIR%\installer\%APP_NAME%_Setup_%VERSION%.exe
    echo.
    echo To test the installer:
    echo   1. Run the installer on a clean Windows machine
    echo   2. Verify all features work
    echo   3. Test uninstallation
    echo.
) else (
    echo ERROR: Installer file not found
    echo Check Inno Setup logs for details.
)

pause
endlocal
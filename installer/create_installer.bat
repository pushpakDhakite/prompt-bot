@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    AI Prompt Generator Pro - Installer Creator
echo ========================================
echo.

set PROJECT_DIR=%~dp0
set PROJECT_DIR=%PROJECT_DIR:~0,-1%
set DIST_DIR=%PROJECT_DIR%\..\dist
set INSTALLER_DIR=%PROJECT_DIR%\..
set APP_NAME=PromptGeneratorPro
set VERSION=2.0.0
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

:: Check if executable exists
echo [1/4] Checking executable...
if not exist "%DIST_DIR%\%APP_NAME%.exe" (
    echo ERROR: Executable not found at %DIST_DIR%\%APP_NAME%.exe
    echo Please build the executable first using: python -m PyInstaller PromptGeneratorPro.spec
    pause
    exit /b 1
)

:: Check Inno Setup installation
echo [2/4] Checking Inno Setup...
if not exist %INNO_SETUP% (
    echo Inno Setup not found at default location.
    echo.
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isinfo.php
    echo.
    echo After installation, you can create the installer by running:
    echo   %INNO_SETUP% "%PROJECT_DIR%\setup.iss"
    echo.
    echo For now, creating portable version instead...
    goto :create_portable
)

:: Create installer directory
echo [3/4] Creating directories...
if not exist "%INSTALLER_DIR%\installer" mkdir "%INSTALLER_DIR%\installer"

:: Build installer using Inno Setup
echo [4/4] Building installer...
cd /d "%PROJECT_DIR%"
%INNO_SETUP% "setup.iss"

if errorlevel 1 (
    echo ERROR: Installer creation failed
    pause
    exit /b 1
)

:: Verify installer was created
if exist "%INSTALLER_DIR%\installer\%APP_NAME%_Setup_%VERSION%.exe" (
    echo.
    echo ========================================
    echo    Installer created successfully!
    echo ========================================
    echo.
    echo Installer: %INSTALLER_DIR%\installer\%APP_NAME%_Setup_%VERSION%.exe
    echo.
) else (
    echo ERROR: Installer file not found
    echo Check Inno Setup logs for details.
)
goto :end

:create_portable
echo.
echo Creating portable version...
cd /d "%PROJECT_DIR%\.."
if not exist "release\portable" mkdir "release\portable"
copy "%DIST_DIR%\%APP_NAME%.exe" "release\portable\" >nul
xcopy "templates" "release\portable\templates\" /E /I /Y >nul
copy "README.md" "release\portable\" >nul
copy "LICENSE" "release\portable\" >nul
copy "QUICK_START.md" "release\portable\" >nul

:: Create launcher
(
    echo @echo off
    echo echo ========================================
    echo echo    AI Prompt Generator Pro
    echo echo ========================================
    echo echo.
    echo echo Starting application...
    echo echo.
    echo start "" "PromptGeneratorPro.exe"
    echo exit
) > "release\portable\Start_Application.bat"

:: Create README
(
    echo AI Prompt Generator Pro - Portable Version
    echo ===========================================
    echo.
    echo Version: %VERSION%
    echo.
    echo Quick Start:
    echo 1. Double-click "Start_Application.bat" or "PromptGeneratorPro.exe"
    echo 2. The application will start immediately
    echo.
    echo No installation required!
    echo - No Python installation needed
    echo - No dependencies to install
    echo - Works from any location
    echo.
    echo See QUICK_START.md for detailed usage instructions.
) > "release\portable\README.txt"

:: Create zip
powershell -command "Compress-Archive -Path 'release\portable' -DestinationPath 'release\AI_Prompt_Generator_Pro_v%VERSION%_Portable.zip' -Force"

echo.
echo ========================================
echo    Portable version created successfully!
echo ========================================
echo.
echo Portable: release\AI_Prompt_Generator_Pro_v%VERSION%_Portable.zip
echo.

:end
pause
endlocal
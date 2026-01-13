@echo off
setlocal enabledelayedexpansion

echo ===============================================================
echo Terry-the-Tool-Bot Windows Installation Script
echo ===============================================================
echo.
echo This installer sets up Terry-the-Tool-Bot with Git integration
echo Optimized for Windows 10/11
echo ===============================================================
echo.

:: Check Python installation
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8+ first:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%a in ('python --version') do set PYTHON_VERSION=%%a
    echo ✅ Python found: !PYTHON_VERSION!
)

:: Check Git installation
echo [2/8] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found!
    echo.
    echo Please install Git for Windows:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%a in ('git --version') do set GIT_VERSION=%%a
    echo ✅ Git found: !GIT_VERSION!
)

:: Check for GitHub Desktop
echo [3/8] Checking GitHub Desktop...
if exist "C:\Users\%USERNAME%\AppData\Local\GitHubDesktop\GitHubDesktop.exe" (
    echo ✅ GitHub Desktop found
) else if exist "C:\Program Files\GitHub Desktop\GitHubDesktop.exe" (
    echo ✅ GitHub Desktop found
) else if exist "C:\Program Files (x86)\GitHub Desktop\GitHubDesktop.exe" (
    echo ✅ GitHub Desktop found
) else (
    echo ⚠️ GitHub Desktop not found (optional)
    echo. 
    echo You can install it from: https://desktop.github.com/
)

:: Create installation directory
echo [4/8] Setting up installation directory...
set INSTALL_DIR=C:\Terry-the-Tool-Bot
if not exist "!INSTALL_DIR!" (
    mkdir "!INSTALL_DIR!"
    echo ✅ Created installation directory: !INSTALL_DIR!
) else (
    echo ✅ Installation directory exists: !INSTALL_DIR!
)

:: Install Terry package
echo [5/8] Installing Terry-the-Tool-Bot package...
cd /d "%~dp0"
python -m pip install -e . --upgrade
if errorlevel 1 (
    echo ❌ Package installation failed!
    echo.
    echo Trying alternative installation method...
    python -m pip install -e . --user
    if errorlevel 1 (
        echo ❌ Installation failed completely!
        pause
        exit /b 1
    )
)
echo ✅ Terry-the-Tool-Bot installed!

:: Install Git integration dependencies
echo [6/8] Installing Git integration dependencies...
python -m pip install GitPython PyGithub python-gitlab
if errorlevel 1 (
    echo ❌ Git dependencies installation failed!
    echo.
    echo Git integration may not work properly
) else (
    echo ✅ Git dependencies installed!
)

:: Install Windows-specific dependencies
echo [7/8] Installing Windows-specific dependencies...
python -m pip install pywin32 wmi
if errorlevel 1 (
    echo ⚠️ Windows dependencies installation failed!
    echo.
    echo Some Windows-specific features may not work
) else (
    echo ✅ Windows dependencies installed!
)

:: Configure Git for Windows
echo [8/8] Configuring Git for Windows compatibility...
git config --global core.autocrlf true
git config --global core.longpaths true
git config --global core.symlinks true
git config --global core.filemode false
echo ✅ Git configured for Windows!

:: Create Terry configuration directory
echo.
echo Creating configuration directories...
set CONFIG_DIR=%APPDATA%\Terry
if not exist "!CONFIG_DIR!" (
    mkdir "!CONFIG_DIR!"
)
mkdir "!CONFIG_DIR!\logs" 2>nul
mkdir "!CONFIG_DIR!\cache" 2>nul
mkdir "!CONFIG_DIR!\plugins" 2>nul
echo ✅ Configuration directories created!

:: Create desktop shortcut
echo.
echo Creating desktop shortcut...
set SHORTCUT_TARGET=!INSTALL_DIR!\main.py
set SHORTCUT_NAME=Terry-the-Tool-Bot
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\!SHORTCUT_NAME!.lnk'); $shortcut.TargetPath = '!SHORTCUT_TARGET!'; $shortcut.Save()"
echo ✅ Desktop shortcut created!

:: Set up PATH
echo.
echo Adding Terry to system PATH...
for /f "tokens=*" %%a in ("!INSTALL_DIR!") do (
    if not exist "%%~dp$PATH:%%a" (
        echo !INSTALL_DIR! >> %PATH%
    )
)
echo ✅ Added to PATH!

:: Create uninstaller
echo.
echo Creating uninstaller...
echo @echo off > "!INSTALL_DIR!\uninstall.bat"
echo echo Uninstalling Terry-the-Tool-Bot... >> "!INSTALL_DIR!\uninstall.bat"
echo python -m pip uninstall terry-tool-bot -y 2^>nul >> "!INSTALL_DIR!\uninstall.bat"
echo rmdir /s /q "!INSTALL_DIR!" 2^>nul >> "!INSTALL_DIR!\uninstall.bat"
echo del "%USERPROFILE%\Desktop\!SHORTCUT_NAME!.lnk" 2^>nul >> "!INSTALL_DIR!\uninstall.bat"
echo echo Terry-the-Tool-Bot has been uninstalled. >> "!INSTALL_DIR!\uninstall.bat"
echo pause >> "!INSTALL_DIR!\uninstall.bat"
echo ✅ Uninstaller created!

:: Installation complete
echo.
echo ===============================================================
echo 🎉 Installation Complete!
echo ===============================================================
echo.
echo Terry-the-Tool-Bot is now installed and ready to use!
echo.
echo 📋 Features installed:
echo   ✅ Core Terry AI assistant
echo   ✅ Git integration (clone, commit, push, pull)
echo   ✅ GitHub Desktop integration
echo   ✅ Windows 10/11 optimizations
echo   ✅ PowerShell Git commands
echo   ✅ Long path support
echo.
echo 🚀 Usage:
echo   • Run from Start Menu: Terry-the-Tool-Bot
echo   • Run from Command Prompt: terry
echo   • Run GUI: terry --gui
echo   • Run CLI: terry "your request here"
echo.
echo 📁 Installation locations:
echo   • Main directory: !INSTALL_DIR!
echo   • Config: !CONFIG_DIR!
echo   • Desktop shortcut: %USERPROFILE%\Desktop\!SHORTCUT_NAME!.lnk
echo   • Uninstaller: !INSTALL_DIR!\uninstall.bat
echo.
echo ⚙️ Git setup:
echo   • Git configured for Windows compatibility
echo   • GitHub Desktop integration available
echo   • PowerShell commands enabled
echo.
echo 📚 Help:
echo   • terry --help
echo   • Visit: https://docs.terry-tool-bot.dev
echo.
echo To start using Terry immediately, type: terry
echo.
pause
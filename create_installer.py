#!/usr/bin/env python3
"""
Terry-the-Tool-Bot Cross-Platform Installer
Creates installation packages for Linux and Windows
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import zipfile
import json

class TerryInstaller:
    """Cross-platform installer for Terry-the-Tool-Bot"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.install_name = "terry-the-tool-bot"
        self.version = "2.0.0"
        
    def create_requirements_file(self):
        """Create requirements.txt for installation"""
        requirements = """# Terry-the-Tool-Bot Core Dependencies
requests>=2.28.0
psutil>=5.9.0
click>=8.0.0
pyyaml>=6.0

# Optional GUI Dependencies
webbrowser>=0.0.1
http.server>=0.0.1

# Development Dependencies
pytest>=7.0
black>=22.0
flake8>=5.0
"""
        
        req_file = self.project_root / "install_requirements.txt"
        with open(req_file, 'w') as f:
            f.write(requirements)
        return req_file
    
    def create_launcher_script(self, platform_type):
        """Create launcher script for the specified platform"""
        
        if platform_type == "windows":
            launcher = f'''@echo off
echo 🚀 Starting Terry-the-Tool-Bot...
cd /d "%~dp0"
python terry_minimal.py %*
pause
'''
            return launcher, "terry.bat"
            
        elif platform_type == "linux":
            launcher = f'''#!/bin/bash
echo "🚀 Starting Terry-the-Tool-Bot..."
cd "$(dirname "$0")"
python3 terry_minimal.py "$@"
'''
            return launcher, "terry"
            
        elif platform_type == "gui":
            launcher = f'''#!/usr/bin/env python3
"""
Terry-the-Tool-Bot GUI Launcher
Cross-platform GUI application launcher
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the GUI
from terry_gui_simple import main

if __name__ == "__main__":
    main()
'''
            return launcher, "terry_gui.py"
    
    def create_desktop_entry(self):
        """Create .desktop file for Linux"""
        desktop_content = f'''[Desktop Entry]
Version={self.version}
Type=Application
Name=Terry-the-Tool-Bot
Comment=AI Coding Assistant
Exec={os.path.expanduser("~")}/.local/bin/terry-gui
Icon={os.path.expanduser("~")}/.local/share/icons/terry.png
Terminal=false
Categories=Development;
'''
        return desktop_content
    
    def create_windows_shortcut(self):
        """Create Windows shortcut content"""
        return f'''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\\SOFTWARE\\Classes\\TerryBot]
@="URL:Terry Bot Protocol"
"URL Protocol"=""

[HKEY_CURRENT_USER\\SOFTWARE\\Classes\\TerryBot\\shell\\open\\command]
@="python3 \\"%USERPROFILE%\\\\Terry\\\\terry_gui.py\\" \\"%1\\""
'''
    
    def create_package_structure(self, dest_dir):
        """Create the package structure with all necessary files"""
        dest_path = Path(dest_dir)
        dest_path.mkdir(exist_ok=True)
        
        # Copy essential files
        essential_files = [
            "terry_minimal.py",
            "terry_gui_simple.py",
            "README.md",
            "requirements.txt"
        ]
        
        for file_name in essential_files:
            src_file = self.project_root / file_name
            if src_file.exists():
                shutil.copy2(src_file, dest_path / file_name)
        
        # Create launchers
        windows_launcher, windows_name = self.create_launcher_script("windows")
        linux_launcher, linux_name = self.create_launcher_script("linux")
        gui_launcher, gui_name = self.create_launcher_script("gui")
        
        with open(dest_path / windows_name, 'w') as f:
            f.write(windows_launcher)
        
        with open(dest_path / linux_name, 'w') as f:
            f.write(linux_launcher)
            os.chmod(dest_path / linux_name, 0o755)
        
        with open(dest_path / gui_name, 'w') as f:
            f.write(gui_launcher)
            os.chmod(dest_path / gui_name, 0o755)
        
        # Create install scripts
        self.create_install_scripts(dest_path)
        
        return dest_path
    
    def create_install_scripts(self, dest_path):
        """Create platform-specific install scripts"""
        
        # Linux install script
        linux_install = '''#!/bin/bash
# Terry-the-Tool-Bot Linux Installer

echo "🚀 Installing Terry-the-Tool-Bot on Linux..."

# Create directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons

# Copy files
cp -r . ~/.local/share/terry-the-tool-bot/
chmod +x ~/.local/share/terry-the-tool-bot/terry
chmod +x ~/.local/share/terry-the-tool-bot/terry_gui.py

# Create symlink
ln -sf ~/.local/share/terry-the-tool-bot/terry ~/.local/bin/terry
ln -sf ~/.local/share/terry-the-tool-bot/terry_gui.py ~/.local/bin/terry-gui

# Create desktop entry
cat > ~/.local/share/applications/terry.desktop << 'EOF'
[Desktop Entry]
Version=2.0.0
Type=Application
Name=Terry-the-Tool-Bot
Comment=AI Coding Assistant
Exec=~/.local/bin/terry-gui
Icon=~/.local/share/icons/terry.png
Terminal=false
Categories=Development;
EOF

# Install dependencies
pip3 install -r ~/.local/share/terry-the-tool-bot/requirements.txt --user

echo "✅ Installation complete!"
echo "Run 'terry' for CLI or 'terry-gui' for GUI"
echo "Or find Terry in your applications menu"
'''
        
        # Windows install script
        windows_install = '''@echo off
REM Terry-the-Tool-Bot Windows Installer

echo 🚀 Installing Terry-the-Tool-Bot on Windows...

REM Create installation directory
if not exist "%USERPROFILE%\\Terry" mkdir "%USERPROFILE%\\Terry"

REM Copy files
xcopy . "%USERPROFILE%\\Terry" /E /Y

REM Add to PATH
setx PATH "%PATH%;%USERPROFILE%\\Terry"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Terry Bot.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\Terry\\terry_gui.py'; $Shortcut.Save()"

REM Install dependencies
python -m pip install -r "%USERPROFILE%\\Terry\\requirements.txt"

echo ✅ Installation complete!
echo Run 'terry' from command line or use desktop shortcut
pause
'''
        
        with open(dest_path / "install-linux.sh", 'w') as f:
            f.write(linux_install)
            os.chmod(dest_path / "install-linux.sh", 0o755)
        
        with open(dest_path / "install-windows.bat", 'w') as f:
            f.write(windows_install)
    
    def create_linux_package(self):
        """Create Linux installation package"""
        print("🐧 Creating Linux package...")
        
        package_dir = self.project_root / "terry-linux-package"
        self.create_package_structure(package_dir)
        
        # Create tar.gz archive
        archive_name = f"{self.install_name}-linux-{self.version}.tar.gz"
        subprocess.run(['tar', '-czf', archive_name, '-C', self.project_root, 'terry-linux-package'], 
                      cwd=self.project_root)
        
        print(f"✅ Linux package created: {archive_name}")
        return archive_name
    
    def create_windows_package(self):
        """Create Windows installation package"""
        print("🪟 Creating Windows package...")
        
        package_dir = self.project_root / "terry-windows-package"
        self.create_package_structure(package_dir)
        
        # Create zip archive
        archive_name = f"{self.install_name}-windows-{self.version}.zip"
        with zipfile.ZipFile(self.project_root / archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Windows package created: {archive_name}")
        return archive_name
    
    def create_universal_installer(self):
        """Create a universal installer that detects platform"""
        installer_content = '''#!/usr/bin/env python3
"""
Terry-the-Tool-Bot Universal Installer
Automatically detects platform and installs Terry
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def install_terry():
    system = platform.system().lower()
    
    print(f"🚀 Installing Terry-the-Tool-Bot on {system.title()}...")
    
    if system == "linux" or system == "darwin":
        # Linux/macOS installation
        install_dir = Path.home() / ".local" / "share" / "terry-the-tool-bot"
        bin_dir = Path.home() / ".local" / "bin"
        
        # Create directories
        install_dir.mkdir(parents=True, exist_ok=True)
        bin_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        current_dir = Path(__file__).parent
        for file in current_dir.glob("*.py"):
            shutil.copy2(file, install_dir / file.name)
        
        # Create launchers
        launcher = '''#!/bin/bash
cd "{install_dir}"
python3 terry_gui.py "$@"
'''.format(install_dir=install_dir)
        
        launcher_path = bin_dir / "terry-gui"
        with open(launcher_path, 'w') as f:
            f.write(launcher)
        launcher_path.chmod(0o755)
        
        print("✅ Installation complete!")
        print(f"Run 'terry-gui' to start Terry")
        
    elif system == "windows":
        # Windows installation
        install_dir = Path.home() / "Terry"
        install_dir.mkdir(exist_ok=True)
        
        # Copy files
        current_dir = Path(__file__).parent
        for file in current_dir.glob("*.py"):
            shutil.copy2(file, install_dir / file.name)
        
        # Add to PATH
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, 
                           os.environ["PATH"] + f";{install_dir}")
            winreg.CloseKey(key)
        except:
            print("⚠️  Could not add to PATH automatically")
        
        print("✅ Installation complete!")
        print(f"Run 'python {install_dir}/terry_gui.py' to start Terry")

if __name__ == "__main__":
    install_terry()
'''
        
        with open(self.project_root / "install_terry.py", 'w') as f:
            f.write(installer_content)
        
        print("✅ Universal installer created: install_terry.py")

def main():
    """Main installation process"""
    installer = TerryInstaller()
    
    print("🎯 Terry-the-Tool-Bot Cross-Platform Installer")
    print("=" * 50)
    
    # Create requirements file
    installer.create_requirements_file()
    
    # Create packages
    linux_package = installer.create_linux_package()
    windows_package = installer.create_windows_package()
    installer.create_universal_installer()
    
    print("\n" + "=" * 50)
    print("✅ Installation packages created successfully!")
    print(f"\n📦 Linux Package: {linux_package}")
    print(f"📦 Windows Package: {windows_package}")
    print(f"📦 Universal Installer: install_terry.py")
    print("\n💡 Installation instructions:")
    print("Linux: Extract and run 'install-linux.sh'")
    print("Windows: Extract and run 'install-windows.bat'")
    print("Universal: Run 'python install_terry.py'")

if __name__ == "__main__":
    main()
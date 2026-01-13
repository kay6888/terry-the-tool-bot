#!/usr/bin/env python3
"""
Terry-the-Tool-Bot Ultra-Modern Installer
Creates installation packages for Linux and Windows
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import zipfile

class TerryUltraInstaller:
    """Ultra-Modern installer for Terry-the-Tool-Bot"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.install_name = "terry-the-tool-bot"
        self.version = "2.0.0"
        
    def create_package_structure(self, dest_dir):
        """Create package structure with ultra-modern files"""
        dest_path = Path(dest_dir)
        dest_path.mkdir(exist_ok=True)
        
        # Copy essential files
        essential_files = [
            "terry_minimal.py",
            "terry_gui_simple.py", 
            "terry_gui_ultra.py",
            "README.md",
            "requirements.txt"
        ]
        
        for file_name in essential_files:
            src_file = self.project_root / file_name
            if src_file.exists():
                shutil.copy2(src_file, dest_path / file_name)
        
        # Create launchers
        windows_launcher = '@echo off\\necho 🚀 Starting Terry-the-Tool-Bot Ultra...\\ncd /d "%~dp0"\\npython terry_gui_ultra.py\\npause\\n'
        linux_launcher = '#!/bin/bash\\necho "🚀 Starting Terry-the-Tool-Bot Ultra..."\\ncd "$(dirname "$0")"\\npython3 terry_gui_ultra.py\\n'
        
        with open(dest_path / "terry.bat", 'w') as f:
            f.write(windows_launcher)
        
        with open(dest_path / "terry", 'w') as f:
            f.write(linux_launcher)
            os.chmod(dest_path / "terry", 0o755)
        
        return dest_path
    
    def create_linux_package(self):
        """Create Linux installation package"""
        print("🐧 Creating Ultra-Modern Linux package...")
        
        package_dir = self.project_root / "terry-ultra-linux-package"
        self.create_package_structure(package_dir)
        
        # Create tar.gz archive
        archive_name = f"{self.install_name}-ultra-linux-{self.version}.tar.gz"
        subprocess.run(['tar', '-czf', archive_name, '-C', self.project_root, 'terry-ultra-linux-package'], 
                      cwd=self.project_root)
        
        print(f"✅ Ultra-Modern Linux package created: {archive_name}")
        return archive_name
    
    def create_windows_package(self):
        """Create Windows installation package"""
        print("🪟 Creating Ultra-Modern Windows package...")
        
        package_dir = self.project_root / "terry-ultra-windows-package"
        self.create_package_structure(package_dir)
        
        # Create zip archive
        archive_name = f"{self.install_name}-ultra-windows-{self.version}.zip"
        with zipfile.ZipFile(self.project_root / archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Ultra-Modern Windows package created: {archive_name}")
        return archive_name

def main():
    """Main installation process"""
    installer = TerryUltraInstaller()
    
    print("🎯 Terry-the-Tool-Bot Ultra-Modern Installer")
    print("=" * 60)
    
    # Create packages
    linux_package = installer.create_linux_package()
    windows_package = installer.create_windows_package()
    
    print("\\n" + "=" * 60)
    print("✅ Ultra-Modern installation packages created successfully!")
    print(f"\\n📦 Ultra-Modern Linux Package: {linux_package}")
    print(f"📦 Ultra-Modern Windows Package: {windows_package}")
    print("\\n💫 Features:")
    print("• Ultra-Modern Glass-morphism Design")
    print("• Animated Gradient Background")
    print("• Floating Particle Effects")
    print("• Quantum-Enhanced AI Responses")
    print("• Eye-Popping Animations")
    print("• Advanced Settings & Customization")
    print("\\n🚀 Ready to launch the future of AI assistants!")

if __name__ == "__main__":
    main()
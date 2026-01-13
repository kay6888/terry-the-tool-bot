#!/usr/bin/env python3
"""
Complete Terry Logo Installer
All logo variants included
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import zipfile

class TerryCompleteLogoInstaller:
    """Complete installer with all logo variants"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.install_name = "terry-the-tool-bot"
        self.version = "2.0.0"
        
    def create_complete_package_structure(self, dest_dir):
        """Create package structure with ALL logos"""
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
        
        # Create logos directory
        logos_dir = dest_path / "logos"
        logos_dir.mkdir(exist_ok=True)
        
        # Copy ALL logo files
        logo_files = [
            "terry_logo.svg",
            "terry_logo_small.svg", 
            "terry_logo_better.svg",
            "terry_logo_premium.svg",
            "terry_logo_robust.svg",
            "terry_logo_ultra_robust.svg"
        ]
        
        for logo_name in logo_files:
            src_file = self.project_root / logo_name
            if src_file.exists():
                shutil.copy2(src_file, logos_dir / logo_name)
        
        # Copy galleries
        gallery_files = [
            "terry_logo_complete_gallery.html",
            "terry_logo_showcase_enhanced.html"
        ]
        
        for gallery_name in gallery_files:
            src_file = self.project_root / gallery_name
            if src_file.exists():
                shutil.copy2(src_file, dest_path / gallery_name)
        
        # Create launchers
        windows_launcher = '@echo off\\necho 🚀 Starting Terry-the-Tool-Bot Complete...\\ncd /d "%~dp0"\\npython terry_gui_ultra.py\\npause\\n'
        linux_launcher = '#!/bin/bash\\necho "🚀 Starting Terry-the-Tool-Bot Complete..."\\ncd "$(dirname "$0")"\\npython3 terry_gui_ultra.py\\n'
        
        with open(dest_path / "terry.bat", 'w') as f:
            f.write(windows_launcher)
        
        with open(dest_path / "terry", 'w') as f:
            f.write(linux_launcher)
            os.chmod(dest_path / "terry", 0o755)
        
        # Create logo selector
        logo_selector = '''#!/usr/bin/env python3
"""
Terry Logo Selector
Choose your favorite Terry logo!
"""

import sys
from pathlib import Path

def show_logo_menu():
    """Display logo selection menu"""
    logos = [
        ("Original", "terry_logo.svg", "Classic purple design"),
        ("Enhanced", "terry_logo_better.svg", "Premium gradients and details"),
        ("Robust", "terry_logo_robust.svg", "Industrial gray/red theme"),
        ("Ultra-Robust", "terry_logo_ultra_robust.svg", "Heavy-duty industrial"),
        ("Premium", "terry_logo_premium.svg", "Ultimate design with sparkles")
    ]
    
    print("🎨 Choose Your Terry Logo:")
    print("=" * 50)
    
    for i, (name, file, desc) in enumerate(logos, 1):
        print(f"{i}. {name}")
        print(f"   📁 {file}")
        print(f"   💬 {desc}")
        print()
    
    try:
        choice = int(input("Enter logo number (1-5): "))
        if 1 <= choice <= len(logos):
            selected = logos[choice - 1]
            update_gui_logo(selected[1])
            print(f"✅ Updated GUI to use {selected[0]} logo!")
        else:
            print("❌ Invalid choice!")
    except (ValueError, KeyboardInterrupt):
        print("❌ No selection made.")

def update_gui_logo(logo_file):
    """Update the GUI to use selected logo"""
    gui_file = Path(__file__).parent / "terry_gui_ultra.py"
    
    if not gui_file.exists():
        print("❌ GUI file not found!")
        return
    
    # Read current GUI
    with open(gui_file, 'r') as f:
        content = f.read()
    
    # Update logo references
    content = content.replace('terry_logo_robust.svg', logo_file)
    
    # Save updated GUI
    with open(gui_file, 'w') as f:
        f.write(content)
    
    print(f"✅ GUI updated to use {logo_file}")

if __name__ == "__main__":
    show_logo_menu()
'''
        
        with open(dest_path / "logo_selector.py", 'w') as f:
            f.write(logo_selector)
        
        os.chmod(dest_path / "logo_selector.py", 0o755)
        
        return dest_path
    
    def create_complete_linux_package(self):
        """Create complete Linux package"""
        print("🐧 Creating Complete Logo Linux package...")
        
        package_dir = self.project_root / "terry-complete-linux-package"
        self.create_complete_package_structure(package_dir)
        
        archive_name = f"{self.install_name}-complete-linux-{self.version}.tar.gz"
        subprocess.run(['tar', '-czf', archive_name, '-C', self.project_root, 'terry-complete-linux-package'], 
                      cwd=self.project_root)
        
        print(f"✅ Complete Linux package created: {archive_name}")
        return archive_name
    
    def create_complete_windows_package(self):
        """Create complete Windows package"""
        print("🪟 Creating Complete Logo Windows package...")
        
        package_dir = self.project_root / "terry-complete-windows-package"
        self.create_complete_package_structure(package_dir)
        
        archive_name = f"{self.install_name}-complete-windows-{self.version}.zip"
        with zipfile.ZipFile(self.project_root / archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Complete Windows package created: {archive_name}")
        return archive_name

def main():
    """Main complete installation process"""
    installer = TerryCompleteLogoInstaller()
    
    print("🎯 Terry-the-Tool-Bot Complete Logo Installer")
    print("=" * 70)
    
    # Create complete packages
    linux_package = installer.create_complete_linux_package()
    windows_package = installer.create_complete_windows_package()
    
    print("\\n" + "=" * 70)
    print("✅ COMPLETE installation packages created successfully!")
    print(f"\\n📦 Complete Linux Package: {linux_package}")
    print(f"📦 Complete Windows Package: {windows_package}")
    print("\\n🎨 Complete Logo Collection:")
    print("  • Original (Classic Purple)")
    print("  • Enhanced (Premium Gradients)")
    print("  • Robust (Industrial Gray/Red)")
    print("  • Ultra-Robust (Heavy-Duty)")
    print("  • Premium (Ultimate Sparkles)")
    print("  • Logo Selector Tool")
    print("  • Complete Logo Galleries")
    print("\\n🚀 Ready for deployment with ALL logo options!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
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

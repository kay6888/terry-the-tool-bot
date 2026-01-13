#!/usr/bin/env python3
"""
Terry Recovery Builder - File Structure and Output Locations

Shows where all recovery files and artifacts are stored.
"""

import os
from pathlib import Path

def show_recovery_builder_structure():
    """Display the complete recovery builder file structure"""
    
    workspace = Path.home() / ".terry_toolbot" / "recovery_builder"
    
    print("📁 Terry Recovery Builder - Complete File Structure")
    print("=" * 60)
    print(f"🏠 Main Workspace: {workspace}")
    print()
    
    structure = {
        "📂 RECOVERY BUILDER WORKSPACE": workspace,
        "  📂 sources": workspace / "sources",
        "    📂 twrp": workspace / "sources" / "twrp",
        "    📂 orange_fox": workspace / "sources" / "orange_fox", 
        "    📂 device_trees": workspace / "sources" / "device_trees",
        "    📂 custom_trees": workspace / "sources" / "custom_trees",
        "  📂 builds": workspace / "builds",
        "    📂 twrp": workspace / "builds" / "twrp",
        "    📂 orange_fox": workspace / "builds" / "orange_fox",
        "    📂 custom": workspace / "builds" / "custom",
        "  📂 artifacts": workspace / "artifacts",  # ⭐ FINAL RECOVERY FILES
        "  📂 roomservice": workspace / "roomservice",
        "  📂 logs": workspace / "logs",
        "  📂 cache": workspace / "cache",
        "  📂 tools": workspace / "tools"
    }
    
    for description, path in structure.items():
        exists = "✅" if path.exists() else "🔨"
        print(f"{exists} {description}")
        if path.exists():
            items = list(path.iterdir())
            if items:
                item_count = len(items)
                print(f"    📄 {item_count} items")
                # Show recent items
                recent = sorted(items, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
                for item in recent:
                    if item.is_file():
                        size = f"({item.stat().st_size:,} bytes)" if item.stat().st_size > 1000 else f"({item.stat().st_size} bytes)"
                        print(f"      📄 {item.name} {size}")
                    else:
                        sub_items = list(item.iterdir())
                        print(f"      📂 {item.name} ({len(sub_items)} items)")
        print()
    
    print("🎯 WHERE BUILT RECOVERIES ARE SAVED:")
    print("─" * 50)
    
    artifacts_dir = workspace / "artifacts"
    print(f"📁 FINAL RECOVERY FILES: {artifacts_dir}")
    print()
    
    if artifacts_dir.exists():
        files = list(artifacts_dir.glob("*.img"))
        zips = list(artifacts_dir.glob("*.zip"))
        logs = list(artifacts_dir.glob("*.log"))
        
        if files:
            print("📱 Built Recovery Images:")
            for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  📄 {file.name} ({size_mb:.1f} MB)")
        
        if zips:
            print("📦 Flashable ZIP Files:")
            for file in sorted(zips, key=lambda x: x.stat().st_mtime, reverse=True):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  📦 {file.name} ({size_mb:.1f} MB)")
        
        if logs:
            print("📋 Build Logs:")
            for file in sorted(logs, key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
                print(f"  📋 {file.name}")
    else:
        print("🔨 No recoveries built yet")
        print("💡 Use 'build twrp [device]' or 'build orange fox [device]' to start building!")
    
    print()
    print("📋 ROOMSERVICE.XML FILES:")
    print("─" * 30)
    roomservice_dir = workspace / "roomservice"
    if roomservice_dir.exists():
        xml_files = list(roomservice_dir.glob("*.xml"))
        if xml_files:
            for file in sorted(xml_files):
                print(f"  📄 {file.name}")
        else:
            print("  🔨 No roomservice files yet")
    else:
        print("  🔨 Roomservice directory not created yet")
    
    print()
    print("📂 EXAMPLE FILE PATHS AFTER BUILD:")
    print("─" * 40)
    
    examples = [
        f"📄 TWRP for beryllium: {artifacts_dir}/twrp_beryllium_20240113_103045.img",
        f"📄 Orange Fox for guacamole: {artifacts_dir}/orange_fox_guacamole_20240113_103045.img", 
        f"📋 TWRP Build Log: {artifacts_dir}/twrp_beryllium_20240113_103045_build.log",
        f"📋 Orange Fox Build Log: {artifacts_dir}/orange_fox_guacamole_20240113_103045_build.log",
        f"📄 Roomservice XML: {roomservice_dir}/roomservice_beryllium.xml",
        f"📄 Custom Device DB: {workspace}/custom_devices.json",
        f"📄 Build Report: {artifacts_dir}/build_report_20240113_103045.json"
    ]
    
    for example in examples:
        print(f"  {example}")
    
    print()
    print("🔍 QUICK ACCESS COMMANDS:")
    print("─" * 30)
    print(f"📁 cd {artifacts_dir}")
    print(f"📁 cd {roomservice_dir}")
    print(f"📁 cd {workspace}")
    print("📊 ls -la *.img  # List all recovery images")
    print("📊 ls -la *.zip  # List all flashable ZIPs")
    print("📊 ls -la *.log  # List all build logs")
    
    print()
    print("💡 FILE NAMING CONVENTION:")
    print("─" * 30)
    print("📄 Recovery Images: {recovery_type}_{device_codename}_{timestamp}.img")
    print("📦 Flashable ZIPs: {recovery_type}_{device_codename}_{timestamp}.zip")
    print("📋 Build Logs: {recovery_type}_{device_codename}_{timestamp}_build.log")
    print("📋 Roomservice: roomservice_{device_codename}.xml")
    print("📊 Reports: build_report_{timestamp}.json")

if __name__ == "__main__":
    show_recovery_builder_structure()
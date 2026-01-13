#!/usr/bin/env python3
"""
Create Demo Roomservice.xml Files

Generates example roomservice.xml files for supported devices.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from tools.recovery_builder import RecoveryBuilder, RecoveryType
    
    def create_demo_roomservice_files():
        """Create demo roomservice.xml files"""
        print("📄 Creating Demo Roomservice.xml Files")
        print("=" * 50)
        
        builder = RecoveryBuilder()
        
        # Create roomservice for some key devices
        demo_devices = ["beryllium", "begonia", "guacamole", "redfin"]
        
        for device in demo_devices:
            print(f"📄 Creating roomservice.xml for {device}...")
            
            # Generate for TWRP
            success = builder.setup_roomservice_xml(device, RecoveryType.TWRP)
            if success:
                roomservice_file = builder.get_roomservice_file(device)
                print(f"   ✅ TWRP: {roomservice_file}")
                
                # Show file size
                if roomservice_file.exists():
                    size = roomservice_file.stat().st_size
                    lines = len(roomservice_file.read_text().split('\\n'))
                    print(f"      📏 Size: {size:,} bytes, {lines} lines")
            
            # Generate for Orange Fox
            success = builder.setup_roomservice_xml(device, RecoveryType.ORANGE_FOX)
            if success:
                roomservice_file = builder.get_roomservice_file(device)
                print(f"   ✅ Orange Fox: {roomservice_file}")
                
                # Show file size
                if roomservice_file.exists():
                    size = roomservice_file.stat().st_size
                    lines = len(roomservice_file.read_text().split('\\n'))
                    print(f"      📏 Size: {size:,} bytes, {lines} lines")
            
            print()
        
        # Show all created files
        roomservice_dir = builder.workspace_dir / "roomservice"
        if roomservice_dir.exists():
            xml_files = list(roomservice_dir.glob("*.xml"))
            print(f"📄 Total roomservice.xml files created: {len(xml_files)}")
            
            for xml_file in xml_files:
                size = xml_file.stat().st_size
                print(f"   📄 {xml_file.name} ({size:,} bytes)")
        
        print()
        print("🎯 Roomservice.xml Generation Complete!")
        print("📁 Files saved to:", roomservice_dir)
        
        # Show sample content
        print("\\n📝 Sample roomservice.xml content (beryllium TWRP):")
        print("─" * 55)
        beryllium_file = roomservice_dir / "roomservice_beryllium.xml"
        if beryllium_file.exists():
            content = beryllium_file.read_text()
            lines = content.split('\\n')
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:2d}: {line}")
            if len(lines) > 20:
                print(f"... and {len(lines) - 20} more lines")
        
        print("\\n💡 Roomservice.xml files are now ready for use!")
        print("🔧 These can be used with repo sync commands in recovery building.")
    
    if __name__ == "__main__":
        create_demo_roomservice_files()
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Demo failed: {e}")
    import traceback
    traceback.print_exc()
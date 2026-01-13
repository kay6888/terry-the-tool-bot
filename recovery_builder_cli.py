#!/usr/bin/env python3
"""
Recovery Builder CLI - Terry's Recovery Building Interface

Command-line interface for building TWRP and Orange Fox recoveries.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.terry_bot import TerryToolBot

def main():
    """Main CLI interface"""
    print("🔧 Terry Recovery Builder CLI")
    print("=" * 50)
    
    # Initialize Terry
    terry = TerryToolBot()
    
    # Check recovery builder availability
    recovery_info = terry.get_recovery_builder_info()
    if not recovery_info['available']:
        print("❌ Recovery Builder is not available!")
        print("Please ensure all dependencies are installed.")
        return
    
    print(f"✅ Recovery Builder initialized")
    print(f"📱 Supported devices: {recovery_info['supported_devices']}")
    print(f"📁 Artifacts directory: {recovery_info['artifacts_directory']}")
    print()
    
    # Interactive loop
    while True:
        try:
            print("\\n" + "="*50)
            print("Available commands:")
            print("1. setup environment - Setup build environment")
            print("2. list devices - Show supported devices")  
            print("3. build twrp [device] - Build TWRP recovery")
            print("4. build orange fox [device] - Build Orange Fox recovery")
            print("5. status - Show build status")
            print("6. help - Show help")
            print("7. exit - Exit")
            print("="*50)
            
            command = input("🔧 Enter command: ").strip().lower()
            
            if command in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            if not command:
                continue
            
            # Process command
            response = terry.process_input(command)
            print(f"\\n🤖 Terry: {response}")
            
        except KeyboardInterrupt:
            print("\\n\\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\\n❌ Error: {e}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Terry-the-Tool-Bot - Advanced AI Coding Assistant

Main entry points for CLI and GUI interfaces.
"""

import sys
import argparse
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Terry-the-Tool-Bot - Advanced AI Coding Assistant')
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface')
    parser.add_argument('--quantum', action='store_true', help='Enable Quantum Code Synthesis Engine')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    if args.gui:
        # Launch GUI interface
        try:
            from gui.main_window import TerryMainWindow
            app = TerryMainWindow()
            app.run()
        except ImportError as e:
            print(f"❌ GUI not available: {e}")
            print("Please install GUI dependencies: pip install terry-tool-bot[gui]")
            return
    else:
        # Launch CLI interface
        try:
            from terry_bot import TerryToolBot
            
            bot = TerryToolBot()
            command = args.command if args.command else ""
            
            if args.quantum:
                print("🚀 Quantum Code Synthesis Engine enabled!")
            
            if args.debug:
                print("🔍 Debug mode enabled")
            
            if command:
                response = bot.process_input(command)
                print(f"🤖 Terry: {response}")
            else:
                bot.run()
            
        except ImportError as e:
            print(f"❌ Failed to import Terry: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Terry-the-Tool-Bot is shutting down...\n")

def main_gui():
    """GUI entry point"""
    try:
        from gui.main_window import TerryMainWindow
        app = TerryMainWindow()
        app.run()
    except ImportError as e:
        print(f"❌ GUI not available: {e}")
        print("Please install GUI dependencies: pip install terry-tool-bot[gui]")
        sys.exit(1)

if __name__ == '__main__':
    main()
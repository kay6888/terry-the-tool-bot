#!/usr/bin/env python3
"""
Simple test of Terry functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_terry():
    try:
        from terry_bot import TerryToolBot
        
        # Create Terry instance
        bot = TerryToolBot()
        
        # Test with a simple command
        test_command = "hello"
        print(f"Testing Terry with command: '{test_command}'")
        
        response = bot.process_input(test_command)
        print(f"Terry response: {response}")
        
        print("✅ Terry test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Terry test failed: {e}")
        return False

if __name__ == "__main__":
    test_terry()
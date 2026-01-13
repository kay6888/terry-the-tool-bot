#!/usr/bin/env python3
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

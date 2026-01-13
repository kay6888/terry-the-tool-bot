"""Terry-the-Tool-Bot - Advanced AI Coding Assistant

A revolutionary AI coding assistant specializing in Android development,
with Quantum Code Synthesis Engine capabilities.

Author: Terry Development Team
Version: 2.0.0
License: MIT
"""

__version__ = "2.0.0"
__author__ = "Terry Development Team"
__email__ = "terry@ai-assistant.dev"
__description__ = "Advanced AI coding assistant with Quantum Code Synthesis"

# Core imports
from .terry_bot import TerryToolBot
from .qcse.integration.terry_integration import QCSEIntegration

__all__ = [
    'TerryToolBot',
    'QCSEIntegration',
]
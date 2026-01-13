"""
Git Module - Comprehensive Git integration for Terry-the-Tool-Bot
Windows 10/11 optimized with cross-platform support
"""

from .cross_platform_git import GitManagerFactory, CrossPlatformGitManager
from .windows_git_manager import WindowsGitManager
from .terry_git_tool import TerryGitTool

__all__ = [
    'GitManagerFactory',
    'CrossPlatformGitManager', 
    'WindowsGitManager',
    'TerryGitTool'
]
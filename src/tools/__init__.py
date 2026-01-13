"""
Tools Module - Complete tool ecosystem for Terry-the-Tool-Bot
Windows 10/11 optimized with comprehensive Git integration
"""

# Core Tools (Existing)
# Note: Commented out missing tools until they're created
# from .android_builder import AndroidBuilderTool
# from .recovery_expert import RecoveryExpertTool
# from .imei_fixer import IMEIFixerTool
# from .web_scraper import WebScraperTool
# from .file_manager import FileManagerTool
# from .article_writer import ArticleWriterTool
# from .debug_master import DebugMasterTool

from .base_tool import BaseTool

# Git Integration (NEW - Fully Implemented)
from .git.cross_platform_git import GitManagerFactory, CrossPlatformGitManager
from .git.windows_git_manager import WindowsGitManager
from .git.terry_git_tool import TerryGitTool

# GitHub Integration (NEW - Fully Implemented)
from .github.github_desktop_integration import GitHubDesktopWindows
from .github.github_api_client import GitHubAPIClient

# GitLab Integration (NEW - Fully Implemented)
from .gitlab.gitlab_runner_windows import GitLabRunnerWindows

__all__ = [
    # Core Tools
    'BaseTool',
    # 'AndroidBuilderTool',  # Available when implemented
    # 'RecoveryExpertTool',  # Available when implemented
    # 'IMEIFixerTool',     # Available when implemented
    # 'WebScraperTool',    # Available when implemented
    # 'FileManagerTool',   # Available when implemented
    # 'ArticleWriterTool',  # Available when implemented
    # 'DebugMasterTool',   # Available when implemented
    
    # Git Integration (NEW - Ready)
    'GitManagerFactory',
    'CrossPlatformGitManager',
    'WindowsGitManager',
    'TerryGitTool',
    
    # GitHub Integration (NEW - Ready)
    'GitHubDesktopWindows',
    'GitHubAPIClient',
    
    # GitLab Integration (NEW - Ready)
    'GitLabRunnerWindows',
]
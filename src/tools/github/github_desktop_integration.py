"""
GitHub Desktop Integration - Windows-specific GitHub Desktop support
Provides seamless integration with GitHub Desktop for Windows users
"""

import os
import platform
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

class GitHubDesktopWindows:
    """GitHub Desktop integration for Windows"""
    
    def __init__(self):
        self.desktop_available = False
        self.winreg = None
        
        # Platform-specific initialization
        if platform.system() == "Windows":
            try:
                import winreg
                self.winreg = winreg
                self.desktop_available = True
            except ImportError:
                logging.warning("Windows registry module not available")
        
        self.desktop_path = self._find_github_desktop()
        
        if self.desktop_available:
            logging.info(f"GitHub Desktop found at: {self.desktop_path}")
        else:
            logging.info("GitHub Desktop not found - integration unavailable")
    
    def _find_github_desktop(self) -> Optional[str]:
        """Find GitHub Desktop installation on Windows"""
        # Only check on Windows
        if not self.desktop_available:
            return None
            
        # Check common installation paths
        possible_paths = [
            rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\GitHubDesktop\GitHubDesktop.exe",
            r"C:\Program Files\GitHub Desktop\GitHubDesktop.exe",
            r"C:\Program Files (x86)\GitHub Desktop\GitHubDesktop.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logging.info(f"Found GitHub Desktop at: {path}")
                return path
        
        # Check Windows Registry (only if available)
        if self.winreg:
            try:
                with self.winreg.OpenKey(self.winreg.HKEY_LOCAL_MACHINE, 
                                      r"SOFTWARE\GitHub\GitHubDesktop") as key:
                    install_path = self.winreg.QueryValueEx(key, "InstallPath")[0]
                    desktop_exe = os.path.join(install_path, "GitHubDesktop.exe")
                    if os.path.exists(desktop_exe):
                        logging.info(f"Found GitHub Desktop via registry: {desktop_exe}")
                        return desktop_exe
            except (FileNotFoundError, OSError) as e:
                logging.debug(f"Registry check failed: {e}")
            
            # Check user registry
            try:
                with self.winreg.OpenKey(self.winreg.HKEY_CURRENT_USER, 
                                      r"SOFTWARE\GitHub\GitHubDesktop") as key:
                    install_path = self.winreg.QueryValueEx(key, "InstallPath")[0]
                    desktop_exe = os.path.join(install_path, "GitHubDesktop.exe")
                    if os.path.exists(desktop_exe):
                        logging.info(f"Found GitHub Desktop via user registry: {desktop_exe}")
                        return desktop_exe
            except (FileNotFoundError, OSError) as e:
                logging.debug(f"User registry check failed: {e}")
        
        return None
    
    def open_repo_in_desktop(self, repo_path: str) -> Dict[str, Any]:
        """Open repository in GitHub Desktop"""
        if not self.desktop_available:
            return {
                'success': False,
                'error': 'GitHub Desktop not found',
                'suggestions': [
                    'Install GitHub Desktop from: https://desktop.github.com/',
                    'Use command-line Git operations instead'
                ]
            }
        
        try:
            # Normalize path for Windows
            normalized_path = self._normalize_windows_path(repo_path)
            
            logging.info(f"Opening repository in GitHub Desktop: {normalized_path}")
            
            result = subprocess.run([
                self.desktop_path, '--open-repo', normalized_path
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': f'Opened {repo_path} in GitHub Desktop',
                    'repo_path': repo_path,
                    'normalized_path': normalized_path,
                    'desktop_path': self.desktop_path
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to open in GitHub Desktop: {result.stderr}',
                    'repo_path': repo_path,
                    'return_code': result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'GitHub Desktop operation timeout',
                'repo_path': repo_path
            }
        except Exception as e:
            logging.error(f"Failed to open repo in GitHub Desktop: {e}")
            return {
                'success': False,
                'error': f'Failed to open in GitHub Desktop: {str(e)}',
                'repo_path': repo_path
            }
    
    def clone_with_desktop(self, repo_url: str, target_path: Optional[str] = None) -> Dict[str, Any]:
        """Clone repository using GitHub Desktop"""
        if not self.desktop_available:
            return {
                'success': False,
                'error': 'GitHub Desktop not found',
                'suggestions': [
                    'Install GitHub Desktop from: https://desktop.github.com/',
                    'Use Terry Git tool for cloning instead'
                ]
            }
        
        try:
            # Extract repo name and set default target path
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            clone_target = target_path or repo_name
            
            logging.info(f"Cloning {repo_url} using GitHub Desktop")
            
            result = subprocess.run([
                self.desktop_path, '--clone-repo', repo_url
            ], capture_output=True, text=True, timeout=300)  # 5 minutes timeout
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': f'Successfully cloned {repo_name} using GitHub Desktop',
                    'repo_url': repo_url,
                    'target_path': clone_target,
                    'repo_name': repo_name,
                    'desktop_path': self.desktop_path
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to clone with GitHub Desktop: {result.stderr}',
                    'repo_url': repo_url,
                    'return_code': result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'GitHub Desktop clone timeout',
                'repo_url': repo_url
            }
        except Exception as e:
            logging.error(f"Failed to clone with GitHub Desktop: {e}")
            return {
                'success': False,
                'error': f'Failed to clone with GitHub Desktop: {str(e)}',
                'repo_url': repo_url
            }
    
    def sync_with_desktop(self, repo_path: str) -> Dict[str, Any]:
        """Sync repository with GitHub Desktop"""
        if not self.desktop_available:
            return {
                'success': False,
                'error': 'GitHub Desktop not found'
            }
        
        try:
            normalized_path = self._normalize_windows_path(repo_path)
            
            logging.info(f"Syncing repository with GitHub Desktop: {normalized_path}")
            
            # GitHub Desktop doesn't have explicit sync command, 
            # but we can open the repo which triggers sync
            return self.open_repo_in_desktop(repo_path)
            
        except Exception as e:
            logging.error(f"Failed to sync with GitHub Desktop: {e}")
            return {
                'success': False,
                'error': f'Failed to sync with GitHub Desktop: {str(e)}',
                'repo_path': repo_path
            }
    
    def _normalize_windows_path(self, path: str) -> str:
        """Normalize path for GitHub Desktop on Windows"""
        if not path:
            return path
            
        # Convert to Path object for proper handling
        path_obj = Path(path)
        
        # Convert forward slashes to backslashes for GitHub Desktop
        windows_path = str(path_obj).replace('/', '\\')
        
        # Handle long paths
        if len(windows_path) > 260:
            absolute_path = path_obj.absolute()
            return f"\\\\?\\{absolute_path}"
            
        return windows_path
    
    def check_desktop_status(self) -> Dict[str, Any]:
        """Check GitHub Desktop status"""
        return {
            'available': self.desktop_available,
            'desktop_path': self.desktop_path,
            'version': self._get_desktop_version(),
            'installed_location': self.desktop_path,
            'platform': 'Windows'
        }
    
    def _get_desktop_version(self) -> Optional[str]:
        """Get GitHub Desktop version"""
        if not self.desktop_available:
            return None
            
        try:
            # Try to get version from executable properties
            result = subprocess.run([
                self.desktop_path, '--version'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.warning(f"Could not get GitHub Desktop version: {result.stderr}")
                return None
                
        except Exception as e:
            logging.debug(f"Failed to get GitHub Desktop version: {e}")
            return None
    
    def get_desktop_help(self) -> str:
        """Get GitHub Desktop integration help"""
        return """
🖥 GitHub Desktop Integration for Windows

📋 Available Operations:
• Open in GitHub Desktop - Open repository in GUI
• Clone with Desktop - Clone using GitHub Desktop interface
• Sync with Desktop - Sync repository with GitHub Desktop

⚙️ Features:
• Automatic GitHub Desktop detection
• Windows path handling (long paths, special characters)
• Registry-based installation detection
• Integration with Terry Git operations

💡 Requirements:
• GitHub Desktop installed on Windows 10/11
• Git for Windows installed
• Repository accessible locally

🔗 Installation:
Download GitHub Desktop from: https://desktop.github.com/

📖 Examples:
• "Open my-project in GitHub Desktop"
• "Clone https://github.com/user/repo with Desktop"
• "Sync repository with Desktop"
        """.strip()
    
    def validate_repo_path(self, repo_path: str) -> Dict[str, Any]:
        """Validate repository path for GitHub Desktop"""
        try:
            path_obj = Path(repo_path)
            
            # Check if path exists
            if not path_obj.exists():
                return {
                    'valid': False,
                    'error': f'Path does not exist: {repo_path}',
                    'suggestions': [
                        'Create the directory first',
                        'Check the path spelling',
                        'Use absolute path'
                    ]
                }
            
            # Check if it's a Git repository
            git_dir = path_obj / '.git'
            if not git_dir.exists():
                return {
                    'valid': False,
                    'error': f'Not a Git repository: {repo_path}',
                    'suggestions': [
                        'Initialize with: git init',
                        'Clone a repository first',
                        'Navigate to correct repository'
                    ]
                }
            
            return {
                'valid': True,
                'path': str(path_obj.absolute()),
                'is_git_repo': git_dir.exists(),
                'repo_name': path_obj.name
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Path validation failed: {str(e)}'
            }
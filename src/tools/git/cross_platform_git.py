"""
Cross-Platform Git Interface - Unified Git operations across Windows, macOS, and Linux
Provides platform-specific Git managers with consistent interface
"""

import platform
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

class CrossPlatformGitManager(ABC):
    """Abstract base class for platform-specific Git managers"""
    
    @abstractmethod
    def execute_git_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Execute Git command"""
        pass
    
    @abstractmethod
    def clone_repository(self, repo_url: str, target_path: str) -> Dict[str, Any]:
        """Clone repository"""
        pass
    
    @abstractmethod
    def get_status(self, repo_path: str = '.') -> Dict[str, Any]:
        """Get Git status"""
        pass
    
    @abstractmethod
    def commit_changes(self, message: str, files: Optional[list] = None, repo_path: str = '.') -> Dict[str, Any]:
        """Commit changes"""
        pass
    
    @abstractmethod
    def push_changes(self, remote: str = 'origin', branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Push changes to remote"""
        pass
    
    @abstractmethod
    def pull_changes(self, remote: str = 'origin', branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Pull changes from remote"""
        pass
    
    @abstractmethod
    def create_branch(self, branch_name: str, base_branch: str = 'main', repo_path: str = '.') -> Dict[str, Any]:
        """Create new branch"""
        pass
    
    @abstractmethod
    def merge_branch(self, source_branch: str, target_branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Merge branches"""
        pass


class WindowsGitManager(CrossPlatformGitManager):
    """Windows-specific Git manager using PowerShell integration"""
    
    def __init__(self):
        from .windows_git_manager import WindowsGitManager as WGM
        self._manager = WGM()
    
    def execute_git_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Execute Git command using Windows manager"""
        return self._manager.execute_git_command(command, cwd)
    
    def clone_repository(self, repo_url: str, target_path: str) -> Dict[str, Any]:
        """Clone repository using Windows manager"""
        return self._manager.clone_repository(repo_url, target_path)
    
    def get_status(self, repo_path: str = '.') -> Dict[str, Any]:
        """Get Git status using Windows manager"""
        return self._manager.get_status(repo_path)
    
    def commit_changes(self, message: str, files: Optional[list] = None, repo_path: str = '.') -> Dict[str, Any]:
        """Commit changes using Windows manager"""
        return self._manager.commit_changes(message, files, repo_path)
    
    def push_changes(self, remote: str = 'origin', branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Push changes using Windows manager"""
        # Push command for Windows
        command = f'push {remote}'
        if branch:
            command += f' {branch}'
        return self._manager.execute_git_command(command, repo_path)
    
    def pull_changes(self, remote: str = 'origin', branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Pull changes using Windows manager"""
        # Pull command for Windows
        command = f'pull {remote}'
        if branch:
            command += f' {branch}'
        return self._manager.execute_git_command(command, repo_path)
    
    def create_branch(self, branch_name: str, base_branch: str = 'main', repo_path: str = '.') -> Dict[str, Any]:
        """Create branch using Windows manager"""
        command = f'checkout -b {branch_name} {base_branch}'
        return self._manager.execute_git_command(command, repo_path)
    
    def merge_branch(self, source_branch: str, target_branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Merge branches using Windows manager"""
        # First ensure we're on the target branch
        if target_branch:
            checkout_result = self._manager.execute_git_command(f'checkout {target_branch}', repo_path)
            if not checkout_result['success']:
                return checkout_result
        
        # Merge the source branch
        command = f'merge {source_branch}'
        return self._manager.execute_git_command(command, repo_path)


class UnixGitManager(CrossPlatformGitManager):
    """Unix/Linux/macOS Git manager using shell commands"""
    
    def __init__(self):
        self.system = platform.system()
        self.git_executable = 'git'
        logging.info(f"Initialized UnixGitManager for {self.system}")
    
    def execute_git_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Execute Git command using shell"""
        import subprocess
        
        try:
            # Build full command
            full_command = f'cd "{cwd or os.getcwd()}" && {self.git_executable} {command}'
            
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=60
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_method': 'Shell',
                'platform': self.system
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timeout',
                'stdout': '',
                'stderr': '',
                'return_code': -1,
                'execution_method': 'Shell',
                'platform': self.system
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': '',
                'return_code': -1,
                'execution_method': 'Shell',
                'platform': self.system
            }
    
    def clone_repository(self, repo_url: str, target_path: str) -> Dict[str, Any]:
        """Clone repository on Unix systems"""
        import subprocess
        import os
        
        try:
            # Create target directory if it doesn't exist
            os.makedirs(target_path, exist_ok=True)
            
            command = f'clone {repo_url} "{target_path}"'
            result = self.execute_git_command(command)
            
            if result['success']:
                repo_name = repo_url.split('/')[-1].replace('.git', '')
                return {
                    'success': True,
                    'repository_path': target_path,
                    'repository_url': repo_url,
                    'repository_name': repo_name,
                    'message': f'Successfully cloned {repo_name}',
                    'platform': self.system
                }
            else:
                return {
                    'success': False,
                    'error': result.get('stderr', 'Clone failed'),
                    'platform': self.system
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Clone operation failed: {str(e)}',
                'platform': self.system
            }
    
    def get_status(self, repo_path: str = '.') -> Dict[str, Any]:
        """Get Git status on Unix systems"""
        import os
        
        try:
            # Change to repository directory
            original_cwd = os.getcwd()
            os.chdir(repo_path)
            
            result = self.execute_git_command('status --porcelain=v2')
            
            # Restore original directory
            os.chdir(original_cwd)
            
            if result['success']:
                import subprocess
                timestamp = subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
                return {
                    'success': True,
                    'status': result['stdout'],
                    'repo_path': repo_path,
                    'timestamp': timestamp,
                    'platform': self.system
                }
            else:
                return {
                    'success': False,
                    'error': result.get('stderr', 'Status command failed'),
                    'repo_path': repo_path,
                    'platform': self.system
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Status command failed: {str(e)}',
                'repo_path': repo_path,
                'platform': self.system
            }
    
    def commit_changes(self, message: str, files: Optional[list] = None, repo_path: str = '.') -> Dict[str, Any]:
        """Commit changes on Unix systems"""
        import os
        
        try:
            # Change to repository directory
            original_cwd = os.getcwd()
            os.chdir(repo_path)
            
            # Add files
            if files:
                for file_pattern in files:
                    add_result = self.execute_git_command(f'add "{file_pattern}"')
                    if not add_result['success']:
                        os.chdir(original_cwd)
                        return {
                            'success': False,
                            'error': f'Failed to add files: {add_result.get("stderr")}',
                            'platform': self.system
                        }
            else:
                # Add all changes
                add_result = self.execute_git_command('add -A')
                if not add_result['success']:
                    os.chdir(original_cwd)
                    return {
                        'success': False,
                        'error': f'Failed to add all files: {add_result.get("stderr")}',
                        'platform': self.system
                    }
            
            # Create commit
            commit_result = self.execute_git_command(f'commit -m "{message}"')
            
            # Restore original directory
            os.chdir(original_cwd)
            
            if commit_result['success']:
                # Get commit hash
                hash_result = self.execute_git_command('rev-parse HEAD')
                commit_hash = hash_result.get('stdout', '').strip() if hash_result['success'] else 'unknown'
                
                import subprocess
                timestamp = subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
                
                return {
                    'success': True,
                    'commit_hash': commit_hash,
                    'commit_message': message,
                    'repo_path': repo_path,
                    'timestamp': timestamp,
                    'platform': self.system
                }
            else:
                return {
                    'success': False,
                    'error': commit_result.get('stderr', 'Commit failed'),
                    'repo_path': repo_path,
                    'platform': self.system
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Commit operation failed: {str(e)}',
                'repo_path': repo_path,
                'platform': self.system
            }
    
    def push_changes(self, remote: str = 'origin', branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Push changes to remote on Unix systems"""
        command = f'push {remote}'
        if branch:
            command += f' {branch}'
        return self.execute_git_command(command, repo_path)
    
    def pull_changes(self, remote: str = 'origin', branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Pull changes from remote on Unix systems"""
        command = f'pull {remote}'
        if branch:
            command += f' {branch}'
        return self.execute_git_command(command, repo_path)
    
    def create_branch(self, branch_name: str, base_branch: str = 'main', repo_path: str = '.') -> Dict[str, Any]:
        """Create new branch on Unix systems"""
        command = f'checkout -b {branch_name} {base_branch}'
        return self.execute_git_command(command, repo_path)
    
    def merge_branch(self, source_branch: str, target_branch: str = None, repo_path: str = '.') -> Dict[str, Any]:
        """Merge branches on Unix systems"""
        # First ensure we're on the target branch
        if target_branch:
            checkout_result = self.execute_git_command(f'checkout {target_branch}', repo_path)
            if not checkout_result['success']:
                return checkout_result
        
        # Merge the source branch
        command = f'merge {source_branch}'
        return self.execute_git_command(command, repo_path)


class GitManagerFactory:
    """Factory for creating platform-specific Git managers"""
    
    @staticmethod
    def create_manager():
        """Create appropriate Git manager for current platform"""
        system = platform.system()
        
        logging.info(f"Creating Git manager for platform: {system}")
        
        if system == "Windows":
            return WindowsGitManager()
        elif system == "Darwin":  # macOS
            logging.info("Using UnixGitManager for macOS")
            return UnixGitManager()
        else:  # Linux and other Unix-like systems
            logging.info("Using UnixGitManager for Linux/Unix")
            return UnixGitManager()
    
    @staticmethod
    def get_platform_info():
        """Get platform information for Git operations"""
        system = platform.system()
        
        return {
            'system': system,
            'is_windows': system == "Windows",
            'is_macos': system == "Darwin",
            'is_linux': system == "Linux",
            'supports_powershell': system == "Windows",
            'path_separator': '\\' if system == "Windows" else '/',
            'git_executable': 'git.exe' if system == "Windows" else 'git'
        }
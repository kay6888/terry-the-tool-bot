"""
Windows Git Manager - Windows-specific Git operations for Terry-the-Tool-Bot
Handles Windows 10/11 compatibility with PowerShell integration and long path support
"""

import os
import platform
import subprocess
import ctypes
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

class WindowsGitManager:
    """Windows-specific Git operations manager"""
    
    def __init__(self):
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"
        self.git_executable = self._find_git_executable()
        self.use_powershell = self._should_use_powershell()
        
        if self.is_windows:
            self._configure_windows_git()
            logging.info("Windows Git Manager initialized")
        else:
            logging.warning(f"Not running on Windows, current platform: {self.platform}")
    
    def _find_git_executable(self) -> Optional[str]:
        """Find Git executable on Windows"""
        if not self.is_windows:
            return "git"
            
        git_paths = [
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files (x86)\Git\cmd\git.exe", 
            r"C:\Program Files\Git\bin\git.exe",
            rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\Programs\Git\cmd\git.exe"
        ]
        
        for path in git_paths:
            if os.path.exists(path):
                logging.info(f"Found Git at: {path}")
                return path
                
        # Check PATH
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            logging.info("Git found in PATH")
            return "git"
        except subprocess.CalledProcessError:
            logging.error("Git not found on system")
            return None
    
    def _configure_windows_git(self):
        """Configure Git for Windows compatibility"""
        if not self.git_executable:
            raise Exception("Git not found on Windows")
            
        windows_configs = {
            'core.autocrlf': 'true',      # Handle line endings
            'core.longpaths': 'true',      # Support long paths
            'core.symlinks': 'true',       # Enable symbolic links
            'core.filemode': 'false',      # Ignore permission bits
            'core.protectntfs': 'false'    # Allow NTFS operations
        }
        
        for key, value in windows_configs.items():
            try:
                subprocess.run([
                    self.git_executable, 'config', '--global', key, value
                ], check=True, capture_output=True)
                logging.info(f"Configured Git: {key} = {value}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to configure {key}: {e}")
    
    def _should_use_powershell(self) -> bool:
        """Determine if PowerShell should be used for Git commands"""
        if not self.is_windows:
            return False
            
        # Check if PowerShell 5+ is available
        try:
            result = subprocess.run([
                'powershell', '-Command', '$PSVersionTable.PSVersion.Major'
            ], capture_output=True, text=True, check=True)
            
            ps_version = int(result.stdout.strip())
            return ps_version >= 5
        except:
            return False
    
    def execute_git_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Execute Git command using appropriate Windows method"""
        if self.use_powershell:
            return self._execute_via_powershell(command, cwd)
        else:
            return self._execute_directly(command, cwd)
    
    def _execute_via_powershell(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Execute Git command through PowerShell for better Windows integration"""
        ps_script = f"""
        try {{
            Set-Location '{cwd or os.getcwd()}'
            
            # Enable progress reporting
            $ProgressPreference = 'Continue'
            
            # Execute git command
            $result = git {command}
            
            # Output result
            if ($result) {{
                Write-Output $result
            }}
            
            exit 0
        }} catch {{
            Write-Error $_.Exception.Message
            exit 1
        }}
        """
        
        try:
            result = subprocess.run([
                'powershell',
                '-NoProfile',           # Don't load profiles
                '-ExecutionPolicy', 'Bypass',  # Bypass execution policy
                '-Command', ps_script
            ], capture_output=True, text=True, cwd=cwd, timeout=60)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_method': 'PowerShell'
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timeout',
                'stdout': '',
                'stderr': '',
                'return_code': -1,
                'execution_method': 'PowerShell'
            }
    
    def _execute_directly(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Execute Git command directly"""
        try:
            result = subprocess.run([
                self.git_executable
            ] + command.split(), capture_output=True, text=True, cwd=cwd, timeout=60)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_method': 'Direct'
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timeout',
                'stdout': '',
                'stderr': '',
                'return_code': -1,
                'execution_method': 'Direct'
            }
    
    def handle_windows_paths(self, path: str) -> str:
        """Handle Windows-specific path issues"""
        if not self.is_windows:
            return path
            
        # Convert to Path object for proper handling
        path_obj = Path(path)
        
        # Normalize path separators
        normalized_path = str(path_obj)
        
        # Handle long paths (>260 characters)
        if len(normalized_path) > 260:
            # Use Windows extended-length path syntax
            absolute_path = path_obj.absolute()
            return f"\\\\?\\{absolute_path}"
            
        return normalized_path
    
    def get_windows_short_path(self, long_path: str) -> str:
        """Get Windows short path name for long paths"""
        try:
            buffer = ctypes.create_unicode_buffer(260)
            result = ctypes.windll.kernel32.GetShortPathNameW(long_path, buffer, 260)
            if result:
                short_path = buffer.value
                logging.info(f"Converted long path to short path: {short_path}")
                return short_path
        except Exception as e:
            logging.warning(f"Failed to get short path for {long_path}: {e}")
        return long_path
    
    def validate_repository_path(self, repo_path: str) -> Dict[str, Any]:
        """Validate repository path for Windows compatibility"""
        try:
            path_obj = Path(repo_path)
            
            # Check if path exists
            if not path_obj.exists():
                return {
                    'valid': False,
                    'error': f'Path does not exist: {repo_path}',
                    'suggestions': ['Create the directory', 'Check path spelling']
                }
            
            # Check for Windows path issues
            issues = []
            
            # Check for forbidden characters
            forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']
            if any(char in repo_path for char in forbidden_chars):
                issues.append('Contains forbidden characters')
            
            # Check path length
            if len(str(path_obj.absolute())) > 260:
                issues.append('Path exceeds 260 characters')
            
            # Check for reserved names
            reserved_names = ['CON', 'PRN', 'AUX', 'NUL'] + [f'COM{i}' for i in range(1, 10)] + [f'LPT{i}' for i in range(1, 10)]
            path_parts = path_obj.parts
            if any(part in reserved_names for part in path_parts):
                issues.append('Contains reserved name')
            
            return {
                'valid': len(issues) == 0,
                'issues': issues,
                'path': str(path_obj.absolute()),
                'suggestions': [
                    'Use shorter path names',
                    'Avoid special characters',
                    'Use subst to map long paths'
                ] if issues else []
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Path validation failed: {str(e)}'
            }
    
    def clone_repository(self, repo_url: str, target_path: str) -> Dict[str, Any]:
        """Clone repository with Windows path handling"""
        try:
            # Validate target path
            path_validation = self.validate_repository_path(target_path)
            if not path_validation['valid']:
                return {
                    'success': False,
                    'error': 'Invalid target path',
                    'details': path_validation
                }
            
            # Handle Windows path length issues
            clone_path = self.handle_windows_paths(target_path)
            
            logging.info(f"Cloning repository {repo_url} to {clone_path}")
            
            result = self.execute_git_command(f'clone {repo_url} "{clone_path}"')
            
            if result['success']:
                repo_name = repo_url.split('/')[-1].replace('.git', '')
                return {
                    'success': True,
                    'repository_path': clone_path,
                    'repository_url': repo_url,
                    'repository_name': repo_name,
                    'message': f'Successfully cloned {repo_name}',
                    'validation': path_validation
                }
            else:
                return {
                    'success': False,
                    'error': result.get('stderr', 'Clone failed'),
                    'execution_method': result.get('execution_method')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Clone operation failed: {str(e)}'
            }
    
    def get_status(self, repo_path: str = '.') -> Dict[str, Any]:
        """Get Git status with Windows compatibility"""
        try:
            # Change to repository directory
            original_cwd = os.getcwd()
            os.chdir(repo_path)
            
            result = self.execute_git_command('status --porcelain=v2')
            
            # Restore original directory
            os.chdir(original_cwd)
            
            if result['success']:
                return {
                    'success': True,
                    'status': result['stdout'],
                    'repo_path': repo_path,
                    'execution_method': result.get('execution_method'),
                    'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
                }
            else:
                return {
                    'success': False,
                    'error': result.get('stderr', 'Status command failed'),
                    'repo_path': repo_path
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Status command failed: {str(e)}',
                'repo_path': repo_path
            }
    
    def commit_changes(self, message: str, files: Optional[List[str]] = None, repo_path: str = '.') -> Dict[str, Any]:
        """Commit changes with platform-specific handling"""
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
                            'error': f'Failed to add files: {add_result.get("stderr")}'
                        }
            else:
                # Add all changes
                add_result = self.execute_git_command('add -A')
                if not add_result['success']:
                    os.chdir(original_cwd)
                    return {
                        'success': False,
                        'error': f'Failed to add all files: {add_result.get("stderr")}'
                    }
            
            # Create commit
            commit_result = self.execute_git_command(f'commit -m "{message}"')
            
            # Restore original directory
            os.chdir(original_cwd)
            
            if commit_result['success']:
                # Get commit hash
                hash_result = self.execute_git_command('rev-parse HEAD')
                commit_hash = hash_result.get('stdout', '').strip() if hash_result['success'] else 'unknown'
                
                return {
                    'success': True,
                    'commit_hash': commit_hash,
                    'commit_message': message,
                    'repo_path': repo_path,
                    'execution_method': commit_result.get('execution_method'),
                    'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
                }
            else:
                return {
                    'success': False,
                    'error': commit_result.get('stderr', 'Commit failed'),
                    'repo_path': repo_path
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Commit operation failed: {str(e)}',
                'repo_path': repo_path
            }
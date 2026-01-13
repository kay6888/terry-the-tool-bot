"""
GitLab Runner Windows - GitLab CI/CD integration for Windows 10/11
Provides GitLab Runner setup and management on Windows platforms
"""

import os
import platform
import subprocess
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

class GitLabRunnerWindows:
    """GitLab Runner management for Windows"""
    
    def __init__(self, gitlab_url: str, registration_token: str):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.registration_token = registration_token
        self.platform = platform.system()
        self.runner_executable = None
        self.is_windows = self.platform == "Windows"
        
        if self.is_windows:
            self.runner_executable = self._find_or_download_runner()
        
        logging.info(f"Initialized GitLab Runner manager for {self.platform}")
        logging.info(f"GitLab URL: {self.gitlab_url}")
    
    def _find_or_download_runner(self) -> Optional[str]:
        """Find or download GitLab Runner executable"""
        possible_paths = [
            r"C:\GitLab-Runner\gitlab-runner.exe",
            r"C:\Program Files\GitLab-Runner\gitlab-runner.exe",
            r"C:\Program Files (x86)\GitLab-Runner\gitlab-runner.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logging.info(f"Found GitLab Runner at: {path}")
                return path
        
        # If not found, offer to download
        logging.warning("GitLab Runner not found. Please download from GitLab instance.")
        logging.info(f"Download URL: {self.gitlab_url}/-/admin/runners/")
        
        return None
    
    def install_runner_windows(self, install_path: str = r"C:\GitLab-Runner", 
                            description: str = "Terry-the-Tool-Bot Windows Runner") -> Dict[str, Any]:
        """Install GitLab Runner as Windows service"""
        if not self.is_windows:
            return {
                'success': False,
                'error': 'This method is for Windows only',
                'platform': self.platform
            }
        
        if not self.runner_executable:
            return {
                'success': False,
                'error': 'GitLab Runner executable not available',
                'suggestions': [
                    'Download GitLab Runner from GitLab instance',
                    'Check installation path',
                    'Verify runner executable permissions'
                ]
            }
        
        try:
            # Create installation directory
            os.makedirs(install_path, exist_ok=True)
            
            # Copy runner to installation path (if not already there)
            runner_dest = os.path.join(install_path, "gitlab-runner.exe")
            if not os.path.exists(runner_dest):
                import shutil
                shutil.copy2(self.runner_executable, runner_dest)
                logging.info(f"Copied runner to: {runner_dest}")
            
            # Install as service
            install_cmd = [
                runner_dest,
                'install',
                '--url', self.gitlab_url,
                '--registration-token', self.registration_token,
                '--description', description,
                '--executor', 'shell',
                '--tag-list', 'windows,shell,terry-bot'
            ]
            
            logging.info("Installing GitLab Runner as service...")
            result = subprocess.run(install_cmd, capture_output=True, text=True, cwd=install_path)
            
            if result.returncode == 0:
                # Start the service
                logging.info("Starting GitLab Runner service...")
                start_result = subprocess.run([
                    runner_dest, 'start'
                ], capture_output=True, text=True, cwd=install_path)
                
                if start_result.returncode == 0:
                    return {
                        'success': True,
                        'message': 'GitLab Runner installed and started successfully',
                        'install_path': install_path,
                        'runner_executable': runner_dest,
                        'platform': self.platform,
                        'service_status': 'running',
                        'gitlab_url': self.gitlab_url
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Failed to start GitLab Runner service: {start_result.stderr}',
                        'install_path': install_path,
                        'platform': self.platform,
                        'service_status': 'stopped'
                    }
            else:
                return {
                    'success': False,
                    'error': f'Failed to install GitLab Runner: {result.stderr}',
                    'install_path': install_path,
                    'platform': self.platform
                }
                
        except Exception as e:
            logging.error(f"Failed to install GitLab Runner: {e}")
            return {
                'success': False,
                'error': f'Installation failed: {str(e)}',
                'platform': self.platform
            }
    
    def register_runner(self, runner_name: str = "Terry-Windows-Runner", 
                    tags: List[str] = None, 
                    executor: str = "shell") -> Dict[str, Any]:
        """Register GitLab Runner"""
        if not self.runner_executable:
            return {
                'success': False,
                'error': 'GitLab Runner executable not available'
            }
        
        try:
            register_cmd = [
                self.runner_executable,
                'register',
                '--url', self.gitlab_url,
                '--registration-token', self.registration_token,
                '--description', runner_name,
                '--executor', executor,
                '--tag-list', ','.join(tags or ['windows', 'terry-bot'])
            ]
            
            logging.info(f"Registering GitLab Runner: {runner_name}")
            result = subprocess.run(register_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': f'Successfully registered runner: {runner_name}',
                    'runner_name': runner_name,
                    'tags': tags or ['windows', 'terry-bot'],
                    'executor': executor,
                    'platform': self.platform
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to register runner: {result.stderr}',
                    'platform': self.platform
                }
                
        except Exception as e:
            logging.error(f"Failed to register GitLab Runner: {e}")
            return {
                'success': False,
                'error': f'Registration failed: {str(e)}',
                'platform': self.platform
            }
    
    def start_runner_service(self, install_path: str = r"C:\GitLab-Runner") -> Dict[str, Any]:
        """Start GitLab Runner service on Windows"""
        if not self.is_windows:
            return {
                'success': False,
                'error': 'This method is for Windows only',
                'platform': self.platform
            }
        
        runner_exe = os.path.join(install_path, "gitlab-runner.exe")
        
        if not os.path.exists(runner_exe):
            return {
                'success': False,
                'error': 'GitLab Runner not found at installation path',
                'install_path': install_path
            }
        
        try:
            start_cmd = [runner_exe, 'start']
            
            logging.info("Starting GitLab Runner service...")
            result = subprocess.run(start_cmd, capture_output=True, text=True, cwd=install_path)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'GitLab Runner service started successfully',
                    'install_path': install_path,
                    'service_status': 'running',
                    'platform': self.platform
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to start service: {result.stderr}',
                    'install_path': install_path,
                    'service_status': 'stopped'
                }
                
        except Exception as e:
            logging.error(f"Failed to start GitLab Runner service: {e}")
            return {
                'success': False,
                'error': f'Service start failed: {str(e)}',
                'install_path': install_path
            }
    
    def stop_runner_service(self, install_path: str = r"C:\GitLab-Runner") -> Dict[str, Any]:
        """Stop GitLab Runner service on Windows"""
        if not self.is_windows:
            return {
                'success': False,
                'error': 'This method is for Windows only',
                'platform': self.platform
            }
        
        runner_exe = os.path.join(install_path, "gitlab-runner.exe")
        
        if not os.path.exists(runner_exe):
            return {
                'success': False,
                'error': 'GitLab Runner not found at installation path',
                'install_path': install_path
            }
        
        try:
            stop_cmd = [runner_exe, 'stop']
            
            logging.info("Stopping GitLab Runner service...")
            result = subprocess.run(stop_cmd, capture_output=True, text=True, cwd=install_path)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'GitLab Runner service stopped successfully',
                    'install_path': install_path,
                    'service_status': 'stopped',
                    'platform': self.platform
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to stop service: {result.stderr}',
                    'install_path': install_path,
                    'service_status': 'running'
                }
                
        except Exception as e:
            logging.error(f"Failed to stop GitLab Runner service: {e}")
            return {
                'success': False,
                'error': f'Service stop failed: {str(e)}',
                'install_path': install_path
            }
    
    def get_runner_status(self, install_path: str = r"C:\GitLab-Runner") -> Dict[str, Any]:
        """Get GitLab Runner status"""
        if not self.is_windows:
            return {
                'success': False,
                'error': 'This method is for Windows only',
                'platform': self.platform
            }
        
        runner_exe = os.path.join(install_path, "gitlab-runner.exe")
        
        if not os.path.exists(runner_exe):
            return {
                'success': False,
                'error': 'GitLab Runner not found at installation path',
                'install_path': install_path,
                'service_status': 'not_installed'
            }
        
        try:
            status_cmd = [runner_exe, 'status']
            
            result = subprocess.run(status_cmd, capture_output=True, text=True, cwd=install_path)
            
            if result.returncode == 0:
                # Parse status output
                status_output = result.stdout
                return {
                    'success': True,
                    'status_output': status_output,
                    'service_status': 'active',
                    'install_path': install_path,
                    'platform': self.platform
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to get status: {result.stderr}',
                    'install_path': install_path,
                    'service_status': 'unknown'
                }
                
        except Exception as e:
            logging.error(f"Failed to get GitLab Runner status: {e}")
            return {
                'success': False,
                'error': f'Status check failed: {str(e)}',
                'install_path': install_path
            }
    
    def uninstall_runner(self, install_path: str = r"C:\GitLab-Runner") -> Dict[str, Any]:
        """Uninstall GitLab Runner from Windows"""
        if not self.is_windows:
            return {
                'success': False,
                'error': 'This method is for Windows only',
                'platform': self.platform
            }
        
        runner_exe = os.path.join(install_path, "gitlab-runner.exe")
        
        if not os.path.exists(runner_exe):
            return {
                'success': False,
                'error': 'GitLab Runner not found at installation path',
                'install_path': install_path
            }
        
        try:
            # Stop service first
            stop_result = self.stop_runner_service(install_path)
            
            if stop_result['success']:
                # Uninstall service
                uninstall_cmd = [runner_exe, 'uninstall']
                
                logging.info("Uninstalling GitLab Runner service...")
                result = subprocess.run(uninstall_cmd, capture_output=True, text=True, cwd=install_path)
                
                if result.returncode == 0:
                    # Remove installation directory
                    try:
                        import shutil
                        shutil.rmtree(install_path)
                        logging.info(f"Removed installation directory: {install_path}")
                    except Exception as e:
                        logging.warning(f"Failed to remove installation directory: {e}")
                    
                    return {
                        'success': True,
                        'message': 'GitLab Runner uninstalled successfully',
                        'install_path': install_path,
                        'platform': self.platform
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Failed to uninstall service: {result.stderr}',
                        'install_path': install_path
                    }
            else:
                return stop_result
                
        except Exception as e:
            logging.error(f"Failed to uninstall GitLab Runner: {e}")
            return {
                'success': False,
                'error': f'Uninstallation failed: {str(e)}',
                'install_path': install_path
            }
    
    def get_help_text(self) -> str:
        """Get help text for GitLab Runner operations"""
        return """
🏃 GitLab Runner Management for Windows 10/11

📋 Supported Operations:
• install-runner [path] - Install and register as Windows service
• register-runner <name> - Register runner with GitLab
• start-runner - Start runner service
• stop-runner - Stop runner service
• status-runner - Get runner status
• uninstall-runner - Uninstall runner service

⚙️ Features:
• Windows service installation and management
• Automatic runner registration
• Service status monitoring
• Windows-specific path handling
• Terry-the-Tool-Bot integration

🔧 Installation:
1. Download GitLab Runner from your GitLab instance
2. Use "install-runner" command for automatic setup
3. Runner will be installed as Windows service
4. Automatic start after installation

💡 Examples:
• install-runner "C:\GitLab-Runner"
• register-runner "Terry-Windows-Runner"
• start-runner
• stop-runner
• status-runner
• uninstall-runner

🛠️ Windows Integration:
• Native Windows service management
• Registry-compatible installation
• Windows path handling (long paths, special chars)
• PowerShell command execution
• Windows service controls

📝 Notes:
• Requires Windows Administrator privileges
• GitLab Runner executable must be available
• Registration token required for setup
• Service runs under SYSTEM account
        """.strip()
    
    def validate_windows_requirements(self) -> Dict[str, Any]:
        """Validate Windows requirements for GitLab Runner"""
        if not self.is_windows:
            return {
                'valid': False,
                'error': 'This module is for Windows only',
                'platform': self.platform
            }
        
        issues = []
        
        # Check Administrator privileges
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                issues.append('Administrator privileges required')
        except Exception:
            issues.append('Could not verify administrator privileges')
        
        # Check Windows version
        try:
            import sys
            if sys.getwindowsversion().major < 10:
                issues.append('Windows 10/11 required')
        except Exception:
            logging.debug("Could not determine Windows version")
        
        # Check PowerShell availability
        try:
            subprocess.run(['powershell', '-Command', 'Get-Host'], 
                         capture_output=True, check=True, timeout=5)
        except subprocess.CalledProcessError:
            issues.append('PowerShell not available')
        
        return {
            'valid': len(issues) == 0,
            'platform': self.platform,
            'issues': issues,
            'requirements': {
                'platform': 'Windows 10/11',
                'privileges': 'Administrator',
                'powershell': 'PowerShell 5+',
                'connectivity': 'GitLab instance access'
            },
            'suggestions': [
                'Run as Administrator',
                'Install GitLab Runner executable',
                'Ensure PowerShell 5+ is available',
                'Verify network connectivity to GitLab'
            ] if issues else []
        }
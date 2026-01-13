"""
Terry Git Tool - Comprehensive Git integration for Terry-the-Tool-Bot
Windows 10/11 optimized with cross-platform support
"""

import time
import platform
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import re

from .cross_platform_git import GitManagerFactory
from ..base_tool import BaseTool

class TerryGitTool(BaseTool):
    """Comprehensive Git integration tool for Terry-the-Tool-Bot with Windows support"""
    
    def __init__(self):
        super().__init__(
            name="terry_git",
            version="1.0.0",
            description="Advanced Git operations with Windows 10/11 compatibility"
        )
        
        self.platform = platform.system()
        self.git_manager = GitManagerFactory.create_manager()
        self.platform_info = GitManagerFactory.get_platform_info()
        
        logging.info(f"Initialized TerryGitTool for {self.platform}")
        logging.info(f"Platform info: {self.platform_info}")
        
        # Platform-specific initialization
        if self.platform == "Windows":
            self._initialize_windows_support()
    
    def _initialize_windows_support(self):
        """Initialize Windows-specific Git support"""
        logging.info("Initializing Windows-specific Git features")
        
        # Check for Windows-specific requirements
        try:
            import subprocess
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Git version: {result.stdout.strip()}")
            else:
                logging.warning("Git not found or not properly installed")
        except Exception as e:
            logging.error(f"Failed to check Git installation: {e}")
    
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Git operations based on user input"""
        start_time = time.time()
        
        try:
            # Parse user intent
            operation = self._parse_git_intent(user_input)
            
            if not operation:
                return self._format_response(
                    'error', 
                    'Could not determine Git operation from input',
                    execution_time=time.time() - start_time,
                    suggestions=[
                        'Try: "clone https://github.com/user/repo.git"',
                        'Try: "commit with message"',
                        'Try: "push to origin"',
                        'Try: "check status"'
                    ]
                )
            
            # Execute the operation
            result = self._execute_git_operation(operation, context)
            
            return self._format_response(
                'success',
                f'Git operation {operation["type"]} completed successfully',
                data=result,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logging.error(f"Git operation failed: {str(e)}")
            return self._format_response(
                'error',
                f'Git operation failed: {str(e)}',
                execution_time=time.time() - start_time
            )
    
    def _parse_git_intent(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Parse user input to determine Git operation"""
        input_lower = user_input.lower()
        
        # Comprehensive Git operation patterns
        operations = {
            # Repository operations
            'clone': {
                'patterns': [
                    r'clone\s+(https?://[^\s]+)',
                    r'clone\s+(git@[^\s]+)',
                    r'clone\s+([^\s]+\.[^\s]+)'
                ],
                'extract_args': lambda match: [match.group(1)] if match else []
            },
            
            # Commit operations
            'commit': {
                'patterns': [
                    r'commit\s+with\s+message\s+["\']?([^"\'\n]+)["\']?',
                    r'commit\s+["\']?([^"\'\n]+)["\']?',
                    r'commit\s+-m\s+["\']?([^"\'\n]+)["\']?'
                ],
                'extract_args': lambda match: [match.group(1)] if match else []
            },
            
            # Push operations
            'push': {
                'patterns': [
                    r'push\s+(?:to\s+)?([^\s]+)?',
                    r'push\s+(?:origin|upstream|remote)?',
                    r'push\s+(?:to\s+)?origin(?:\s+.+)?'
                ],
                'extract_args': lambda match: [arg.strip() for arg in match.groups() if arg and arg.strip()]
            },
            
            # Pull operations
            'pull': {
                'patterns': [
                    r'pull\s+(?:from\s+)?([^\s]+)?',
                    r'pull\s+(?:origin|upstream|remote)?',
                    r'pull\s+(?:from\s+)?origin(?:\s+.+)?'
                ],
                'extract_args': lambda match: [arg.strip() for arg in match.groups() if arg and arg.strip()]
            },
            
            # Branch operations
            'branch': {
                'patterns': [
                    r'(?:create|new)\s+branch\s+([^\s]+)',
                    r'create\s+branch\s+([^\s]+)',
                    r'checkout\s+-b\s+([^\s]+)',
                    r'branch\s+([^\s]+)'
                ],
                'extract_args': lambda match: [match.group(1)] if match else []
            },
            
            # Merge operations
            'merge': {
                'patterns': [
                    r'merge\s+([^\s]+)',
                    r'merge\s+([^\s]+)\s+into\s+([^\s]+)'
                ],
                'extract_args': lambda match: [arg for arg in match.groups() if arg and arg.strip()]
            },
            
            # Status operations
            'status': {
                'patterns': [
                    r'(?:git\s+)?status',
                    r'check\s+status',
                    r'get\s+status',
                    r'show\s+status'
                ],
                'extract_args': lambda match: []
            },
            
            # Init operations
            'init': {
                'patterns': [
                    r'init\s+(?:repo|repository)?\s*([^\s]+)?',
                    r'initialize\s+(?:repo|repository)?\s*([^\s]+)?',
                    r'create\s+(?:repo|repository)?\s*([^\s]+)?'
                ],
                'extract_args': lambda match: [match.group(1)] if match and match.group(1) else ['.']
            },
            
            # Add operations
            'add': {
                'patterns': [
                    r'add\s+([^\s]+)',
                    r'stage\s+([^\s]+)',
                    r'add\s+all',
                    r'add\s+\.'
                ],
                'extract_args': lambda match: [match.group(1)] if match else ['.']
            }
        }
        
        # Try to match operations
        for op_type, op_config in operations.items():
            for pattern in op_config['patterns']:
                match = re.search(pattern, input_lower)
                if match:
                    args = op_config['extract_args'](match)
                    return {
                        'type': op_type,
                        'args': args,
                        'raw_input': user_input,
                        'matched_pattern': pattern
                    }
        
        return None
    
    def _execute_git_operation(self, operation: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parsed Git operation"""
        op_type = operation['type']
        args = operation['args']
        
        logging.info(f"Executing Git operation: {op_type} with args: {args}")
        
        # Route to appropriate method
        if op_type == 'clone':
            return self._handle_clone_operation(args, context)
        elif op_type == 'commit':
            return self._handle_commit_operation(args, context)
        elif op_type == 'push':
            return self._handle_push_operation(args, context)
        elif op_type == 'pull':
            return self._handle_pull_operation(args, context)
        elif op_type == 'branch':
            return self._handle_branch_operation(args, context)
        elif op_type == 'merge':
            return self._handle_merge_operation(args, context)
        elif op_type == 'status':
            return self._handle_status_operation(context)
        elif op_type == 'init':
            return self._handle_init_operation(args, context)
        elif op_type == 'add':
            return self._handle_add_operation(args, context)
        else:
            raise ValueError(f"Unsupported Git operation: {op_type}")
    
    def _handle_clone_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle repository cloning operation"""
        if not args:
            return {'error': 'Repository URL required for clone operation'}
        
        repo_url = args[0]
        # Extract repo name from URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        target_path = repo_name
        
        return self.git_manager.clone_repository(repo_url, target_path)
    
    def _handle_commit_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle commit operation"""
        message = args[0] if args else "Auto-commit by Terry-the-Tool-Bot"
        
        # Try to get current working directory from context
        repo_path = context.get('current_directory', '.')
        
        return self.git_manager.commit_changes(message, repo_path=repo_path)
    
    def _handle_push_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle push operation"""
        remote = args[0] if args else 'origin'
        branch = args[1] if len(args) > 1 else None
        
        repo_path = context.get('current_directory', '.')
        
        return self.git_manager.push_changes(remote, branch, repo_path)
    
    def _handle_pull_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pull operation"""
        remote = args[0] if args else 'origin'
        branch = args[1] if len(args) > 1 else None
        
        repo_path = context.get('current_directory', '.')
        
        return self.git_manager.pull_changes(remote, branch, repo_path)
    
    def _handle_branch_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle branch operation"""
        if not args:
            return {'error': 'Branch name required'}
        
        branch_name = args[0]
        base_branch = args[1] if len(args) > 1 else 'main'
        
        repo_path = context.get('current_directory', '.')
        
        return self.git_manager.create_branch(branch_name, base_branch, repo_path)
    
    def _handle_merge_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle merge operation"""
        if not args:
            return {'error': 'Source branch required for merge'}
        
        source_branch = args[0]
        target_branch = args[1] if len(args) > 1 else None
        
        repo_path = context.get('current_directory', '.')
        
        return self.git_manager.merge_branch(source_branch, target_branch, repo_path)
    
    def _handle_status_operation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle status operation"""
        repo_path = context.get('current_directory', '.')
        
        return self.git_manager.get_status(repo_path)
    
    def _handle_init_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle repository initialization"""
        target_path = args[0] if args else '.'
        
        return self.git_manager.execute_git_command(f'init "{target_path}"', target_path)
    
    def _handle_add_operation(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle add operation"""
        if not args:
            return {'error': 'Files or patterns required for add operation'}
        
        repo_path = context.get('current_directory', '.')
        
        # Add each file/pattern
        results = []
        for file_pattern in args:
            result = self.git_manager.execute_git_command(f'add "{file_pattern}"', repo_path)
            results.append({
                'file_pattern': file_pattern,
                'result': result
            })
        
        return {
            'success': all(r['result']['success'] for r in results),
            'files_added': len(results),
            'details': results
        }
    
    def validate_input(self, user_input: str) -> bool:
        """Validate if input is suitable for Git operations"""
        # Check for Git-related keywords
        git_keywords = [
            'clone', 'commit', 'push', 'pull', 'branch', 
            'merge', 'status', 'add', 'init', 'checkout',
            'repository', 'repo', 'git'
        ]
        
        return any(keyword in user_input.lower() for keyword in git_keywords)
    
    def get_help_text(self) -> str:
        """Get help text for Git operations"""
        return """
🔧 Terry Git Tool - Comprehensive Git Operations

📋 Supported Operations:
• clone <url> - Clone a repository
• commit with message "<message>" - Commit changes
• push [remote] [branch] - Push to remote
• pull [remote] [branch] - Pull from remote  
• create branch <name> - Create new branch
• merge <source> [into <target>] - Merge branches
• status - Show repository status
• init [path] - Initialize repository
• add <files> - Add files to staging

🌐 Platform Support:
• Windows 10/11 with PowerShell integration
• macOS with shell commands
• Linux with bash commands
• Long path support on Windows
• Cross-platform path handling

💡 Examples:
• "clone https://github.com/user/repo.git"
• "commit with message 'Fixed bug in login'"
• "push to origin main"  
• "create branch feature/new-ui"
• "merge feature/new-ui into main"
• "check status"
        """.strip()
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current Git tool status"""
        return {
            'platform': self.platform,
            'platform_info': self.platform_info,
            'git_manager_type': type(self.git_manager).__name__,
            'supported_operations': [
                'clone', 'commit', 'push', 'pull', 
                'branch', 'merge', 'status', 'init', 'add'
            ],
            'windows_features': self.platform == 'Windows',
            'powershell_available': self.platform_info.get('supports_powershell', False)
        }
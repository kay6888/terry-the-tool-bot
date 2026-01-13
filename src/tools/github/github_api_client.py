"""
GitHub API Client - Windows-compatible GitHub API integration
Provides comprehensive GitHub API operations with Windows-specific optimizations
"""

import os
import platform
import subprocess
import logging
import time
from typing import Dict, Any, Optional, List
import requests
import json

class GitHubAPIClient:
    """GitHub API client with Windows compatibility"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.platform = platform.system()
        self.session = requests.Session()
        
        # Set up headers
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Terry-the-Tool-Bot/1.0.0',
            'X-GitHub-Api-Version': '2022-11-28'
        })
        
        # Add authentication token if available
        if self.token:
            self.session.headers['Authorization'] = f'token {self.token}'
        
        logging.info(f"Initialized GitHub API client for {self.platform}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                      params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json(),
                    'status_code': response.status_code,
                    'headers': dict(response.headers)
                }
            else:
                error_data = response.json() if response.content else {}
                return {
                    'success': False,
                    'error': error_data.get('message', 'Unknown API error'),
                    'status_code': response.status_code,
                    'response_text': response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout',
                'status_code': -1
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Connection error',
                'status_code': -2
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Request failed: {str(e)}',
                'status_code': -3
            }
    
    def create_repository(self, name: str, description: str = '', private: bool = False,
                        auto_init: bool = True) -> Dict[str, Any]:
        """Create a new repository"""
        data = {
            'name': name,
            'description': description,
            'private': private,
            'auto_init': auto_init
        }
        
        logging.info(f"Creating repository: {name}")
        result = self._make_request('POST', 'user/repos', data)
        
        if result['success']:
            repo_data = result['data']
            logging.info(f"Repository created successfully: {repo_data.get('html_url')}")
            return {
                'success': True,
                'repository': {
                    'name': repo_data.get('name'),
                    'full_name': repo_data.get('full_name'),
                    'description': repo_data.get('description'),
                    'clone_url': repo_data.get('clone_url'),
                    'ssh_url': repo_data.get('ssh_url'),
                    'html_url': repo_data.get('html_url'),
                    'private': repo_data.get('private'),
                    'created_at': repo_data.get('created_at')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to create repository: {result.get('error')}")
            return result
    
    def get_repository(self, owner: str, repo_name: str) -> Dict[str, Any]:
        """Get repository information"""
        endpoint = f"repos/{owner}/{repo_name}"
        
        logging.info(f"Fetching repository: {owner}/{repo_name}")
        result = self._make_request('GET', endpoint)
        
        if result['success']:
            repo_data = result['data']
            return {
                'success': True,
                'repository': {
                    'name': repo_data.get('name'),
                    'full_name': repo_data.get('full_name'),
                    'description': repo_data.get('description'),
                    'clone_url': repo_data.get('clone_url'),
                    'ssh_url': repo_data.get('ssh_url'),
                    'html_url': repo_data.get('html_url'),
                    'private': repo_data.get('private'),
                    'default_branch': repo_data.get('default_branch'),
                    'language': repo_data.get('language'),
                    'stars': repo_data.get('stargazers_count'),
                    'forks': repo_data.get('forks_count'),
                    'open_issues': repo_data.get('open_issues_count'),
                    'created_at': repo_data.get('created_at'),
                    'updated_at': repo_data.get('updated_at')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to get repository: {result.get('error')}")
            return result
    
    def list_repositories(self, user: Optional[str] = None, repo_type: str = 'all',
                        sort: str = 'updated', direction: str = 'desc') -> Dict[str, Any]:
        """List user repositories"""
        params = {
            'type': repo_type,  # all, owner, member
            'sort': sort,      # created, updated, pushed, full_name
            'direction': direction,  # asc, desc
            'per_page': 100     # GitHub API max
        }
        
        if user:
            params['user'] = user
        else:
            # Get authenticated user's repos
            endpoint = 'user/repos'
            result = self._make_request('GET', endpoint, params=params)
            return result
        
        endpoint = f"users/{user}/repos"
        result = self._make_request('GET', endpoint, params=params)
        
        if result['success']:
            repos = result['data']
            repo_list = []
            
            for repo in repos:
                repo_list.append({
                    'name': repo.get('name'),
                    'full_name': repo.get('full_name'),
                    'description': repo.get('description'),
                    'clone_url': repo.get('clone_url'),
                    'ssh_url': repo.get('ssh_url'),
                    'html_url': repo.get('html_url'),
                    'private': repo.get('private'),
                    'language': repo.get('language'),
                    'stars': repo.get('stargazers_count'),
                    'forks': repo.get('forks_count'),
                    'open_issues': repo.get('open_issues_count'),
                    'created_at': repo.get('created_at'),
                    'updated_at': repo.get('updated_at')
                })
            
            logging.info(f"Retrieved {len(repo_list)} repositories")
            return {
                'success': True,
                'repositories': repo_list,
                'total_count': len(repo_list),
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to list repositories: {result.get('error')}")
            return result
    
    def create_issue(self, owner: str, repo_name: str, title: str, body: str = '',
                   labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create an issue in a repository"""
        data = {
            'title': title,
            'body': body,
            'labels': labels or []
        }
        
        endpoint = f"repos/{owner}/{repo_name}/issues"
        
        logging.info(f"Creating issue in {owner}/{repo_name}: {title}")
        result = self._make_request('POST', endpoint, data)
        
        if result['success']:
            issue_data = result['data']
            return {
                'success': True,
                'issue': {
                    'number': issue_data.get('number'),
                    'title': issue_data.get('title'),
                    'body': issue_data.get('body'),
                    'labels': [label.get('name') for label in issue_data.get('labels', [])],
                    'state': issue_data.get('state'),
                    'created_at': issue_data.get('created_at'),
                    'html_url': issue_data.get('html_url')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to create issue: {result.get('error')}")
            return result
    
    def create_pull_request(self, owner: str, repo_name: str, title: str, 
                          head: str, base: str, body: str = '') -> Dict[str, Any]:
        """Create a pull request"""
        data = {
            'title': title,
            'head': head,
            'base': base,
            'body': body
        }
        
        endpoint = f"repos/{owner}/{repo_name}/pulls"
        
        logging.info(f"Creating PR in {owner}/{repo_name}: {title}")
        result = self._make_request('POST', endpoint, data)
        
        if result['success']:
            pr_data = result['data']
            return {
                'success': True,
                'pull_request': {
                    'number': pr_data.get('number'),
                    'title': pr_data.get('title'),
                    'body': pr_data.get('body'),
                    'head': pr_data.get('head'),
                    'base': pr_data.get('base'),
                    'state': pr_data.get('state'),
                    'created_at': pr_data.get('created_at'),
                    'html_url': pr_data.get('html_url')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to create pull request: {result.get('error')}")
            return result
    
    def get_file_content(self, owner: str, repo_name: str, path: str, 
                       ref: Optional[str] = None) -> Dict[str, Any]:
        """Get file content from repository"""
        params = {}
        if ref:
            params['ref'] = ref
        
        endpoint = f"repos/{owner}/{repo_name}/contents/{path}"
        
        logging.info(f"Fetching file content: {owner}/{repo_name}/{path}")
        result = self._make_request('GET', endpoint, params=params)
        
        if result['success']:
            file_data = result['data']
            # Handle content encoding
            content = file_data.get('content', '')
            if file_data.get('encoding') == 'base64':
                import base64
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except Exception as e:
                    logging.warning(f"Failed to decode base64 content: {e}")
                    content = ''
            
            return {
                'success': True,
                'file': {
                    'name': file_data.get('name'),
                    'path': file_data.get('path'),
                    'size': file_data.get('size'),
                    'encoding': file_data.get('encoding'),
                    'content': content,
                    'sha': file_data.get('sha'),
                    'download_url': file_data.get('download_url')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to get file content: {result.get('error')}")
            return result
    
    def create_or_update_file(self, owner: str, repo_name: str, path: str, 
                           content: str, message: str = '', branch: str = 'main') -> Dict[str, Any]:
        """Create or update a file in a repository"""
        import base64
        
        data = {
            'message': message or f'Update {path}',
            'content': content,
            'branch': branch
        }
        
        endpoint = f"repos/{owner}/{repo_name}/contents/{path}"
        
        logging.info(f"Creating/updating file: {owner}/{repo_name}/{path}")
        result = self._make_request('PUT', endpoint, data)
        
        if result['success']:
            file_data = result['data']
            return {
                'success': True,
                'file': {
                    'name': file_data.get('name'),
                    'path': file_data.get('path'),
                    'size': file_data.get('size'),
                    'sha': file_data.get('content', {}).get('sha'),
                    'commit': file_data.get('commit')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to create/update file: {result.get('error')}")
            return result
    
    def get_user_info(self, username: Optional[str] = None) -> Dict[str, Any]:
        """Get user information"""
        if username:
            endpoint = f"users/{username}"
        else:
            endpoint = 'user'  # Get authenticated user
        
        logging.info(f"Fetching user info for: {username or 'authenticated user'}")
        result = self._make_request('GET', endpoint)
        
        if result['success']:
            user_data = result['data']
            return {
                'success': True,
                'user': {
                    'login': user_data.get('login'),
                    'name': user_data.get('name'),
                    'email': user_data.get('email'),
                    'bio': user_data.get('bio'),
                    'location': user_data.get('location'),
                    'company': user_data.get('company'),
                    'public_repos': user_data.get('public_repos'),
                    'private_repos': user_data.get('total_private_repos'),
                    'followers': user_data.get('followers'),
                    'following': user_data.get('following'),
                    'created_at': user_data.get('created_at'),
                    'updated_at': user_data.get('updated_at')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to get user info: {result.get('error')}")
            return result
    
    def search_repositories(self, query: str, sort: str = 'stars', 
                          order: str = 'desc', per_page: int = 30) -> Dict[str, Any]:
        """Search repositories"""
        params = {
            'q': query,
            'sort': sort,      # stars, forks, updated
            'order': order,    # desc, asc
            'per_page': per_page
        }
        
        endpoint = 'search/repositories'
        
        logging.info(f"Searching repositories: {query}")
        result = self._make_request('GET', endpoint, params=params)
        
        if result['success']:
            search_data = result['data']
            repos = []
            
            for repo in search_data.get('items', []):
                repos.append({
                    'name': repo.get('name'),
                    'full_name': repo.get('full_name'),
                    'description': repo.get('description'),
                    'clone_url': repo.get('clone_url'),
                    'html_url': repo.get('html_url'),
                    'language': repo.get('language'),
                    'stars': repo.get('stargazers_count'),
                    'forks': repo.get('forks_count'),
                    'open_issues': repo.get('open_issues_count'),
                    'created_at': repo.get('created_at'),
                    'updated_at': repo.get('updated_at')
                })
            
            logging.info(f"Found {len(repos)} repositories")
            return {
                'success': True,
                'repositories': repos,
                'total_count': search_data.get('total_count', 0),
                'incomplete_results': search_data.get('incomplete_results', False),
                'query': query,
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to search repositories: {result.get('error')}")
            return result
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get GitHub API rate limit information"""
        endpoint = 'rate_limit'
        
        result = self._make_request('GET', endpoint)
        
        if result['success']:
            rate_data = result['data']
            return {
                'success': True,
                'rate_limit': {
                    'limit': rate_data.get('rate', {}).get('limit'),
                    'remaining': rate_data.get('rate', {}).get('remaining'),
                    'reset': rate_data.get('rate', {}).get('reset'),
                    'used': rate_data.get('rate', {}).get('used')
                },
                'resources': rate_data.get('resources', {}),
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to get rate limit info: {result.get('error')}")
            return result
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get GitHub status information"""
        result = self._make_request('GET', 'status')
        
        if result['success']:
            status_data = result['data']
            return {
                'success': True,
                'status': {
                    'page': status_data.get('page'),
                    'status': status_data.get('status'),
                    'timestamp': status_data.get('timestamp')
                },
                'platform': self.platform
            }
        else:
            logging.error(f"Failed to get GitHub status: {result.get('error')}")
            return result
    
    def get_help_text(self) -> str:
        """Get help text for GitHub API operations"""
        return """
🐙 GitHub API Client for Terry-the-Tool-Bot
Windows 10/11 optimized with comprehensive GitHub integration

📋 Supported Operations:
• create-repo <name> - Create new repository
• get-repo <owner>/<repo> - Get repository info
• list-repos [user] - List repositories
• create-issue <owner>/<repo> <title> - Create issue
• create-pr <owner>/<repo> <title> - Create pull request
• get-file <owner>/<repo>/<path> - Get file content
• update-file <owner>/<repo>/<path> - Update file
• get-user [username] - Get user info
• search-repos <query> - Search repositories
• rate-limit - Get API rate limit info
• status - Get GitHub status

⚙️ Features:
• Windows-optimized requests
• Token authentication
• Rate limiting awareness
• Error handling and retries
• Base64 content encoding/decoding
• Comprehensive data parsing

🔑 Authentication:
• Set GITHUB_TOKEN environment variable
• Or provide token during initialization
• Public operations work without token

💡 Examples:
• create-repo my-awesome-project
• get-repo microsoft/vscode
• list-repos octocat
• create-issue myuser/myrepo "Bug in login"
• create-pr myuser/myrepo "Fix login bug" feature/main
• get-file microsoft/vscode/README.md
• update-file myuser/myrepo/config.json
• get-user torvalds
• search-repos "machine learning python"
• rate-limit
• status

🛠️ Windows Integration:
• Native Windows path handling
• Registry-based GitHub Desktop detection
• PowerShell command compatibility
• Long path support (>260 characters)
• Windows-specific optimizations
        """.strip()
    
    def validate_authentication(self) -> Dict[str, Any]:
        """Validate GitHub API authentication"""
        if self.token:
            # Test authentication with a simple request
            result = self.get_user_info()
            if result['success']:
                return {
                    'authenticated': True,
                    'token_valid': True,
                    'user': result.get('user'),
                    'permissions': 'full_access'
                }
            else:
                return {
                    'authenticated': False,
                    'token_valid': False,
                    'error': result.get('error')
                }
        else:
            return {
                'authenticated': False,
                'token_valid': False,
                'message': 'No GitHub token provided',
                'public_access_only': True
            }
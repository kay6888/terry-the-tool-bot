"""
Base Tool Module for Terry-the-Tool-Bot

Provides abstract base class for all tools in Terry's modular system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import time

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Abstract base class for all Terry tools"""
    
    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description
        self.active = True
        self.execution_count = 0
        self.success_count = 0
        self.last_used = None
        
        logger.info(f"Initialized tool: {name} v{version}")
        
    @abstractmethod
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool's main functionality
        
        Args:
            user_input: Raw user input string
            context: Conversation context with relevant information
            
        Returns:
            Dictionary containing execution results with standardized format:
            {
                'status': 'success' | 'error' | 'permission_denied',
                'message': str,
                'data': dict (optional),
                'execution_time': float (seconds),
                'tool_name': str,
                'version': str
            }
        """
        pass
    
    @abstractmethod
    def validate_input(self, user_input: str) -> bool:
        """
        Validate if input is suitable for this tool
        
        Args:
            user_input: Raw user input string
            
        Returns:
            True if input is valid for this tool
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get comprehensive tool information"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'active': self.active,
            'execution_count': self.execution_count,
            'success_count': self.success_count,
            'success_rate': self.success_count / max(self.execution_count, 1),
            'last_used': self.last_used
        }
    
    def activate(self) -> None:
        """Activate the tool"""
        self.active = True
        logger.info(f"Tool {self.name} activated")
        
    def deactivate(self) -> None:
        """Deactivate the tool"""
        self.active = False
        logger.info(f"Tool {self.name} deactivated")
        
    def _record_execution(self, success: bool) -> None:
        """Record tool execution statistics"""
        self.execution_count += 1
        if success:
            self.success_count += 1
        self.last_used = time.time()
        
    def _validate_permission(self, context: Dict[str, Any], required_permission: str) -> bool:
        """Check if required permission is available"""
        permissions = context.get('permissions', {})
        return permissions.get(required_permission, False)
        
    def _get_tool_function(self, function_name: str) -> Optional[callable]:
        """Get tool function by name (for dynamic calling)"""
        return getattr(self, function_name, None) if hasattr(self, function_name) else None
        
    def _format_response(self, status: str, message: str, data: Any = None, execution_time: float = 0) -> Dict[str, Any]:
        """Format standardized response"""
        self._record_execution(status == 'success')
        
        return {
            'status': status,
            'message': message,
            'data': data,
            'execution_time': execution_time,
            'tool_name': self.name,
            'version': self.version
        }
        
    def _get_capabilities(self) -> List[str]:
        """Get list of tool capabilities (to be overridden by subclasses)"""
        return [
            'execute',
            'validate_input',
            'get_info',
            'activate',
            'deactivate'
        ]
        
    def supports_function(self, function_name: str) -> bool:
        """Check if tool supports a specific function"""
        return function_name in self._get_capabilities()
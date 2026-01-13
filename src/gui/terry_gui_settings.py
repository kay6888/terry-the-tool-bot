"""
Terry GUI Settings - Comprehensive settings management system
Handles user preferences, themes, and configuration options
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

class TerryGUISettings:
    """Terry GUI settings manager"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.settings_file = self.config_dir / "gui_settings.json"
        self.default_settings = self._get_default_settings()
        self.settings = self._load_settings()
        
        # Initialize setting categories
        self.theme_settings = self.settings.get('theme', self.default_settings['theme'])
        self.display_settings = self.settings.get('display', self.default_settings['display'])
        self.communication_settings = self.settings.get('communication', self.default_settings['communication'])
        self.monetization_settings = self.settings.get('monetization', self.default_settings['monetization'])
        
        logging.info(f"GUI Settings initialized: {self.config_dir}")
    
    def _get_config_dir(self) -> Path:
        """Get configuration directory"""
        # Try different config locations based on platform
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / 'Terry-the-Tool-Bot'
        else:  # Unix-like systems
            config_dir = Path.home() / '.config' / 'terry-tool-bot'
        
        config_dir.mkdir(exist_ok=True)
        return config_dir
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings"""
        return {
            'theme': {
                'color_scheme': 'dark',
                'font_family': 'Segoe UI',
                'font_size': 10,
                'accent_color': '#0078d4',
                'background_color': '#1e1e1e',
                'text_color': '#ffffff',
                'use_system_theme': False,
                'custom_colors': {}
            },
            'display': {
                'window_size': '1400x900',
                'remember_position': True,
                'always_on_top': False,
                'show_minimize_button': True,
                'show_status_bar': True,
                'animations_enabled': True
            },
            'communication': {
                'email': 'kaynikko88@gmail.com',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'enable_notifications': True,
                'auto_save_conversations': True,
                'conversation_history_limit': 1000,
                'sound_enabled': True
            },
            'monetization': {
                'cashapp_enabled': False,
                'paypal_email': 'kaynikko88@gmail.com',
                'paypal_client_id': '',
                'donation_button_visible': True,
                'donation_amounts': [5, 10, 20, 50, 100],
                'default_donation': 10,
                'show_thank_you': True,
                'currency': 'USD'
            },
            'privacy': {
                'analytics_enabled': False,
                'crash_reports_enabled': True,
                'usage_statistics_enabled': True,
                'data_retention_days': 90,
                'encrypt_settings': True
            },
            'git_integration': {
                'default_branch': 'main',
                'auto_commit': False,
                'show_git_status': True,
                'enable_github_desktop': True,
                'preferred_editor': 'code'
            }
        }
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_settings(self.default_settings, settings)
            except Exception as e:
                logging.error(f"Failed to load settings: {e}")
                return self.default_settings.copy()
        else:
            return self.default_settings.copy()
    
    def _merge_settings(self, defaults: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded settings with defaults"""
        merged = defaults.copy()
        
        def deep_merge(default_dict, loaded_dict):
            for key, value in loaded_dict.items():
                if key in default_dict:
                    if isinstance(default_dict[key], dict) and isinstance(value, dict):
                        merged[key] = deep_merge(default_dict[key], value)
                    else:
                        merged[key] = value
                else:
                    merged[key] = value
            return merged
        
        return deep_merge(defaults, loaded)
    
    def save_settings(self) -> bool:
        """Save settings to file"""
        try:
            # Ensure directory exists
            self.settings_file.parent.mkdir(exist_ok=True)
            
            # Create backup
            if self.settings_file.exists():
                backup_file = self.settings_file.with_suffix('.backup')
                self.settings_file.rename(backup_file)
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            logging.info(f"Settings saved to: {self.settings_file}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")
            return False
    
    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Get a specific setting"""
        category_settings = self.settings.get(category, {})
        return category_settings.get(key, default)
    
    def set_setting(self, category: str, key: str, value: Any) -> bool:
        """Set a specific setting"""
        if category not in self.settings:
            self.settings[category] = {}
        
        self.settings[category][key] = value
        return self.save_settings()
    
    def reset_to_defaults(self, category: Optional[str] = None) -> bool:
        """Reset settings to defaults"""
        if category:
            self.settings[category] = self.default_settings[category].copy()
        else:
            self.settings = self.default_settings.copy()
        
        return self.save_settings()
    
    def get_theme_settings(self) -> Dict[str, Any]:
        """Get theme settings"""
        return self.theme_settings
    
    def set_theme_settings(self, settings: Dict[str, Any]) -> bool:
        """Update theme settings"""
        self.theme_settings.update(settings)
        return self.set_setting('theme', 'theme_settings')
    
    def get_display_settings(self) -> Dict[str, Any]:
        """Get display settings"""
        return self.display_settings
    
    def set_display_settings(self, settings: Dict[str, Any]) -> bool:
        """Update display settings"""
        self.display_settings.update(settings)
        return self.set_setting('display', 'display_settings')
    
    def get_communication_settings(self) -> Dict[str, Any]:
        """Get communication settings"""
        return self.communication_settings
    
    def set_communication_settings(self, settings: Dict[str, Any]) -> bool:
        """Update communication settings"""
        self.communication_settings.update(settings)
        return self.set_setting('communication', 'communication_settings')
    
    def get_monetization_settings(self) -> Dict[str, Any]:
        """Get monetization settings"""
        return self.monetization_settings
    
    def set_monetization_settings(self, settings: Dict[str, Any]) -> bool:
        """Update monetization settings"""
        self.monetization_settings.update(settings)
        return self.set_setting('monetization', 'monetization_settings')
    
    def export_settings(self) -> str:
        """Export settings to JSON string"""
        return json.dumps(self.settings, indent=2)
    
    def import_settings(self, settings_json: str) -> bool:
        """Import settings from JSON string"""
        try:
            imported_settings = json.loads(settings_json)
            self.settings = self._merge_settings(self.default_settings, imported_settings)
            return self.save_settings()
        except Exception as e:
            logging.error(f"Failed to import settings: {e}")
            return False
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of all settings for display"""
        return {
            'theme': self.theme_settings.get('color_scheme', 'default'),
            'email_configured': bool(self.get_communication_settings('email')),
            'donation_enabled': self.get_monetization_settings('donation_button_visible'),
            'analytics_enabled': self.settings.get('privacy', {}).get('analytics_enabled', False),
            'git_integration_enabled': len([k for k, v in self.settings.get('git_integration', {}).items() if v]) > 0
        }
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """Validate email address"""
        import re
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_pattern, email):
            return {'valid': True, 'message': 'Valid email address'}
        else:
            return {
                'valid': False, 
                'message': 'Please enter a valid email address'
            }
    
    def validate_color(self, color: str) -> Dict[str, Any]:
        """Validate color input"""
        import re
        
        # Support hex colors (#RRGGBB) and common color names
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        color_names = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black', 'white']
        
        if re.match(hex_pattern, color) or color.lower() in color_names:
            return {'valid': True, 'message': 'Valid color'}
        else:
            return {
                'valid': False, 
                'message': 'Please enter a valid color (hex or name)'
            }
    
    def get_window_geometry(self) -> str:
        """Get window geometry from settings"""
        return self.get_display_settings('window_size', '1400x900')
    
    def apply_theme_immediately(self, theme_name: str) -> bool:
        """Apply theme immediately without saving"""
        themes = {
            'dark': {
                'background_color': '#1e1e1e',
                'text_color': '#ffffff',
                'accent_color': '#0078d4',
                'border_color': '#444444'
            },
            'light': {
                'background_color': '#ffffff',
                'text_color': '#000000',
                'accent_color': '#0078d4',
                'border_color': '#cccccc'
            },
            'blue': {
                'background_color': '#1e3a8f',
                'text_color': '#ffffff',
                'accent_color': '#2196f3',
                'border_color': '#1976d2'
            },
            'green': {
                'background_color': '#1e1e1e',
                'text_color': '#ffffff',
                'accent_color': '#28a745',
                'border_color': '#1b5e20'
            }
        }
        
        if theme_name in themes:
            self.theme_settings.update(themes[theme_name])
            return True
        else:
            return False
    
    def log_usage_stats(self) -> None:
        """Log anonymous usage statistics"""
        try:
            stats_file = self.config_dir / "usage_stats.json"
            
            stats = {
                'last_opened': datetime.now().isoformat(),
                'opens_today': 1,
                'total_opens': self._increment_counter('total_opens'),
                'themes_used': self._increment_counter('themes_used'),
                'settings_changed': self._increment_counter('settings_changed')
            }
            
            # Load existing stats
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    existing_stats = json.load(f)
                    stats['total_opens'] = existing_stats.get('total_opens', 0) + 1
                    stats['themes_used'] = existing_stats.get('themes_used', 0) + 1
                    stats['settings_changed'] = existing_stats.get('settings_changed', 0) + 1
            
            # Save stats
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
                
        except Exception as e:
            logging.error(f"Failed to log usage stats: {e}")
    
    def _increment_counter(self, counter_name: str) -> int:
        """Increment counter in usage stats"""
        try:
            stats_file = self.config_dir / "usage_stats.json"
            
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
            else:
                stats = {}
            
            return stats.get(counter_name, 0) + 1
            
        except Exception:
            return 0
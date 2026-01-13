"""
Terry-the-Tool-Bot - Main Bot Module

The core Terry bot class extracted and refactored for modularity.
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from collections import deque
import queue
import sqlite3
import hashlib
import subprocess
import psutil
import platform
import json
from datetime import datetime, timedelta

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TerryToolBot:
    """Main Terry-the-Tool-Bot class - refactored for modularity"""
    
    def __init__(self):
        self.name = "Terry-the-Tool-Bot"
        self.version = "2.0.0"
        self.mode = "ANDROID_EXPERT_QUANTUM"
        
        # Root directory with user permission
        self.root_dir = Path.home() / ".terry_toolbot"
        self.root_dir.mkdir(exist_ok=True)
        
        # Permission system
        self.permissions = self.load_permissions()
        self.grant_permissions()
        
        # Initialize systems
        print("🎯 Initializing Terry-the-Tool-Bot v2.0 - Modular Architecture")
        
        self.setup_directories()
        self.setup_databases()
        self.load_knowledge()
        # Setup tools will be called later
        self.setup_web_access()
        self.setup_device_database()
        
        # Conversation system
        self.conversation_history = deque(maxlen=1000)
        self.thought_log = []
        self.learning_queue = queue.Queue()
        
        # Initialize new systems
        self.gui_settings = None
        self.contact_system = None
        self.payment_system = None
        
        # Initialize recovery builder
        self.recovery_builder = None
        try:
            from .tools.recovery_builder import RecoveryBuilder
            self.recovery_builder = RecoveryBuilder()
            print("✅ Recovery Builder initialized")
        except ImportError as e:
            logger.warning(f"Failed to initialize Recovery Builder: {e}")
            print("⚠️ Recovery Builder not available")
        
        # Store system instances
        self.terry_gui = None
        self.terry_contact = None
        self.terry_payment = None
    
    def setup_settings_system(self) -> None:
        """Setup GUI settings system"""
        if self.gui_settings:
            logging.info("GUI Settings system initialized")
        else:
            logging.warning("GUI Settings system not available")
    
    def setup_contact_system(self) -> None:
        """Setup contact system"""
        if self.contact_system:
            logging.info("Contact system initialized")
        else:
            logging.warning("Contact system not available")
    
    def setup_payment_system(self) -> None:
        """Setup payment system"""
        if self.payment_system:
            logging.info("Payment system initialized")
        else:
            logging.warning("Payment system not available")
    
    def get_settings_system(self) -> Any:
        """Get settings system instance"""
        return self.gui_settings
    
    def get_contact_system(self) -> Any:
        """Get contact system instance"""
        return self.contact_system
    
    def get_payment_system(self) -> Any:
        """Get payment system instance"""
        return self.payment_system
    
    def get_gui_settings(self) -> Dict[str, Any]:
        """Get GUI settings"""
        if self.gui_settings:
            return self.gui_settings.get_theme_settings()
        return {}
    
    def set_gui_settings(self, settings: Dict[str, Any]) -> bool:
        """Set GUI settings"""
        if self.gui_settings:
            self.gui_settings.set_theme_settings(settings)
            # Update display settings
            display_settings = self.gui_settings.get_display_settings()
            display_settings.update(settings)
            self.gui_settings.set_display_settings(display_settings)
            
            # Update communication settings
            comm_settings = self.gui_settings.get_communication_settings()
            comm_settings.update(settings)
            self.gui_settings.set_communication_settings(comm_settings)
            
            # Save settings
            return self.gui_settings.save_settings()
        return False
    
    def get_contact_info(self) -> Dict[str, Any]:
        """Get contact information"""
        if self.contact_system:
            return {
                'email': self.contact_system.get_communication_settings('email'),
                'paypal_configured': self.contact_system.payments_file.exists(),
                'ticket_count': len(self.contact_system.get_open_tickets()),
                'contact_requests_today': 0
            }
        return {
            'email': 'kaynikko88@gmail.com',
            'paypal_configured': False,
            'ticket_count': 0,
            'contact_requests_today': 0
        }
    
    def get_payment_info(self) -> Dict[str, Any]:
        """Get payment information"""
        if self.payment_system:
            return self.payment_system.get_payment_summary()
        return {
            'paypal_configured': False,
            'cashapp_configured': False,
            'total_donated': 0,
            'monthly_revenue': 0
        }
    
    def get_recovery_builder_info(self) -> Dict[str, Any]:
        """Get recovery builder information"""
        if self.recovery_builder:
            return {
                'available': True,
                'supported_devices': len(self.recovery_builder.get_supported_devices()),
                'build_history_count': len(self.recovery_builder.get_build_history()),
                'current_builds': len(self.recovery_builder.get_current_builds()),
                'artifacts_directory': str(self.recovery_builder.get_artifacts_directory())
            }
        return {
            'available': False,
            'supported_devices': 0,
            'build_history_count': 0,
            'current_builds': 0,
            'artifacts_directory': ''
        }
    
    def build_recovery(self, device_codename: str, recovery_type: str = "twrp", **kwargs) -> Dict[str, Any]:
        """Build recovery for given device"""
        if not self.recovery_builder:
            return {
                'success': False,
                'error': 'Recovery Builder not available'
            }
        
        try:
            from .tools.recovery_builder import BuildConfig, RecoveryType, DeviceInfo
            
            # Check in both default and custom devices
            all_devices = {**self.recovery_builder.device_database, **self.recovery_builder.custom_devices}
            if device_codename not in all_devices:
                return {
                    'success': False,
                    'error': f'Device {device_codename} not supported. Use "list supported devices" to see available devices.'
                }
            
            device_info = all_devices[device_codename]
            
            # Create build config
            build_config = BuildConfig(
                device_info=device_info,
                recovery_type=RecoveryType(recovery_type.lower()),
                **kwargs
            )
            
            # Build recovery
            artifact = self.recovery_builder.build_recovery(build_config)
            
            return {
                'success': artifact.status.value == 'success',
                'artifact': {
                    'device_codename': artifact.device_codename,
                    'recovery_type': artifact.recovery_type.value,
                    'status': artifact.status.value,
                    'file_path': str(artifact.file_path),
                    'file_size': artifact.file_size,
                    'sha256_hash': artifact.sha256_hash,
                    'build_time': artifact.build_time.isoformat()
                },
                'build_log_path': str(artifact.build_log_path)
            }
            
        except Exception as e:
            logger.error(f"Recovery build failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_supported_devices(self) -> List[str]:
        """Get list of supported recovery build devices"""
        if self.recovery_builder:
            return self.recovery_builder.get_supported_devices()
        return []
    
    def add_custom_device_tree(self, device_codename: str, brand: str, model: str, arch: str, 
                             platform: str, android_version: str, tree_url: str, 
                             kernel_url: str = None) -> Dict[str, Any]:
        """Add a custom device tree for recovery building"""
        if not self.recovery_builder:
            return {
                'success': False,
                'error': 'Recovery Builder not available'
            }
        
        try:
            from .tools.recovery_builder import DeviceInfo
            
            # Create device info
            device_info = DeviceInfo(
                codename=device_codename,
                brand=brand,
                model=model,
                arch=arch,
                platform=platform,
                android_version=android_version
            )
            
            # Add custom device tree
            success = self.recovery_builder.add_custom_device_tree(
                device_info, tree_url, kernel_url
            )
            
            if success:
                return {
                    'success': True,
                    'message': f'Custom device {device_codename} ({brand} {model}) added successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to add custom device tree for {device_codename}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error adding custom device tree: {str(e)}'
            }
    
    def setup_roomservice_xml(self, device_codename: str, recovery_type: str = "twrp") -> Dict[str, Any]:
        """Setup roomservice.xml for device recovery building"""
        if not self.recovery_builder:
            return {
                'success': False,
                'error': 'Recovery Builder not available'
            }
        
        try:
            from .tools.recovery_builder import RecoveryType
            
            recovery_type_enum = RecoveryType(recovery_type.lower())
            success = self.recovery_builder.setup_roomservice_xml(device_codename, recovery_type_enum)
            
            roomservice_file = self.recovery_builder.get_roomservice_file(device_codename)
            
            if success and roomservice_file:
                return {
                    'success': True,
                    'message': f'Roomservice XML created for {device_codename}',
                    'file_path': str(roomservice_file)
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to setup roomservice XML for {device_codename}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error setting up roomservice XML: {str(e)}'
            }
    
    def setup_recovery_build_environment(self) -> Dict[str, Any]:
        """Setup recovery build environment"""
        if not self.recovery_builder:
            return {
                'success': False,
                'error': 'Recovery Builder not available'
            }
        
        try:
            success = self.recovery_builder.setup_build_environment()
            return {
                'success': success,
                'message': 'Build environment setup complete' if success else 'Build environment setup failed'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        print("✅ Modular initialization complete!")
        
    def load_permissions(self) -> Dict[str, bool]:
        """Load or create permission settings"""
        perm_file = self.root_dir / "permissions.json"
        if perm_file.exists():
            import json
            with open(perm_file, 'r') as f:
                return json.load(f)
        
        default_perms = {
            "full_system": True,
            "web_access": True,
            "file_access": True,
            "network_access": True,
            "adb_access": True,
            "sudo_access": False,
            "learning_enabled": True,
            "auto_update": True
        }
        
        with open(perm_file, 'w') as f:
            import json
            json.dump(default_perms, f, indent=2)
        
        return default_perms
    
    def grant_permissions(self) -> None:
        """Grant system permissions"""
        print("\n🔐 PERMISSION SYSTEM:")
        print("-" * 50)
        
        for perm, granted in self.permissions.items():
            status = "✅ GRANTED" if granted else "❌ DENIED"
            print(f"{status} {perm.replace('_', ' ').title()}")
        
        print("-" * 50)
    
    def setup_directories(self) -> None:
        """Create organized directory structure"""
        dirs = [
            "projects/android",
            "projects/python", 
            "projects/web",
            "knowledge/code_patterns",
            "data/logs/conversations",
            "data/logs/errors",
            "data/logs/system"
        ]
        
        for dir_path in dirs:
            (self.root_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    def setup_databases(self) -> None:
        """Setup comprehensive databases"""
        self.db_path = self.root_dir / "knowledge.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_input TEXT,
                bot_response TEXT,
                intent TEXT,
                success_score REAL,
                learned_pattern TEXT,
                improvement_suggestions TEXT
            )
        ''')
        
        self.conn.commit()
    
    def load_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive knowledge base"""
        return {
            "android_development": {
                "project_structures": ["MVVM", "MVI", "MVP"],
                "common_patterns": ["Repository", "ViewBinding", "Coroutines"],
                "best_practices": ["Material Design", "Dependency Injection"]
            },
            "qcse_enabled": True
        }
    
    def _show_settings_display(self) -> str:
        """Show current settings display"""
        if self.gui_settings:
            return self.gui_settings.get_settings_summary()
        return "Settings system not available"
    
    def setup_web_access(self) -> None:
        """Setup web access capabilities"""
        pass  # Will be implemented with web scraper tool
    
    def setup_device_database(self) -> Dict[str, Any]:
        """Setup device database"""
        return {
            "devices": {
                "beryllium": {"brand": "Xiaomi", "model": "Poco F1"},
                "begonia": {"brand": "Xiaomi", "model": "Redmi Note 8 Pro"}
            }
        }
    
    def get_knowledge_stats(self) -> str:
        """Get knowledge base statistics"""
        knowledge = self.load_knowledge()
        android_count = len(knowledge["android_development"]["common_patterns"])
        qcse_status = "ENABLED" if knowledge.get("qcse_enabled", False) else "DISABLED"
        
        return f"{android_count} Android patterns, QCSE: {qcse_status}"
    
    def run(self):
        """Main conversation loop"""
        print(f"\n🤖 {self.name} is ready! Type 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"\n👋 Goodbye! {self.name} is shutting down...\n")
                    break
                
                if not user_input:
                    continue
                
                # Simple processing for now - will be enhanced with tools
                response = self.process_input(user_input)
                print(f"\n🤖 Terry: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye! {self.name} is shutting down...\n")
                break
            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                print(f"❌ Error: {str(e)}")
        
        # Cleanup
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Simple rule-based processing for now
        user_input_lower = user_input.lower()
        
        # Recovery building queries
        if any(keyword in user_input_lower for keyword in ['recovery', 'twrp', 'orange fox', 'build recovery', 'custom device', 'roomservice']):
            return self.process_recovery_queries(user_input)
        
        # Android development queries
        elif any(keyword in user_input_lower for keyword in ['android', 'app', 'kotlin', 'java', 'studio']):
            return "I can help you with Android development! I can create complete projects, debug issues, and optimize performance. Use the Android Builder tool for comprehensive project creation."
        
        # Tool-related queries
        elif any(keyword in user_input_lower for keyword in ['tool', 'feature', 'qcse', 'quantum']):
            return "I have modular tools available including Android Builder, Recovery Expert, and the revolutionary Quantum Code Synthesis Engine. These are being integrated into the new architecture."
        
        # Help queries
        elif any(keyword in user_input_lower for keyword in ['help', 'what can you do', 'capabilities']):
            return self.get_capabilities_help()
        
        # Default response
        return "I'm Terry-the-Tool-Bot, your advanced AI coding assistant! I can help with Android development, recovery building, code synthesis, and much more. What would you like to work on?"
    
    def process_recovery_queries(self, user_input: str) -> str:
        """Process recovery building specific queries"""
        user_input_lower = user_input.lower()
        
        # Setup build environment
        if any(keyword in user_input_lower for keyword in ['setup', 'environment', 'prepare']):
            result = self.setup_recovery_build_environment()
            if result['success']:
                return f"✅ {result['message']}! I'm ready to build recoveries now."
            else:
                return f"❌ Setup failed: {result['error']}"
        
        # List supported devices
        elif any(keyword in user_input_lower for keyword in ['devices', 'supported', 'list']):
            devices = self.get_supported_devices()
            if devices:
                device_list = "\\n".join([f"• {device}" for device in devices[:10]])
                return f"📱 Supported devices ({len(devices)} total):\\n{device_list}\\n... and {len(devices) - 10} more devices!"
            else:
                return "❌ No devices available. Recovery Builder might not be initialized."
        
        # Add custom device tree
        elif 'add custom device' in user_input_lower or 'add device tree' in user_input_lower:
            return """🌳 Add Custom Device Tree:\\n\\nFormat: 'add custom device <codename> <brand> <model> <arch> <platform> <android_version> <tree_url> [kernel_url]'\\n\\nExample: 'add custom device lavender Xiaomi Redmi Note 7 arm64 sdm660 9 https://github.com/device/xiaomi_lavender https://github.com/kernel/xiaomi_lavender'\\n\\nRequired info:\\n• codename: Device codename (e.g., lavender)\\n• brand: Manufacturer (e.g., Xiaomi)\\n• model: Device model (e.g., Redmi Note 7)\\n• arch: Architecture (arm64, arm, etc.)\\n• platform: SoC platform (sdm660, mt6768, etc.)\\n• android_version: Android version (9, 10, 11, etc.)\\n• tree_url: Device tree repository URL\\n• kernel_url: (optional) Kernel repository URL"""
        
        # Setup roomservice.xml
        elif any(keyword in user_input_lower for keyword in ['roomservice', 'setup roomservice']):
            # Extract device name
            words = user_input_lower.split()
            device_name = None
            recovery_type = 'twrp'
            
            # Find device name
            for i, word in enumerate(words):
                if word in ['roomservice', 'setup'] and i + 1 < len(words):
                    potential_device = words[i + 1]
                    if potential_device not in ['xml', 'for']:
                        device_name = potential_device
                        break
            
            # Find recovery type
            if 'orange' in user_input_lower and 'fox' in user_input_lower:
                recovery_type = 'orange_fox'
            
            if device_name:
                result = self.setup_roomservice_xml(device_name, recovery_type)
                if result['success']:
                    return f"✅ {result['message']}\\n📁 File: {result['file_path']}"
                else:
                    return f"❌ Roomservice setup failed: {result['error']}"
            else:
                return "Please specify a device name. Example: 'setup roomservice beryllium' or 'setup roomservice orange fox beryllium'"
        
        # Build recovery for specific device
        elif 'build' in user_input_lower and 'twrp' in user_input_lower:
            # Extract device name from input
            words = user_input_lower.split()
            device_name = None
            for i, word in enumerate(words):
                if word == 'twrp' and i + 1 < len(words):
                    device_name = words[i + 1]
                    break
            
            if device_name:
                result = self.build_recovery(device_name, 'twrp')
                if result['success']:
                    artifact = result['artifact']
                    return f"✅ TWRP build successful for {device_name}!\\n📁 File: {artifact['file_path']}\\n📏 Size: {artifact['file_size']:,} bytes\\n🔐 SHA256: {artifact['sha256_hash'][:16]}..."
                else:
                    return f"❌ TWRP build failed: {result['error']}"
            else:
                return "Please specify a device name. Example: 'build twrp beryllium'"
        
        elif 'build' in user_input_lower and 'orange fox' in user_input_lower:
            # Extract device name from input
            words = user_input_lower.split()
            device_name = None
            for i, word in enumerate(words):
                if word == 'fox' and i + 1 < len(words):
                    device_name = words[i + 1]
                    break
            
            if device_name:
                result = self.build_recovery(device_name, 'orange_fox')
                if result['success']:
                    artifact = result['artifact']
                    return f"✅ Orange Fox build successful for {device_name}!\\n📁 File: {artifact['file_path']}\\n📏 Size: {artifact['file_size']:,} bytes\\n🔐 SHA256: {artifact['sha256_hash'][:16]}..."
                else:
                    return f"❌ Orange Fox build failed: {result['error']}"
            else:
                return "Please specify a device name. Example: 'build orange fox beryllium'"
        
        # Recovery status/info
        elif any(keyword in user_input_lower for keyword in ['status', 'info', 'current']):
            info = self.get_recovery_builder_info()
            if info['available']:
                return f"🔧 Recovery Builder Status:\\n📱 Supported devices: {info['supported_devices']}\\n📊 Build history: {info['build_history_count']}\\n🔄 Current builds: {info['current_builds']}\\n📁 Artifacts: {info['artifacts_directory']}"
            else:
                return "❌ Recovery Builder is not available or initialized."
        
        # Default recovery help
        return """🔧 Recovery Building Commands:\\n• 'setup recovery environment' - Setup build tools\\n• 'list supported devices' - Show available devices\\n• 'add custom device' - Show custom device format\\n• 'setup roomservice [device]' - Generate roomservice.xml\\n• 'build twrp [device]' - Build TWRP recovery\\n• 'build orange fox [device]' - Build Orange Fox recovery\\n• 'recovery status' - Show current status\\n\\n🌳 Custom Device Example: 'add custom device lavender Xiaomi Redmi Note 7 arm64 sdm660 9 https://github.com/device/xiaomi_lavender https://github.com/kernel/xiaomi_lavender'"""
    
    def get_capabilities_help(self) -> str:
        """Get comprehensive help about Terry's capabilities"""
        return """I'm Terry-the-Tool-Bot v2.0 with these capabilities:

📱 Android Development
• MVVM, Material Design, modern patterns
• Complete project creation
• Debugging and optimization

🔧 Recovery Building (NEW!)
• TWRP recovery building
• Orange Fox recovery building  
• 15+ supported devices
• Automated build environment

📱 IMEI Problem Solving
• Baseband repair
• EFS backup/restore
• Advanced repair methods

🌐 Web Access & Research
• Intelligent web scraping
• Data interpretation and analysis

⚛️ Quantum Code Synthesis
• Multi-objective optimization
• Advanced code generation

💻 File Management
• Secure operations
• File validation and organization

📝 Article Writing
• Technical documentation
• Tutorial creation

🧠 Continuous Learning
• Pattern recognition
• Adaptive responses

🎨 Modern GUI
• Intuitive interface
• Real-time updates

Try: 'setup recovery environment' to start building recoveries!
Use 'terry --gui' for the graphical interface!"""

# Compatibility with existing imports
try:
    import requests
    import yaml
    import json
    import re
    import html
    import urllib.parse
    import urllib.request
    import random
    
    # Optional imports
    try:
        import pyperclip
        CLIPBOARD_AVAILABLE = True
    except ImportError:
        CLIPBOARD_AVAILABLE = False
    
    try:
        import pyautogui
        SCREENSHOT_AVAILABLE = True
    except ImportError:
        SCREENSHOT_AVAILABLE = False
        
except ImportError as e:
    logger.warning(f"Optional import failed: {e}")
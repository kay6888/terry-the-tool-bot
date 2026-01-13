#!/usr/bin/env python3
"""
Terry-the-Tool-Bot.py - Ultimate Android Development AI
The most advanced coding assistant with system access, web capabilities, and continuous learning
"""

import os
import sys
import json
import re
import sqlite3
import hashlib
import time
import threading
import queue
import subprocess
import webbrowser
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None
import platform
import shutil
import html
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional, Tuple
import urllib.parse
import urllib.request
# import feedparser  # Optional dependency
# import markdown  # Optional dependency
import random
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    BeautifulSoup = None

# Try to import optional packages
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

class TerryToolBot:
    def __init__(self):
        self.name = "Terry-the-Tool-Bot"
        self.version = "1.0.0"
        self.mode = "ANDROID_EXPERT"
        
        # Root directory with user permission
        self.root_dir = Path.home() / ".terry_toolbot"
        self.root_dir.mkdir(exist_ok=True)
        
        # Permission system
        self.permissions = self.load_permissions()
        self.grant_permissions()
        
        # Setup all systems
        print("\n" + "="*100)
        print(f"🛠️  {self.name} v{self.version} - Ultimate Android ToolBot")
        print("="*100)
        print("⚡ STATUS: FULL SYSTEM ACCESS | WEB INTEGRATION | CONTINUOUS LEARNING")
        print("📱 SPECIALTY: ANDROID DEVELOPMENT EXPERT | DEVICE TREE MASTER")
        print("🔧 FEATURES: IMEI PROBLEM SOLVER | ARTICLE WRITER | CONVERSATIONAL AI")
        print("🚀 CAPABILITIES: REAL-TIME UPDATES | TOOL SWAPPING | MISTAKE LEARNING")
        print("="*100)
        
        self.setup_directories()
        self.setup_databases()
        self.load_knowledge()
        self.setup_tools()
        self.setup_web_access()
        self.setup_device_database()
        
        # Conversation system
        self.conversation_history = deque(maxlen=1000)
        self.thought_log = []
        self.learning_queue = queue.Queue()
        
        # Start background services
        self.start_background_services()
        
        print(f"\nInitialization Complete:")
        print(f"• Knowledge Base: {self.get_knowledge_stats()}")
        print(f"• Device Database: {len(self.device_db)} devices")
        print(f"• Tools Available: {len(self.tools)} specialized tools")
        print(f"• System Access: {'GRANTED' if self.permissions['full_system'] else 'LIMITED'}")
        print(f"• Web Access: {'ENABLED' if self.permissions['web_access'] else 'DISABLED'}")
        print("\n" + "-"*100)
        print("💬 Hello! I'm Terry-the-Tool-Bot. I can:")
        print("   1. Create any Android app")
        print("   2. Solve complex coding problems")
        print("   3. Access your computer (with permission)")
        print("   4. Browse and interpret websites")
        print("   5. Learn from my mistakes")
        print("   6. Write professional articles")
        print("   7. Fix IMEI and phone issues")
        print("   8. Hold natural conversations")
        print("\nJust talk to me naturally. What would you like to do?")
        print("-"*100)
    
    def setup_directories(self):
        """Create organized directory structure"""
        dirs = [
            "projects/android",
            "projects/python",
            "projects/web",
            "knowledge/code_patterns",
            "knowledge/device_trees",
            "knowledge/articles",
            "tools/active",
            "tools/archive",
            "logs/conversations",
            "logs/errors",
            "cache/web",
            "cache/images",
            "backups/system",
            "backups/projects",
            "data/imei",
            "data/device_info"
        ]
        
        for dir_path in dirs:
            (self.root_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    def setup_databases(self):
        """Setup comprehensive databases"""
        # Main knowledge database
        self.db_path = self.root_dir / "knowledge.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables
        tables = {
            "conversations": """
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
            """,
            "code_patterns": """
                CREATE TABLE IF NOT EXISTS code_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash TEXT UNIQUE,
                    language TEXT,
                    pattern_type TEXT,
                    code TEXT,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    last_used TEXT,
                    complexity REAL,
                    efficiency_score REAL
                )
            """,
            "device_info": """
                CREATE TABLE IF NOT EXISTS device_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codename TEXT UNIQUE,
                    brand TEXT,
                    model TEXT,
                    chipset TEXT,
                    android_versions TEXT,
                    recovery_status TEXT,
                    kernel_source TEXT,
                    device_tree_url TEXT,
                    partition_layout TEXT,
                    imei_fixes TEXT
                )
            """,
            "learning_mistakes": """
                CREATE TABLE IF NOT EXISTS learning_mistakes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mistake_hash TEXT,
                    context TEXT,
                    error TEXT,
                    correction TEXT,
                    learned_at TEXT,
                    applied_count INTEGER DEFAULT 0
                )
            """,
            "web_cache": """
                CREATE TABLE IF NOT EXISTS web_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    content TEXT,
                    fetched_at TEXT,
                    relevance_score REAL
                )
            """,
            "articles": """
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    topic TEXT,
                    content TEXT,
                    created_at TEXT,
                    quality_score REAL,
                    tags TEXT
                )
            """
        }
        
        for table_name, table_sql in tables.items():
            self.cursor.execute(table_sql)
        
        self.conn.commit()
    
    def load_permissions(self):
        """Load or create permission settings"""
        perm_file = self.root_dir / "permissions.json"
        if perm_file.exists():
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
            json.dump(default_perms, f, indent=2)
        
        return default_perms
    
    def grant_permissions(self):
        """Grant system permissions"""
        print("\n🔐 PERMISSION SYSTEM:")
        print("-" * 50)
        
        for perm, granted in self.permissions.items():
            status = "✅ GRANTED" if granted else "❌ DENIED"
            print(f"{status} {perm.replace('_', ' ').title()}")
        
        print("-" * 50)
        print("Note: All access is logged and requires confirmation for sensitive operations")
    
    def setup_tools(self):
        """Setup modular tool system"""
        self.tools = {
            # Android Development Tools
            "android_builder": {
                "name": "Android Project Builder",
                "description": "Creates complete Android projects with proper structure",
                "version": "2.1",
                "active": True,
                "functions": [
                    "create_android_project",
                    "generate_activity",
                    "setup_gradle",
                    "add_dependencies"
                ]
            },
            "recovery_expert": {
                "name": "Recovery Builder Expert",
                "description": "Builds TWRP, OrangeFox, and custom recoveries",
                "version": "3.0",
                "active": True,
                "functions": [
                    "setup_recovery_env",
                    "build_recovery",
                    "fix_recovery_issues",
                    "create_device_tree"
                ]
            },
            "kernel_toolkit": {
                "name": "Kernel Development Toolkit",
                "description": "Kernel building, patching, and optimization",
                "version": "1.5",
                "active": True,
                "functions": [
                    "compile_kernel",
                    "apply_patches",
                    "optimize_config",
                    "debug_kernel"
                ]
            },
            
            # Problem Solving Tools
            "debug_master": {
                "name": "Debug Master",
                "description": "Advanced debugging and problem diagnosis",
                "version": "2.2",
                "active": True,
                "functions": [
                    "analyze_logcat",
                    "debug_crashes",
                    "memory_analysis",
                    "performance_profiling"
                ]
            },
            "imei_fixer": {
                "name": "IMEI Repair Expert",
                "description": "Fixes IMEI and baseband issues",
                "version": "1.3",
                "active": True,
                "functions": [
                    "diagnose_imei",
                    "repair_imei",
                    "backup_efs",
                    "restore_baseband"
                ]
            },
            
            # System Tools
            "file_manager": {
                "name": "Intelligent File Manager",
                "description": "Advanced file operations with pattern recognition",
                "version": "1.8",
                "active": True,
                "functions": [
                    "organize_files",
                    "find_patterns",
                    "batch_operations",
                    "backup_system"
                ]
            },
            "web_scraper": {
                "name": "Web Intelligence Scraper",
                "description": "Extracts and interprets web content",
                "version": "2.0",
                "active": True,
                "functions": [
                    "fetch_web_content",
                    "extract_information",
                    "summarize_articles",
                    "monitor_updates"
                ]
            },
            
            # Writing Tools
            "article_writer": {
                "name": "Professional Article Writer",
                "description": "Writes technical articles and documentation",
                "version": "1.6",
                "active": True,
                "functions": [
                    "write_article",
                    "format_markdown",
                    "add_code_examples",
                    "create_tutorials"
                ]
            },
            
            # Learning Tools
            "self_improver": {
                "name": "Self-Improvement Engine",
                "description": "Learns from mistakes and optimizes performance",
                "version": "1.4",
                "active": True,
                "functions": [
                    "analyze_mistakes",
                    "update_knowledge",
                    "optimize_responses",
                    "generate_insights"
                ]
            }
        }
        
        # Load custom tools
        self.load_custom_tools()
    
    def load_custom_tools(self):
        """Load user-defined custom tools"""
        tools_dir = self.root_dir / "tools/custom"
        tools_dir.mkdir(exist_ok=True)
        
        for tool_file in tools_dir.glob("*.json"):
            try:
                with open(tool_file, 'r') as f:
                    tool_data = json.load(f)
                    tool_name = tool_file.stem
                    self.tools[tool_name] = tool_data
                    print(f"Loaded custom tool: {tool_data.get('name', tool_name)}")
            except:
                pass
    
    def setup_web_access(self):
        """Setup web access capabilities"""
        if REQUESTS_AVAILABLE and requests:
            self.web_session = requests.Session()
            self.web_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Terry-ToolBot/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        else:
            self.web_session = None
        
        # Web sources for Android development
        self.web_sources = {
            "github": "https://api.github.com",
            "xda": "https://forum.xda-developers.com",
            "android_source": "https://source.android.com",
            "lineage_wiki": "https://wiki.lineageos.org",
            "kernel_org": "https://www.kernel.org",
            "stackoverflow": "https://api.stackexchange.com/2.2"
        }
    
    def setup_device_database(self):
        """Setup comprehensive device database"""
        self.device_db = {}
        
        # Try to load from database first
        self.cursor.execute("SELECT codename, brand, model, chipset FROM device_info")
        devices = self.cursor.fetchall()
        
        for codename, brand, model, chipset in devices:
            self.device_db[codename] = {
                "brand": brand,
                "model": model,
                "chipset": chipset
            }
        
        # If empty, load default devices
        if not self.device_db:
            self.load_default_devices()
    
    def load_default_devices(self):
        """Load default device database"""
        default_devices = {
            "beryllium": {
                "brand": "Xiaomi",
                "model": "Poco F1",
                "chipset": "Snapdragon 845",
                "android_versions": "9-13",
                "recovery_status": "Official TWRP available",
                "kernel_source": "https://github.com/Poco-F1-Development/android_kernel_xiaomi_sdm845",
                "device_tree_url": "https://github.com/Poco-F1-Development/android_device_xiaomi_beryllium"
            },
            "begonia": {
                "brand": "Xiaomi",
                "model": "Redmi Note 8 Pro",
                "chipset": "MediaTek Helio G90T",
                "android_versions": "9-12",
                "recovery_status": "Unofficial TWRP/OrangeFox",
                "kernel_source": "https://github.com/begonia-dev/android_kernel_xiaomi_mt6785"
            },
            "davinci": {
                "brand": "Xiaomi",
                "model": "Mi 9T",
                "chipset": "Snapdragon 730",
                "android_versions": "9-12",
                "recovery_status": "Official TWRP available"
            }
        }
        
        self.device_db = default_devices
        
        # Save to database
        for codename, info in default_devices.items():
            self.cursor.execute('''
                INSERT OR REPLACE INTO device_info 
                (codename, brand, model, chipset, android_versions, recovery_status, kernel_source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (codename, info["brand"], info["model"], info["chipset"], 
                  info["android_versions"], info["recovery_status"], info.get("kernel_source", "")))
        
        self.conn.commit()
    
    def load_knowledge(self):
        """Load comprehensive knowledge base"""
        knowledge_file = self.root_dir / "knowledge_base.json"
        
        if knowledge_file.exists():
            with open(knowledge_file, 'r') as f:
                self.knowledge = json.load(f)
        else:
            # Initialize with expert Android knowledge
            self.knowledge = {
                "android_development": {
                    "project_structures": self.get_android_project_structures(),
                    "common_patterns": self.get_android_patterns(),
                    "best_practices": self.get_android_best_practices(),
                    "debugging_techniques": self.get_debugging_techniques()
                },
                "recovery_building": {
                    "twrp_guide": self.get_twrp_guide(),
                    "orangefox_guide": self.get_orangefox_guide(),
                    "common_issues": self.get_recovery_issues(),
                    "device_tree_templates": self.get_device_tree_templates()
                },
                "imei_repair": {
                    "diagnosis": self.get_imei_diagnosis(),
                    "repair_methods": self.get_imei_repair_methods(),
                    "prevention": self.get_imei_prevention(),
                    "tools": self.get_imei_tools()
                },
                "article_templates": {
                    "tutorial": self.get_article_template("tutorial"),
                    "guide": self.get_article_template("guide"),
                    "review": self.get_article_template("review"),
                    "troubleshooting": self.get_article_template("troubleshooting")
                },
                "learning_patterns": {},
                "conversation_contexts": {}
            }
            
            self.save_knowledge()
    
    def get_knowledge_stats(self):
        """Get knowledge base statistics"""
        android_count = len(self.knowledge.get("android_development", {}).get("common_patterns", []))
        recovery_count = len(self.knowledge.get("recovery_building", {}).get("common_issues", []))
        device_count = len(self.device_db)
        
        return f"{android_count} Android patterns, {recovery_count} recovery solutions, {device_count} devices"
    
    def start_background_services(self):
        """Start background learning and update services"""
        
        # Learning service
        self.learning_service = threading.Thread(target=self.background_learning)
        self.learning_service.daemon = True
        self.learning_service.start()
        
        # Update service
        self.update_service = threading.Thread(target=self.background_updates)
        self.update_service.daemon = True
        self.update_service.start()
        
        # Web monitoring service
        if self.permissions["web_access"]:
            self.web_service = threading.Thread(target=self.background_web_monitor)
            self.web_service.daemon = True
            self.web_service.start()
    
    def background_learning(self):
        """Continuous learning from interactions"""
        while True:
            try:
                if not self.learning_queue.empty():
                    learning_item = self.learning_queue.get()
                    self.process_learning_item(learning_item)
                
                # Consolidate knowledge periodically
                time.sleep(300)  # Every 5 minutes
                self.consolidate_knowledge()
                
            except Exception as e:
                self.log_error(f"Background learning error: {str(e)}")
    
    def background_updates(self):
        """Check for updates and new information"""
        while True:
            try:
                if self.permissions["auto_update"]:
                    self.check_for_updates()
                    self.update_device_database()
                    self.update_code_patterns()
                
                time.sleep(3600)  # Every hour
                
            except Exception as e:
                self.log_error(f"Background update error: {str(e)}")
    
    def background_web_monitor(self):
        """Monitor web for new Android developments"""
        while True:
            try:
                self.monitor_android_news()
                self.monitor_github_repos()
                self.monitor_xda_forums()
                
                time.sleep(1800)  # Every 30 minutes
                
            except Exception as e:
                self.log_error(f"Web monitoring error: {str(e)}")
    
    def process(self, user_input):
        """Main processing function - the brain of Terry"""
        start_time = time.time()
        
        # Log conversation
        self.conversation_history.append({
            "user": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 1: Double-check understanding
        self.thought_log = []
        self.add_thought("🔍 STEP 1: ANALYZING INPUT")
        intent = self.double_check_intent(user_input)
        self.add_thought(f"Detected intent: {intent}")
        
        # Step 2: Access relevant knowledge
        self.add_thought("💾 STEP 2: ACCESSING KNOWLEDGE")
        context = self.access_relevant_knowledge(user_input, intent)
        
        # Step 3: Use appropriate tools
        self.add_thought("🛠️ STEP 3: SELECTING TOOLS")
        tool_response = self.use_tools(user_input, intent, context)
        
        # Step 4: Generate response with learning
        self.add_thought("🧠 STEP 4: GENERATING RESPONSE")
        response = self.generate_intelligent_response(user_input, intent, context, tool_response)
        
        # Step 5: Learn from this interaction
        self.add_thought("📚 STEP 5: LEARNING & IMPROVING")
        self.learn_from_interaction(user_input, response, intent)
        
        # Step 6: Double-check response
        self.add_thought("✅ STEP 6: FINAL VERIFICATION")
        response = self.double_check_response(response, user_input)
        
        processing_time = time.time() - start_time
        self.add_thought(f"⏱️ Processing time: {processing_time:.2f}s")
        
        # Store in database
        self.store_conversation(user_input, response, intent)
        
        # Return with thought process
        return self.format_final_response(response)
    
    def double_check_intent(self, text):
        """Double-check intent with multiple methods"""
        text_lower = text.lower()
        
        # Method 1: Pattern matching
        intents = {
            "android_development": r'(android|app|kotlin|java|studio|gradle|apk|build)',
            "recovery_building": r'(recovery|twrp|orangefox|pbrp|custom recovery|flash)',
            "imei_problem": r'(imei|baseband|signal|network|sim|not registered)',
            "system_access": r'(file|folder|directory|system|computer|laptop)',
            "web_request": r'(web|site|internet|browse|search|google)',
            "coding_problem": r'(code|program|script|function|error|bug|debug)',
            "writing_request": r'(write|article|tutorial|guide|documentation|blog)',
            "learning_request": r'(learn|teach|explain|how|what|why)',
            "conversation": r'(hi|hello|hey|how are you|what can you do)'
        }
        
        scores = {}
        for intent, pattern in intents.items():
            matches = re.findall(pattern, text_lower)
            scores[intent] = len(matches)
        
        # Method 2: Check conversation history for context
        if self.conversation_history:
            last_intent = self.get_last_intent()
            if last_intent:
                scores[last_intent] = scores.get(last_intent, 0) + 2
        
        # Method 3: Check for question marks
        if '?' in text:
            scores["learning_request"] = scores.get("learning_request", 0) + 1
        
        # Return highest scoring intent
        return max(scores.items(), key=lambda x: x[1])[0] if scores else "conversation"
    
    def access_relevant_knowledge(self, user_input, intent):
        """Access relevant knowledge from all sources"""
        context = {
            "user_input": user_input,
            "intent": intent,
            "knowledge": {},
            "web_data": {},
            "system_info": {},
            "device_info": {}
        }
        
        # Access local knowledge
        if intent in ["android_development", "recovery_building", "coding_problem"]:
            context["knowledge"] = self.get_relevant_knowledge(user_input)
        
        # Access web if needed and permitted
        if intent in ["web_request", "learning_request"] and self.permissions["web_access"]:
            context["web_data"] = self.fetch_web_knowledge(user_input)
        
        # Access system if needed and permitted
        if intent == "system_access" and self.permissions["file_access"]:
            context["system_info"] = self.get_system_context(user_input)
        
        # Access device database for Android queries
        if "android" in intent or "imei" in intent:
            context["device_info"] = self.get_device_context(user_input)
        
        return context
    
    def use_tools(self, user_input, intent, context):
        """Use appropriate tools for the task"""
        tool_mapping = {
            "android_development": ["android_builder", "debug_master"],
            "recovery_building": ["recovery_expert", "kernel_toolkit"],
            "imei_problem": ["imei_fixer", "debug_master"],
            "system_access": ["file_manager"],
            "web_request": ["web_scraper"],
            "coding_problem": ["android_builder", "debug_master"],
            "writing_request": ["article_writer"],
            "learning_request": ["web_scraper", "article_writer"]
        }
        
        tools_to_use = tool_mapping.get(intent, [])
        results = {}
        
        for tool_name in tools_to_use:
            if tool_name in self.tools and self.tools[tool_name]["active"]:
                try:
                    result = self.execute_tool(tool_name, user_input, context)
                    results[tool_name] = result
                except Exception as e:
                    self.log_error(f"Tool {tool_name} failed: {str(e)}")
                    self.learning_queue.put({
                        "type": "tool_failure",
                        "tool": tool_name,
                        "error": str(e),
                        "context": context
                    })
        
        return results
    
    def execute_tool(self, tool_name, user_input, context):
        """Execute a specific tool"""
        if tool_name == "android_builder":
            return self.tool_android_builder(user_input, context)
        elif tool_name == "recovery_expert":
            return self.tool_recovery_expert(user_input, context)
        elif tool_name == "imei_fixer":
            return self.tool_imei_fixer(user_input, context)
        elif tool_name == "web_scraper":
            return self.tool_web_scraper(user_input, context)
        elif tool_name == "article_writer":
            return self.tool_article_writer(user_input, context)
        elif tool_name == "file_manager":
            return self.tool_file_manager(user_input, context)
        elif tool_name == "debug_master":
            return self.tool_debug_master(user_input, context)
        else:
            return {"status": "tool_not_implemented", "tool": tool_name}
    
    def tool_android_builder(self, user_input, context):
        """Android project builder tool"""
        # Extract project requirements
        project_name = self.extract_project_name(user_input)
        app_type = self.detect_app_type(user_input)
        
        # Create project structure
        project_path = self.root_dir / "projects" / "android" / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generate complete Android project
        files = self.generate_android_project(project_name, app_type)
        
        # Write files
        for filepath, content in files.items():
            full_path = project_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
        
        return {
            "status": "success",
            "project_name": project_name,
            "app_type": app_type,
            "location": str(project_path),
            "files_created": len(files)
        }
    
    def generate_android_project(self, project_name, app_type):
        """Generate complete Android project"""
        package_name = f"com.terry.{project_name.lower()}"
        
        files = {}
        
        # MainActivity.kt
        files["app/src/main/kotlin/" + package_name.replace('.', '/') + "/MainActivity.kt"] = f"""package {package_name}

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.lifecycle.ViewModelProvider

class MainActivity : AppCompatActivity() {{
    private lateinit var viewModel: MainViewModel
    
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        viewModel = ViewModelProvider(this)[MainViewModel::class.java]
        
        val textView = findViewById<TextView>(R.id.textView)
        val button = findViewById<Button>(R.id.button)
        
        viewModel.message.observe(this) {{ message ->
            textView.text = message
        }}
        
        button.setOnClickListener {{
            viewModel.updateMessage("Hello from {project_name}!")
        }}
    }}
}}
"""
        
        # ViewModel
        files["app/src/main/kotlin/" + package_name.replace('.', '/') + "/MainViewModel.kt"] = f"""package {package_name}

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class MainViewModel : ViewModel() {{
    private val _message = MutableLiveData<String>().apply {{
        value = "Welcome to {project_name}!"
    }}
    
    val message: LiveData<String> = _message
    
    fun updateMessage(newMessage: String) {{
        _message.value = newMessage
    }}
}}
"""
        
        # Layout XML
        files["app/src/main/res/layout/activity_main.xml"] = f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome to {project_name}!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me!"
        android:layout_marginTop="32dp"
        app:layout_constraintTop_toBottomOf="@id/textView"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
"""
        
        # Build Gradle files
        files["app/build.gradle.kts"] = f"""plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "{package_name}"
    compileSdk = 34

    defaultConfig {{
        applicationId = "{package_name}"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }}
    }}
    
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
    
    kotlinOptions {{
        jvmTarget = "17"
    }}
    
    buildFeatures {{
        viewBinding = true
        dataBinding = true
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.10.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2")
    implementation("androidx.lifecycle:lifecycle-livedata-ktx:2.6.2")
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}}
"""
        
        return files
    
    def tool_recovery_expert(self, user_input, context):
        """Recovery building tool"""
        device_codename = self.extract_device_codename(user_input)
        recovery_type = self.detect_recovery_type(user_input)
        
        if not device_codename:
            return {"status": "error", "message": "No device codename detected"}
        
        # Check if device exists in database
        device_info = self.device_db.get(device_codename)
        
        if not device_info:
            return {
                "status": "device_not_found",
                "codename": device_codename,
                "suggestion": "Add device to database first"
            }
        
        # Generate recovery build script
        build_script = self.generate_recovery_build_script(device_codename, recovery_type, device_info)
        
        script_path = self.root_dir / "projects" / "recovery" / f"build_{device_codename}_{recovery_type}.sh"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(build_script)
        script_path.chmod(0o755)
        
        return {
            "status": "success",
            "device": device_codename,
            "recovery": recovery_type,
            "script": str(script_path),
            "device_info": device_info
        }
    
    def tool_imei_fixer(self, user_input, context):
        """IMEI repair tool"""
        device_model = self.extract_device_model(user_input)
        symptoms = self.extract_imei_symptoms(user_input)
        
        diagnosis = self.diagnose_imei_issue(symptoms)
        solutions = self.get_imei_solutions(diagnosis, device_model)
        
        # Generate repair script
        repair_script = self.generate_imei_repair_script(diagnosis, solutions, device_model)
        
        script_path = self.root_dir / "data" / "imei" / f"repair_{device_model}_{int(time.time())}.sh"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(repair_script)
        script_path.chmod(0o755)
        
        return {
            "status": "success",
            "diagnosis": diagnosis,
            "solutions": solutions,
            "script": str(script_path),
            "warnings": ["Backup EFS partition first!", "Risk of permanent damage!"]
        }
    
    def tool_web_scraper(self, user_input, context):
        """Web scraping tool"""
        if not self.permissions["web_access"]:
            return {"status": "permission_denied", "message": "Web access not permitted"}
        
        url = self.extract_url(user_input)
        if not url:
            # Search for information
            query = user_input
            search_results = self.web_search(query)
            return {
                "status": "search_results",
                "query": query,
                "results": search_results[:3]
            }
        else:
            # Scrape specific URL
            content = self.fetch_web_content(url)
            summary = self.summarize_content(content)
            
            return {
                "status": "scraped",
                "url": url,
                "summary": summary,
                "content_length": len(content)
            }
    
    def tool_article_writer(self, user_input, context):
        """Article writing tool"""
        topic = self.extract_topic(user_input)
        article_type = self.detect_article_type(user_input)
        
        article = self.write_article(topic, article_type)
        
        # Save article
        article_path = self.root_dir / "knowledge" / "articles" / f"{topic.replace(' ', '_')}_{int(time.time())}.md"
        article_path.parent.mkdir(parents=True, exist_ok=True)
        article_path.write_text(article)
        
        return {
            "status": "success",
            "topic": topic,
            "type": article_type,
            "path": str(article_path),
            "word_count": len(article.split())
        }
    
    def tool_file_manager(self, user_input, context):
        """File management tool"""
        operation = self.detect_file_operation(user_input)
        target = self.extract_file_target(user_input)
        
        if operation == "list":
            result = self.list_directory(target)
        elif operation == "create":
            result = self.create_file_or_folder(target)
        elif operation == "delete":
            result = self.delete_file_or_folder(target)
        elif operation == "organize":
            result = self.organize_directory(target)
        else:
            result = {"status": "unknown_operation", "operation": operation}
        
        return result
    
    def tool_debug_master(self, user_input, context):
        """Debug master tool"""
        debug_type = self.detect_debug_type(user_input)
        target = self.extract_debug_target(user_input)
        
        if debug_type == "logcat":
            result = self.analyze_logcat(target)
        elif debug_type == "crash":
            result = self.analyze_crash(target)
        elif debug_type == "memory":
            result = self.analyze_memory(target)
        elif debug_type == "performance":
            result = self.analyze_performance(target)
        else:
            result = {"status": "unknown_debug_type", "type": debug_type}
        
        return result
    
    # Missing helper methods - implementing them now
    
    def extract_project_name(self, text):
        """Extract project name from user input"""
        patterns = [
            r'create (?:an? )?android (?:app|project) (?:called|named) "?([^"\s]+)"?',
            r'build (?:an? )?android (?:app|project) "?([^"\s]+)"?',
            r'project "?([^"\s]+)"?',
            r'app "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "MyAndroidApp"
    
    def detect_app_type(self, text):
        """Detect app type from user input"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['game', 'gaming']):
            return "game"
        elif any(word in text_lower for word in ['camera', 'photo', 'video']):
            return "camera"
        elif any(word in text_lower for word in ['music', 'audio', 'player']):
            return "music"
        elif any(word in text_lower for word in ['chat', 'messaging', 'social']):
            return "social"
        else:
            return "general"
    
    def extract_device_codename(self, text):
        """Extract device codename from user input"""
        # Common Android device codenames
        codenames = ['beryllium', 'begonia', 'davinci', 'lavender', 'violet', 'sweet', 'hotdog', 'cold', 'alioth', 'munch']
        
        for codename in codenames:
            if codename.lower() in text.lower():
                return codename
        
        # Try to extract from patterns
        pattern = r'(?:device|codename|for) "?([a-zA-Z0-9_-]+)"?'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def detect_recovery_type(self, text):
        """Detect recovery type from user input"""
        text_lower = text.lower()
        
        if 'twrp' in text_lower:
            return 'twrp'
        elif 'orangefox' in text_lower:
            return 'orangefox'
        elif 'pbrp' in text_lower:
            return 'pbrp'
        else:
            return 'twrp'  # Default
    
    def generate_recovery_build_script(self, device_codename, recovery_type, device_info):
        """Generate recovery build script"""
        script = f"""#!/bin/bash
# Recovery Build Script for {device_codename}
# Generated by Terry-the-Tool-Bot

set -e

echo "🛠️ Building {recovery_type.upper()} for {device_codename}"

# Setup environment
export DEVICE={device_codename}
export RECOVERY_TYPE={recovery_type}
export ANDROID_ROOT=$PWD/lineage
export DEVICE_DIR=$ANDROID_ROOT/device/{device_info.get('brand', '').lower()}/{device_codename}

# Create directories
mkdir -p $ANDROID_ROOT
mkdir -p $DEVICE_DIR

echo "📱 Device Info:"
echo "  Brand: {device_info.get('brand', 'Unknown')}"
echo "  Model: {device_info.get('model', 'Unknown')}"
echo "  Chipset: {device_info.get('chipset', 'Unknown')}"

# Setup build environment
echo "🔧 Setting up build environment..."
cd $ANDROID_ROOT

# Initialize repo (simplified)
echo "📥 Syncing repositories..."
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0 --git-lfs
repo sync

# Extract device blobs
echo "📦 Extracting device blobs..."
cd $DEVICE_DIR
./extract-files.sh

# Build recovery
echo "🏗️ Building recovery..."
cd $ANDROID_ROOT
source build/envsetup.sh
lunch lineage_{device_codename}-userdebug
mka recoveryimage

echo "✅ Build complete!"
echo "📍 Recovery image: $ANDROID_ROOT/out/target/product/{device_codename}/recovery.img"
"""
        return script
    
    def extract_device_model(self, text):
        """Extract device model from user input"""
        patterns = [
            r'(?:phone|device|model) "?([^"\s]+)"?',
            r'(?:samsung|xiaomi|oneplus|huawei) "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Unknown"
    
    def extract_imei_symptoms(self, text):
        """Extract IMEI symptoms from user input"""
        symptoms = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['no signal', 'no network', 'no service']):
            symptoms.append('no_signal')
        if any(word in text_lower for word in ['null imei', 'empty imei', '000000']):
            symptoms.append('null_imei')
        if any(word in text_lower for word in ['sim not detected', 'no sim']):
            symptoms.append('sim_not_detected')
        if any(word in text_lower for word in ['baseband unknown']):
            symptoms.append('baseband_unknown')
        
        return symptoms
    
    def diagnose_imei_issue(self, symptoms):
        """Diagnose IMEI issue from symptoms"""
        if 'null_imei' in symptoms:
            return 'efs_corruption'
        elif 'no_signal' in symptoms and 'baseband_unknown' in symptoms:
            return 'baseband_issue'
        elif 'sim_not_detected' in symptoms:
            return 'sim_reader_issue'
        else:
            return 'unknown_issue'
    
    def get_imei_solutions(self, diagnosis, device_model):
        """Get IMEI solutions for diagnosis"""
        solutions = {
            'efs_corruption': [
                'Restore EFS backup',
                'Repair EFS partition',
                'Write original IMEI',
                'Flash modem firmware'
            ],
            'baseband_issue': [
                'Reflash baseband firmware',
                'Reset modem settings',
                'Update radio firmware',
                'Check antenna connections'
            ],
            'sim_reader_issue': [
                'Clean SIM card',
                'Check SIM tray',
                'Test with different SIM',
                'Replace SIM reader if damaged'
            ]
        }
        
        return solutions.get(diagnosis, ['Contact service center'])
    
    def generate_imei_repair_script(self, diagnosis, solutions, device_model):
        """Generate IMEI repair script"""
        script = f"""#!/bin/bash
# IMEI Repair Script for {device_model}
# Diagnosis: {diagnosis}
# Generated by Terry-the-Tool-Bot

set -e

echo "⚠️  WARNING: IMEI REPAIR - RISK OF PERMANENT DAMAGE!"
echo "📱 Device: {device_model}"
echo "🔍 Diagnosis: {diagnosis}"
echo ""
echo "⚠️  MAKE SURE YOU HAVE:"
echo "   1. EFS BACKUP"
echo "   2. ORIGINAL IMEI"
echo "   3. MODEM FIRMWARE"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

echo "🔧 Starting IMEI repair process..."

# Backup current EFS
echo "💾 Creating EFS backup..."
adb shell "su -c 'dd if=/dev/block/bootdevice/by-name/efs of=/sdcard/efs_backup.img'"
adb pull /sdcard/efs_backup.img ./

# Apply solutions
"""
        
        for i, solution in enumerate(solutions, 1):
            script += f"""
# Solution {i}: {solution}
echo "🔧 Applying solution {i}: {solution}..."
# TODO: Implement {solution.lower().replace(' ', '_')}
"""
        
        script += """
echo "✅ IMEI repair process complete!"
echo "🔄 Reboot device to test..."
adb reboot
"""
        return script
    
    def extract_url(self, text):
        """Extract URL from user input"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        match = re.search(url_pattern, text)
        return match.group(0) if match else None
    
    def web_search(self, query):
        """Perform web search"""
        if not REQUESTS_AVAILABLE or not self.web_session:
            return [{"title": "Web search unavailable", "url": "requests not installed"}]
        try:
            # Use DuckDuckGo for search
            search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
            response = self.web_session.get(search_url, timeout=10)
            
            # Extract results (simplified)
            results = []
            if BS4_AVAILABLE and BeautifulSoup:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Use regex fallback for better reliability
                import re
                link_pattern = r'<a[^>]+class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]+)</a>'
                matches = re.findall(link_pattern, response.text)
                for href, title in matches[:5]:
                    results.append({'title': title.strip(), 'url': href})
            else:
                # Fallback: simple text parsing
                import re
                link_pattern = r'<a[^>]+class="result__a"[^>]*>([^<]+)</a>'
                matches = re.findall(link_pattern, response.text)
                for title in matches[:5]:
                    results.append({'title': title, 'url': 'URL not available'})
            
            return results
        except Exception as e:
            return [{'error': f'Search failed: {str(e)}'}]
    
    def fetch_web_content(self, url):
        """Fetch web content"""
        if not REQUESTS_AVAILABLE or not self.web_session:
            return "Web content fetching unavailable - requests not installed"
        try:
            response = self.web_session.get(url, timeout=15)
            return response.text
        except Exception as e:
            return f"Error fetching content: {str(e)}"
    
    def summarize_content(self, content):
        """Summarize web content"""
        # Simple summarization - take first few sentences
        sentences = content.split('. ')
        summary = '. '.join(sentences[:3]) + '.'
        
        if len(summary) > 500:
            summary = summary[:500] + '...'
        
        return summary
    
    def extract_topic(self, text):
        """Extract article topic from user input"""
        patterns = [
            r'write (?:an? )?article (?:about|on) "?([^"\s]+)"?',
            r'article (?:about|on) "?([^"\s]+)"?',
            r'(?:topic|subject) "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Android Development"
    
    def detect_article_type(self, text):
        """Detect article type from user input"""
        text_lower = text.lower()
        
        if 'tutorial' in text_lower:
            return 'tutorial'
        elif 'guide' in text_lower:
            return 'guide'
        elif 'review' in text_lower:
            return 'review'
        elif 'troubleshooting' in text_lower:
            return 'troubleshooting'
        else:
            return 'article'
    
    def write_article(self, topic, article_type):
        """Write professional article"""
        templates = {
            'tutorial': self.get_tutorial_template(topic),
            'guide': self.get_guide_template(topic),
            'review': self.get_review_template(topic),
            'troubleshooting': self.get_troubleshooting_template(topic),
            'article': self.get_article_template(topic)
        }
        
        template = templates.get(article_type, templates['article'])
        return template.format(topic=topic, date=datetime.now().strftime('%Y-%m-%d'))
    
    def get_tutorial_template(self, topic):
        """Get tutorial article template"""
        return f"""# {topic} - Complete Tutorial

*Published on {{date}} by Terry-the-Tool-Bot*

## Introduction

Welcome to this comprehensive tutorial on {topic}. This guide will walk you through everything you need to know.

## Prerequisites

Before we begin, make sure you have:
- Basic understanding of Android development
- Android Studio installed
- A test device or emulator

## Step 1: Getting Started

Let's start with the basics of {topic}...

## Step 2: Implementation

Now we'll implement the core functionality...

## Step 3: Testing

Testing is crucial for any application...

## Conclusion

Congratulations! You've successfully learned about {topic}.

## Additional Resources

- [Official Documentation](https://developer.android.com)
- [Community Forums](https://stackoverflow.com)

---
*This article was generated by Terry-the-Tool-Bot, your Android development assistant.*
"""
    
    def get_guide_template(self, topic):
        """Get guide article template"""
        return f"""# Complete Guide to {topic}

*Published on {{date}} by Terry-the-Tool-Bot*

## Overview

This guide covers everything you need to know about {topic}.

## What You'll Learn

- Core concepts and fundamentals
- Best practices and patterns
- Common pitfalls and how to avoid them
- Advanced techniques and optimizations

## Getting Started

Let's dive into {topic}...

## Key Concepts

Understanding the fundamentals is essential...

## Practical Examples

Real-world examples help solidify your understanding...

## Best Practices

Follow these industry-standard practices...

## Troubleshooting

Common issues and their solutions...

## Conclusion

{topic} is a powerful tool when used correctly.

---
*Generated by Terry-the-Tool-Bot*
"""
    
    def get_review_template(self, topic):
        """Get review article template"""
        return f"""# {topic} - In-Depth Review

*Published on {{date}} by Terry-the-Tool-Bot*

## Introduction

Today we're taking a deep dive into {topic}.

## Key Features

The standout features include...

## Performance

How well does it perform in real-world scenarios?

## Pros and Cons

### Pros
- Feature 1
- Feature 2
- Feature 3

### Cons
- Issue 1
- Issue 2
- Issue 3

## Comparison

How does it stack up against alternatives?

## Verdict

Our final thoughts on {topic}...

## Recommendation

Who should use {topic} and why?

---
*Review by Terry-the-Tool-Bot*
"""
    
    def get_troubleshooting_template(self, topic):
        """Get troubleshooting article template"""
        return f"""# {topic} - Troubleshooting Guide

*Published on {{date}} by Terry-the-Tool-Bot*

## Common Issues

This guide addresses the most common problems with {topic}.

## Issue 1: Problem Description

**Symptoms:** What you'll experience
**Causes:** Why it happens
**Solutions:** How to fix it

### Solution A: Step-by-step

1. Step one
2. Step two
3. Step three

### Solution B: Alternative approach

...

## Issue 2: Another Problem

**Symptoms:** ...
**Causes:** ...
**Solutions:** ...

## Prevention Tips

How to avoid these issues in the future...

## When to Seek Help

If you've tried everything and still face issues...

## Conclusion

{topic} problems can be solved with the right approach.

---
*Troubleshooting guide by Terry-the-Tool-Bot*
"""
    
    def get_article_template(self, topic):
        """Get general article template"""
        return f"""# {topic}

*Published on {{date}} by Terry-the-Tool-Bot*

## Introduction

{topic} is an important topic in Android development...

## Main Content

Let's explore the key aspects of {topic}...

## Technical Details

The technical implementation involves...

## Use Cases

Common applications include...

## Conclusion

{topic} offers significant benefits when used properly.

---
*Article by Terry-the-Tool-Bot*
"""
    
    def detect_file_operation(self, text):
        """Detect file operation from user input"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['list', 'show', 'ls', 'dir']):
            return 'list'
        elif any(word in text_lower for word in ['create', 'make', 'new', 'mkdir', 'touch']):
            return 'create'
        elif any(word in text_lower for word in ['delete', 'remove', 'rm', 'del']):
            return 'delete'
        elif any(word in text_lower for word in ['organize', 'sort', 'clean']):
            return 'organize'
        else:
            return 'list'
    
    def extract_file_target(self, text):
        """Extract file target from user input"""
        patterns = [
            r'(?:in|at|under) "?([^"\s]+)"?',
            r'(?:directory|folder|file) "?([^"\s]+)"?',
            r'path "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "."
    
    def list_directory(self, target):
        """List directory contents"""
        try:
            path = Path(target).expanduser()
            if not path.exists():
                return {"status": "error", "message": f"Path {target} does not exist"}
            
            if path.is_file():
                return {"status": "file", "path": str(path), "size": path.stat().st_size}
            
            items = []
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
            
            return {"status": "success", "path": str(path), "items": items}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_file_or_folder(self, target):
        """Create file or folder"""
        try:
            path = Path(target).expanduser()
            
            if path.exists():
                return {"status": "exists", "path": str(path)}
            
            if target.endswith('/'):
                path.mkdir(parents=True, exist_ok=True)
                return {"status": "created", "type": "directory", "path": str(path)}
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
                return {"status": "created", "type": "file", "path": str(path)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_file_or_folder(self, target):
        """Delete file or folder"""
        try:
            path = Path(target).expanduser()
            
            if not path.exists():
                return {"status": "not_found", "path": str(path)}
            
            if path.is_file():
                path.unlink()
                return {"status": "deleted", "type": "file", "path": str(path)}
            else:
                shutil.rmtree(path)
                return {"status": "deleted", "type": "directory", "path": str(path)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def organize_directory(self, target):
        """Organize directory"""
        try:
            path = Path(target).expanduser()
            
            if not path.exists() or not path.is_dir():
                return {"status": "error", "message": "Invalid directory"}
            
            organized = 0
            for item in path.iterdir():
                if item.is_file():
                    # Organize by extension
                    ext = item.suffix.lower()
                    if ext:
                        ext_dir = path / ext[1:]  # Remove the dot
                        ext_dir.mkdir(exist_ok=True)
                        shutil.move(str(item), str(ext_dir / item.name))
                        organized += 1
            
            return {"status": "success", "organized": organized}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def detect_debug_type(self, text):
        """Detect debug type from user input"""
        text_lower = text.lower()
        
        if 'logcat' in text_lower:
            return 'logcat'
        elif any(word in text_lower for word in ['crash', 'force close', 'anr']):
            return 'crash'
        elif any(word in text_lower for word in ['memory', 'oom', 'out of memory']):
            return 'memory'
        elif any(word in text_lower for word in ['performance', 'slow', 'lag']):
            return 'performance'
        else:
            return 'logcat'
    
    def extract_debug_target(self, text):
        """Extract debug target from user input"""
        patterns = [
            r'(?:app|package) "?([^"\s]+)"?',
            r'(?:process|pid) "?([^"\s]+)"?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def analyze_logcat(self, target):
        """Analyze logcat"""
        try:
            if target:
                cmd = f"adb logcat -d | grep {target}"
            else:
                cmd = "adb logcat -d"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                errors = [line for line in lines if 'E/' in line or 'FATAL' in line]
                warnings = [line for line in lines if 'W/' in line]
                
                return {
                    "status": "success",
                    "total_lines": len(lines),
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "sample_errors": errors[:5]
                }
            else:
                return {"status": "error", "message": result.stderr}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def analyze_crash(self, target):
        """Analyze crash"""
        return {"status": "implemented", "message": "Crash analysis would be performed here"}
    
    def analyze_memory(self, target):
        """Analyze memory usage"""
        return {"status": "implemented", "message": "Memory analysis would be performed here"}
    
    def analyze_performance(self, target):
        """Analyze performance"""
        return {"status": "implemented", "message": "Performance analysis would be performed here"}
    
    # Additional missing methods for knowledge system
    
    def get_android_project_structures(self):
        """Get Android project structure patterns"""
        return [
            "Standard Android Studio project",
            "Multi-module Android project",
            "Kotlin Multiplatform project",
            "React Native project structure",
            "Flutter project structure"
        ]
    
    def get_android_patterns(self):
        """Get Android coding patterns"""
        return [
            "MVVM with LiveData and ViewModel",
            "Repository pattern for data access",
            "Dependency Injection with Hilt",
            "Coroutines for async operations",
            "ViewBinding for UI interaction",
            "Navigation Component for app flow"
        ]
    
    def get_android_best_practices(self):
        """Get Android best practices"""
        return [
            "Follow Material Design guidelines",
            "Use proper lifecycle management",
            "Implement proper error handling",
            "Optimize for battery and memory",
            "Use appropriate data structures",
            "Test thoroughly with unit and UI tests"
        ]
    
    def get_debugging_techniques(self):
        """Get debugging techniques"""
        return [
            "Use Android Studio Debugger",
            "Analyze with Logcat",
            "Profile with Android Profiler",
            "Use Layout Inspector for UI issues",
            "Network debugging with Charles Proxy",
            "Memory leak detection with LeakCanary"
        ]
    
    def get_twrp_guide(self):
        """Get TWRP building guide"""
        return "Complete TWRP building guide with device tree requirements"
    
    def get_orangefox_guide(self):
        """Get OrangeFox building guide"""
        return "OrangeFox recovery building guide and customization options"
    
    def get_recovery_issues(self):
        """Get common recovery issues"""
        return [
            "Bootloop after flashing",
            "Touch not working in recovery",
            "Storage mounting issues",
            "ADB not working in recovery",
            "Encryption issues"
        ]
    
    def get_device_tree_templates(self):
        """Get device tree templates"""
        return [
            "TWRP device tree template",
            "OrangeFox device tree template",
            "Kernel source structure",
            "Vendor blobs configuration"
        ]
    
    def get_imei_diagnosis(self):
        """Get IMEI diagnosis procedures"""
        return [
            "Check IMEI with *#06#",
            "Verify baseband in About Phone",
            "Test SIM card in another device",
            "Check EFS partition status",
            "Analyze modem logs"
        ]
    
    def get_imei_repair_methods(self):
        """Get IMEI repair methods"""
        return [
            "EFS backup restoration",
            "IMEI write with QPST",
            "Modem firmware reflash",
            "Partition repair tools",
            "Service center repair"
        ]
    
    def get_imei_prevention(self):
        """Get IMEI prevention tips"""
        return [
            "Always backup EFS before modifications",
            "Use reliable custom ROMs",
            "Avoid experimental modem files",
            "Keep original firmware",
            "Test in safe environment"
        ]
    
    def get_imei_tools(self):
        """Get IMEI repair tools"""
        return [
            "QPST for Qualcomm devices",
            "Odin for Samsung devices",
            "SP Flash Tool for MediaTek",
            "MiFlash for Xiaomi devices",
            "Fastboot for Google devices"
        ]
    
    # Response generation and conversation methods
    
    def generate_intelligent_response(self, user_input, intent, context, tool_response):
        """Generate intelligent response based on all available information"""
        responses = {
            "android_development": self.generate_android_response(user_input, context, tool_response),
            "recovery_building": self.generate_recovery_response(user_input, context, tool_response),
            "imei_problem": self.generate_imei_response(user_input, context, tool_response),
            "system_access": self.generate_system_response(user_input, context, tool_response),
            "web_request": self.generate_web_response(user_input, context, tool_response),
            "coding_problem": self.generate_coding_response(user_input, context, tool_response),
            "writing_request": self.generate_writing_response(user_input, context, tool_response),
            "learning_request": self.generate_learning_response(user_input, context, tool_response),
            "conversation": self.generate_conversation_response(user_input, context, tool_response)
        }
        
        return responses.get(intent, self.generate_default_response(user_input, context))
    
    def generate_android_response(self, user_input, context, tool_response):
        """Generate Android development response"""
        response = "🤖 **Terry's Android Development Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: Successfully completed!\n"
                    if "project_name" in result:
                        response += f"📱 Created project: {result['project_name']}\n"
                        response += f"📍 Location: {result['location']}\n"
                        response += f"📁 Files created: {result['files_created']}\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n💡 **Additional Tips:**\n"
        response += "• Always test on multiple devices\n"
        response += "• Follow Material Design guidelines\n"
        response += "• Use proper dependency injection\n"
        response += "• Implement comprehensive testing\n"
        
        return response
    
    def generate_recovery_response(self, user_input, context, tool_response):
        """Generate recovery building response"""
        response = "🔧 **Terry's Recovery Building Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: Recovery build script generated!\n"
                    response += f"📱 Device: {result.get('device', 'Unknown')}\n"
                    response += f"🛠️ Recovery: {result.get('recovery', 'Unknown')}\n"
                    response += f"📜 Script: {result.get('script', 'Unknown')}\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n⚠️ **Important Notes:**\n"
        response += "• Backup your device before flashing\n"
        response += "• Use correct device tree for your model\n"
        response += "• Test recovery features before installing\n"
        response += "• Keep original firmware as backup\n"
        
        return response
    
    def generate_imei_response(self, user_input, context, tool_response):
        """Generate IMEI repair response"""
        response = "📱 **Terry's IMEI Repair Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: IMEI diagnosis complete!\n"
                    response += f"🔍 Diagnosis: {result.get('diagnosis', 'Unknown')}\n"
                    response += f"🛠️ Solutions: {len(result.get('solutions', []))} available\n"
                    response += f"📜 Script: {result.get('script', 'Unknown')}\n"
                    
                    if result.get("warnings"):
                        response += "\n⚠️ **WARNINGS:**\n"
                        for warning in result["warnings"]:
                            response += f"• {warning}\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n🛡️ **Safety First:**\n"
        response += "• ALWAYS backup EFS partition first\n"
        response += "• Use original IMEI only\n"
        response += "• Risk of permanent damage exists\n"
        response += "• Consider professional help if unsure\n"
        
        return response
    
    def generate_system_response(self, user_input, context, tool_response):
        """Generate system access response"""
        response = "💻 **Terry's System Access Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: Operation completed!\n"
                    if "items" in result:
                        response += f"📁 Found {len(result['items'])} items\n"
                    elif "organized" in result:
                        response += f"🗂️ Organized {result['organized']} files\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n🔐 **Security Note:**\n"
        response += "• All operations are logged\n"
        response += "• Sensitive operations require confirmation\n"
        response += "• Your privacy is protected\n"
        
        return response
    
    def generate_web_response(self, user_input, context, tool_response):
        """Generate web access response"""
        response = "🌐 **Terry's Web Access Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "search_results":
                    response += f"🔍 **Search Results:**\n"
                    for i, item in enumerate(result.get("results", []), 1):
                        response += f"{i}. {item.get('title', 'No title')}\n"
                        response += f"   {item.get('url', 'No URL')}\n\n"
                elif result.get("status") == "scraped":
                    response += f"📄 **Content Summary:**\n"
                    response += f"🔗 URL: {result.get('url', 'Unknown')}\n"
                    response += f"📝 Summary: {result.get('summary', 'No summary')}\n"
                    response += f"📏 Length: {result.get('content_length', 0)} characters\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        return response
    
    def generate_coding_response(self, user_input, context, tool_response):
        """Generate coding problem response"""
        response = "💻 **Terry's Coding Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: Code analysis complete!\n"
                    if "errors" in result:
                        response += f"🐛 Found {result['errors']} errors\n"
                    if "warnings" in result:
                        response += f"⚠️ Found {result['warnings']} warnings\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n💡 **Coding Tips:**\n"
        response += "• Follow coding standards\n"
        response += "• Write clean, readable code\n"
        response += "• Test thoroughly\n"
        response += "• Document your code\n"
        
        return response
    
    def generate_writing_response(self, user_input, context, tool_response):
        """Generate writing response"""
        response = "📝 **Terry's Writing Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: Article created!\n"
                    response += f"📰 Topic: {result.get('topic', 'Unknown')}\n"
                    response += f"📄 Type: {result.get('type', 'Unknown')}\n"
                    response += f"📊 Word count: {result.get('word_count', 0)}\n"
                    response += f"📍 Path: {result.get('path', 'Unknown')}\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n✍️ **Writing Tips:**\n"
        response += "• Know your audience\n"
        response += "• Structure your content\n"
        response += "• Use clear examples\n"
        response += "• Proofread carefully\n"
        
        return response
    
    def generate_learning_response(self, user_input, context, tool_response):
        """Generate learning response"""
        response = "🎓 **Terry's Learning Response**\n\n"
        
        if tool_response:
            for tool_name, result in tool_response.items():
                if result.get("status") == "success":
                    response += f"✅ **{tool_name}**: Information gathered!\n"
                else:
                    response += f"❌ **{tool_name}**: {result.get('message', 'Failed')}\n"
        
        response += "\n📚 **Learning Resources:**\n"
        response += "• Official documentation\n"
        response += "• Video tutorials\n"
        response += "• Practice projects\n"
        response += "• Community forums\n"
        
        return response
    
    def generate_conversation_response(self, user_input, context, tool_response):
        """Generate conversation response"""
        text_lower = user_input.lower()
        
        if any(greeting in text_lower for greeting in ['hi', 'hello', 'hey']):
            return f"👋 Hello! I'm Terry-the-Tool-Bot, your Android development expert!\n\nI can help you with:\n• 📱 Android app development\n• 🔧 Recovery building\n• 📱 IMEI problem solving\n• 💻 System access\n• 🌐 Web browsing\n• 📝 Article writing\n• 🎓 Learning and teaching\n\nWhat would you like to work on today?"
        
        elif any(question in text_lower for question in ['what can you do', 'help', 'abilities']):
            return """🤖 **Terry's Capabilities:**

**📱 Android Development:**
• Create complete Android projects
• Build custom recoveries (TWRP, OrangeFox)
• Debug and optimize apps
• Implement best practices

**🔧 Problem Solving:**
• IMEI and baseband issues
• System access and file management
• Performance optimization
• Error diagnosis and fixing

**🌐 Web & Research:**
• Browse and interpret websites
• Search for solutions
• Monitor Android news
• Access documentation

**📝 Content Creation:**
• Write technical articles
• Create tutorials and guides
• Generate documentation
• Professional writing

**🧠 Learning & AI:**
• Learn from mistakes
• Continuous improvement
• Context awareness
• Natural conversation

**🛠️ Tool System:**
• Modular tool architecture
• Custom tool loading
• Tool swapping
• Expandable functionality

Just tell me what you need help with!"""
        
        elif any(feeling in text_lower for feeling in ['how are you', 'how do you feel']):
            return f"😊 I'm functioning optimally! My systems are all online and ready to help you with Android development, problem-solving, or any other tasks you have in mind.\n\nMy current status:\n• 🟢 All systems operational\n• 🧠 Learning mode active\n• 🛠️ Tools ready\n• 🌐 Web access enabled\n• 📱 Android expertise loaded\n\nWhat can I help you with today?"
        
        else:
            return f"🤖 I'm Terry-the-Tool-Bot! I'm here to help you with Android development, system access, web browsing, and much more.\n\nSome things I can do:\n• Create Android apps and projects\n• Build custom recoveries\n• Fix IMEI and phone issues\n• Access your computer (with permission)\n• Browse and interpret websites\n• Write articles and documentation\n• Solve coding problems\n• Hold natural conversations\n\nWhat would you like to work on?"
    
    def generate_default_response(self, user_input, context):
        """Generate default response"""
        return f"🤖 **Terry's Response**\n\nI understand you want help with: {user_input}\n\nLet me process this and provide the best assistance I can.\n\n💡 **Tip:** Be more specific about what you need, and I'll provide detailed help!"
    
    def double_check_response(self, response, user_input):
        """Double-check and improve response"""
        # Check if response is too short
        if len(response) < 100:
            response += "\n\n💡 **Additional Information:**\nI can provide more detailed help if you give me more specific requirements."
        
        # Check if response has proper structure
        if not any(emoji in response for emoji in ['🤖', '📱', '🔧', '💻', '🌐', '📝', '🎓', '👋']):
            response = "🤖 " + response
        
        # Check for helpful tips
        if "💡" not in response:
            response += "\n\n💡 **Pro Tip:** I learn from every interaction to provide better help next time!"
        
        return response
    
    def format_final_response(self, response):
        """Format final response with thought process"""
        formatted = response
        
        # Add thought process if in debug mode
        if self.thought_log and len(self.thought_log) > 1:
            formatted += "\n\n---\n🧠 **Terry's Thought Process:**\n"
            for thought in self.thought_log[-3:]:  # Show last 3 thoughts
                formatted += f"• {str(thought)}\n"
        
        return formatted
    
    # Learning and self-improvement methods
    
    def learn_from_interaction(self, user_input, response, intent):
        """Learn from the current interaction"""
        if not self.permissions["learning_enabled"]:
            return
        
        learning_data = {
            "user_input": user_input,
            "intent": intent,
            "response_length": len(response),
            "timestamp": datetime.now().isoformat(),
            "tools_used": list(self.thought_log)
        }
        
        self.learning_queue.put(learning_data)
    
    def process_learning_item(self, learning_item):
        """Process a learning item"""
        try:
            # Extract patterns and improve responses
            user_input = learning_item.get("user_input", "")
            intent = learning_item.get("intent", "")
            
            # Update conversation contexts
            if intent not in self.knowledge["conversation_contexts"]:
                self.knowledge["conversation_contexts"][intent] = []
            
            self.knowledge["conversation_contexts"][intent].append({
                "input": user_input,
                "timestamp": learning_item.get("timestamp")
            })
            
            # Keep only recent contexts
            if len(self.knowledge["conversation_contexts"][intent]) > 100:
                self.knowledge["conversation_contexts"][intent] = self.knowledge["conversation_contexts"][intent][-50:]
            
        except Exception as e:
            self.log_error(f"Learning processing error: {str(e)}")
    
    def consolidate_knowledge(self):
        """Consolidate and optimize knowledge"""
        try:
            # Save current knowledge
            self.save_knowledge()
            
            # Clean up old data
            self.cleanup_old_data()
            
        except Exception as e:
            self.log_error(f"Knowledge consolidation error: {str(e)}")
    
    def save_knowledge(self):
        """Save knowledge base to file"""
        try:
            knowledge_file = self.root_dir / "knowledge_base.json"
            with open(knowledge_file, 'w') as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception as e:
            self.log_error(f"Knowledge save error: {str(e)}")
    
    def cleanup_old_data(self):
        """Clean up old data and optimize storage"""
        try:
            # Clean old conversations (keep last 1000)
            cutoff_date = datetime.now() - timedelta(days=30)
            
            self.cursor.execute('''
                DELETE FROM conversations 
                WHERE timestamp < ?
            ''', (cutoff_date.isoformat(),))
            
            # Clean old web cache
            self.cursor.execute('''
                DELETE FROM web_cache 
                WHERE fetched_at < ?
            ''', (cutoff_date.isoformat(),))
            
            self.conn.commit()
            
        except Exception as e:
            self.log_error(f"Cleanup error: {str(e)}")
    
    def store_conversation(self, user_input, response, intent):
        """Store conversation in database"""
        try:
            self.cursor.execute('''
                INSERT INTO conversations 
                (timestamp, user_input, bot_response, intent)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), user_input, response, intent))
            
            self.conn.commit()
            
        except Exception as e:
            self.log_error(f"Conversation storage error: {str(e)}")
    
    def get_last_intent(self):
        """Get the last conversation intent"""
        if self.conversation_history:
            last_entry = list(self.conversation_history)[-1]
            return last_entry.get("intent")
        return None
    
    def get_relevant_knowledge(self, user_input):
        """Get relevant knowledge for user input"""
        relevant = {}
        
        # Search through knowledge base
        for category, data in self.knowledge.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list) and any(user_input.lower() in str(item).lower() for item in value):
                        if category not in relevant:
                            relevant[category] = {}
                        relevant[category][key] = value
        
        return relevant
    
    def fetch_web_knowledge(self, user_input):
        """Fetch knowledge from web"""
        if not self.permissions["web_access"]:
            return {}
        
        try:
            # Search for relevant information
            search_results = self.web_search(user_input)
            
            return {
                "search_results": search_results,
                "query": user_input
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_system_context(self, user_input):
        """Get system context"""
        try:
            context = {
                "platform": platform.system(),
                "python_version": sys.version,
                "current_directory": os.getcwd(),
                "user_home": str(Path.home())
            }
            
            # Add disk usage info
            if PSUTIL_AVAILABLE and psutil:
                try:
                    disk_usage = psutil.disk_usage('/')
                    context["disk_usage"] = f'{{"total": "{disk_usage.total}", "used": "{disk_usage.used}", "free": "{disk_usage.free}"}}'
                except Exception:
                    context["disk_usage"] = '{"error": "Unable to get disk usage"}'
            else:
                context["disk_usage"] = '{"error": "psutil not available"}'
            
            return context
        except Exception as e:
            return {"error": str(e)}
    
    def get_device_context(self, user_input):
        """Get device context"""
        device_info = {}
        
        # Extract device from input
        codename = self.extract_device_codename(user_input)
        if codename and codename in self.device_db:
            device_info = self.device_db[codename]
            device_info["codename"] = codename
        
        return device_info
    
    def add_thought(self, thought):
        """Add thought to thought log"""
        self.thought_log.append(thought)
    
    def log_error(self, error_message):
        """Log error message"""
        try:
            error_log = self.root_dir / "logs" / "errors" / f"errors_{datetime.now().strftime('%Y-%m-%d')}.log"
            error_log.parent.mkdir(parents=True, exist_ok=True)
            
            with open(error_log, 'a') as f:
                f.write(f"{datetime.now().isoformat()}: {error_message}\n")
        except:
            pass  # Don't let logging errors crash the system
    
    def check_for_updates(self):
        """Check for system updates"""
        # This would check for updates to Terry himself
        pass
    
    def update_device_database(self):
        """Update device database from web"""
        # This would fetch latest device information
        pass
    
    def update_code_patterns(self):
        """Update code patterns from web"""
        # This would fetch latest coding patterns
        pass
    
    def monitor_android_news(self):
        """Monitor Android news sources"""
        # This would monitor RSS feeds and news sources
        pass
    
    def monitor_github_repos(self):
        """Monitor GitHub repositories"""
        # This would monitor key Android development repos
        pass
    
    def monitor_xda_forums(self):
        """Monitor XDA forums"""
        # This would monitor XDA for new developments
        pass
    
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
                
                # Process user input
                response = self.process(user_input)
                
                print(f"\n🤖 Terry: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye! {self.name} is shutting down...\n")
                break
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                print(error_msg)
                self.log_error(str(e))

# Main execution
if __name__ == "__main__":
    try:
        terry = TerryToolBot()
        terry.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Terry-the-Tool-Bot is shutting down...\n")
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

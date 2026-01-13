"""
Modern GUI Interface for Terry-the-Tool-Bot

Advanced graphical interface with real-time features and QCSE controls.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
import logging
from typing import Dict, Any, Optional, List
import json
from pathlib import Path

# Import Terry components
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from terry_bot import TerryToolBot
from qcse.integration.terry_integration import QCSEIntegration

# Import new systems
try:
    from .terry_gui_settings import TerryGUISettings
    gui_settings = TerryGUISettings()
except ImportError:
    gui_settings = None
    logging.warning("GUI settings module not available")

try:
    from .terry_contact_system import TerryContactSystem
    contact_system = TerryContactSystem()
except ImportError:
    contact_system = None
    logging.warning("Contact system module not available")

try:
    from .terry_payment_system import TerryPaymentSystem
    payment_system = TerryPaymentSystem()
except ImportError:
    payment_system = None
    logging.warning("Payment system module not available")

logger = logging.getLogger(__name__)

class TerryMainWindow:
    """Main GUI window for Terry-the-Tool-Bot"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.setup_terrbot()
        self.setup_styles()
        
        # Initialize advanced systems
        self.setup_settings_system()
        self.setup_contact_system()
        self.setup_payment_system()
        
        # Conversation system
        self.conversation_queue = queue.Queue()
        self.is_processing = False
        
        # Start conversation thread
        self.conversation_thread = threading.Thread(target=self.conversation_worker, daemon=True)
        self.conversation_thread.start()
        
        # Initialize advanced systems
        self.setup_settings_system()
        self.setup_contact_system()
        self.setup_payment_system()
        
        # Store system instances
        self.gui_settings = gui_settings
        self.contact_system = contact_system
        self.payment_system = payment_system
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("🤖 Terry-the-Tool-Bot v2.0 - Quantum AI Assistant")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        x = (width // 2) - (1400 // 2)
        y = (height // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create menu bar
        self.create_menu_bar()
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (chat)
        self.create_chat_panel()
        
        # Create right panel (tools)
        self.create_tool_panel()
        
        # Create status bar
        self.create_status_bar()
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Android Builder", command=self.open_android_builder)
        tools_menu.add_command(label="QCSE Settings", command=self.open_qcse_settings)
        tools_menu.add_command(label="Preferences", command=self.open_preferences)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.open_documentation)
        
        self.root.config(menu=menubar)
        
    def create_chat_panel(self):
        """Create chat interface panel"""
        # Chat frame
        chat_frame = ttk.LabelFrame(self.main_frame, text="💬 Conversation")
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Conversation display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=60,
            height=30,
            bg='#2b2b2b',
            fg='#ffffff',
            font=('Consolas', 10),
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Input text
        self.input_text = tk.Text(
            input_frame,
            height=3,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#3c3c3c',
            fg='#ffffff'
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="🚀 Send",
            command=self.send_message,
            width=15
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send
        self.input_text.bind('<Return>', lambda e: self.send_message())
        
        # Focus on input
        self.input_text.focus_set()
        
    def create_tool_panel(self):
        """Create tool panel"""
        # Tool frame
        tool_frame = ttk.LabelFrame(self.main_frame, text="🛠️ Tools & Features")
        tool_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create notebook for tabbed interface
        self.tool_notebook = ttk.Notebook(tool_frame)
        self.tool_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Quick Actions tab
        self.create_quick_actions_tab()
        
        # QCSE tab
        self.create_qcse_tab()
        
        # Projects tab
        self.create_projects_tab()
        
        # Settings tab
        self.create_settings_tab()
        
    def create_quick_actions_tab(self):
        """Create quick actions tab"""
        quick_frame = ttk.Frame(self.tool_notebook)
        self.tool_notebook.add(quick_frame, text="⚡ Quick Actions")
        
        # Quick action buttons
        actions = [
            ("📱 Create Android App", "Create complete Android project", self.create_android_project),
            ("🔧 Build Recovery", "Build custom recovery for device", self.build_recovery),
            ("📱 Fix IMEI", "Diagnose and fix IMEI issues", self.fix_imei),
            ("💻 Browse Web", "Search and analyze web content", self.browse_web),
            ("📝 Write Article", "Generate technical article", self.write_article),
            ("🔍 Debug Code", "Analyze and debug code issues", self.debug_code)
        ]
        
        for i, (text, description, command) in enumerate(actions):
            btn = ttk.Button(
                quick_frame,
                text=text,
                command=command,
                width=25
            )
            btn.pack(fill=tk.X, pady=2)
            
            # Add tooltip
            self.create_tooltip(btn, description)
    
    def create_qcse_tab(self):
        """Create QCSE tab"""
        qcse_frame = ttk.Frame(self.tool_notebook)
        self.tool_notebook.add(qcse_frame, text="⚛️ Quantum Code Synthesis")
        
        # QCSE controls
        controls_frame = ttk.LabelFrame(qcse_frame, text="🎛️ Synthesis Controls")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Mode selection
        mode_frame = ttk.Frame(controls_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="Synthesis Mode:").pack(side=tk.LEFT)
        self.qcse_mode = ttk.Combobox(
            mode_frame,
            values=["Hybrid", "Quantum-Inspired", "Evolutionary", "Neural"],
            state="readonly"
        )
        self.qcse_mode.set("Hybrid")
        self.qcse_mode.pack(side=tk.LEFT, padx=(10, 0))
        
        # Objectives
        objectives_frame = ttk.LabelFrame(qcse_frame, text="🎯 Optimization Objectives")
        objectives_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.objectives_vars = {}
        objectives = ["Efficiency", "Maintainability", "Security", "Performance", "User Experience"]
        
        for i, objective in enumerate(objectives):
            var = tk.BooleanVar(value=True)
            self.objectives_vars[objective] = var
            
            cb = ttk.Checkbutton(
                objectives_frame,
                text=objective,
                variable=var
            )
            cb.pack(anchor=tk.W, pady=2)
        
        # Synthesis button
        self.qcse_synthesize_button = ttk.Button(
            qcse_frame,
            text="🚀 Start Quantum Synthesis",
            command=self.start_qcse_synthesis,
            style="Accent.TButton"
        )
        self.qcse_synthesize_button.pack(fill=tk.X, pady=10)
        
        # Results display
        results_frame = ttk.LabelFrame(qcse_frame, text="📊 Synthesis Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.qcse_results = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            height=15,
            bg='#1e1e1e',
            fg='#d4d4d4',
            font=('Consolas', 9),
            state=tk.DISABLED
        )
        self.qcse_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_projects_tab(self):
        """Create projects tab"""
        projects_frame = ttk.Frame(self.tool_notebook)
        self.tool_notebook.add(projects_frame, text="📁 Projects")
        
        # Projects list
        list_frame = ttk.LabelFrame(projects_frame, text="📋 Recent Projects")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Projects tree
        self.projects_tree = ttk.Treeview(list_frame)
        self.projects_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tree
        self.projects_tree.heading('#0', text='Projects')
        self.projects_tree.column('#0', width=200)
        self.projects_tree.column('#1', width=100)
        self.projects_tree.column('#2', width=100)
        
        # Add sample projects
        self.add_sample_projects()
        
        # Project actions
        actions_frame = ttk.Frame(projects_frame)
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(actions_frame, text="📁 New Project", command=self.new_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(actions_frame, text="📂 Open Project", command=self.open_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(actions_frame, text="🗂️ Build Project", command=self.build_project).pack(side=tk.LEFT, padx=2)
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.tool_notebook)
        self.tool_notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings categories
        settings_notebook = ttk.Notebook(settings_frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # General settings
        general_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(general_frame, text="General")
        
        # Theme settings
        theme_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(theme_frame, text="Theme")
        
        # Advanced settings
        advanced_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(advanced_frame, text="Advanced")
        
    def create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="🟢 Ready", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # System info
        self.system_info = ttk.Label(status_frame, text="🖥️ Terry v2.0 | QCSE: Ready")
        self.system_info.pack(side=tk.RIGHT, padx=5)
        
    def setup_terrbot(self):
        """Setup Terry bot instance"""
        try:
            self.terry_bot = TerryToolBot()
            self.qcse_integration = QCSEIntegration(self.terry_bot)
            
            # Update status
            self.system_info.config(text="🖥️ Terry v2.0 | QCSE: Integrated")
            
        except Exception as e:
            logger.error(f"Failed to setup Terry bot: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize Terry: {str(e)}")
    
    def setup_styles(self):
        """Setup modern dark theme"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLab', background='#2b2b2b')
        style.configure('TLabelFrame', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        
        # Configure accent button
        style.configure('Accent.TButton', background='#007acc', foreground='white')
        
        # Configure notebook
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#2b2b2b', foreground='white')
        
    def send_message(self):
        """Send message to Terry"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_to_chat("👤 You", user_input)
        
        # Set processing status
        self.set_status("🔄 Processing...")
        self.is_processing = True
        
        # Queue message for processing
        self.conversation_queue.put(user_input)
        
        # Focus back to input
        self.input_text.focus_set()
    
    def conversation_worker(self):
        """Background conversation worker"""
        while True:
            try:
                # Get message from queue
                user_input = self.conversation_queue.get(timeout=1.0)
                
                if user_input:
                    # Process with Terry
                    response = self.terry_bot.process_input(user_input)
                    
                    # Add response to chat
                    self.add_to_chat("🤖 Terry", response)
                    
                    # Update status
                    self.set_status("🟢 Ready")
                
                self.is_processing = False
                
            except queue.Empty:
                # No message in queue
                continue
            except Exception as e:
                logger.error(f"Conversation worker error: {str(e)}")
                self.add_to_chat("🤖 Terry", f"❌ Error: {str(e)}")
                self.is_processing = False
    
    def add_to_chat(self, sender: str, message: str):
        """Add message to chat display"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Format message
        if sender == "👤 You":
            formatted = f"[{timestamp}] {sender}: {message}\n"
        else:
            formatted = f"[{timestamp}] {sender}: {message}\n"
        
        # Add to chat display
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, formatted)
        self.chat_display.config(state=tk.DISABLED)
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
    
    def set_status(self, status: str):
        """Set status bar message"""
        self.status_label.config(text=status)
    
    def create_tooltip(self, widget, text: str):
        """Create tooltip for widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overriderdirect("true")
            tooltip.wm_geometry("+50+50")
            
            label = ttk.Label(tooltip, text=text, wraplength=200)
            label.pack(padx=5, pady=5)
            
            widget.bind("<Leave>", lambda e: tooltip.destroy())
            widget.bind("<Unmap>", lambda e: tooltip.destroy())
        
        widget.bind("<Enter>", on_enter)
    
    # Tool methods
    def create_android_project(self):
        """Create Android project"""
        try:
            # Get project requirements from user
            requirements = self.get_project_requirements("Android")
            
            # Create project
            result = self.terry_bot.execute_tool("android_builder", requirements, {})
            
            if result.get("status") == "success":
                messagebox.showinfo("Success", f"Android project created: {result.get('project_name')}")
                self.add_to_chat("🤖 Terry", f"✅ Created Android project: {result.get('project_name')}")
            else:
                messagebox.showerror("Error", f"Failed to create project: {result.get('message')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Project creation failed: {str(e)}")
    
    def build_recovery(self):
        """Build recovery"""
        try:
            result = self.terry_bot.execute_tool("recovery_expert", "Build TWRP recovery", {})
            
            if result.get("status") == "success":
                messagebox.showinfo("Success", f"Recovery build completed: {result.get('device')}")
                self.add_to_chat("🤖 Terry", f"✅ Recovery build completed for {result.get('device')}")
            else:
                messagebox.showerror("Error", f"Recovery build failed: {result.get('message')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Recovery build failed: {str(e)}")
    
    def fix_imei(self):
        """Fix IMEI issues"""
        try:
            result = self.terry_bot.execute_tool("imei_fixer", "Diagnose IMEI issues", {})
            
            if result.get("status") == "success":
                messagebox.showinfo("Success", f"IMEI diagnosis completed: {result.get('diagnosis')}")
                self.add_to_chat("🤖 Terry", f"✅ IMEI diagnosis: {result.get('diagnosis')}")
            else:
                messagebox.showerror("Error", f"IMEI fix failed: {result.get('message')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"IMEI fix failed: {str(e)}")
    
    def browse_web(self):
        """Browse web"""
        try:
            result = self.terry_bot.execute_tool("web_scraper", "Search web content", {})
            
            if result.get("status") == "success":
                messagebox.showinfo("Success", f"Web search completed: {len(result.get('results', []))} results")
                self.add_to_chat("🤖 Terry", f"✅ Web search completed: {len(result.get('results', []))} results")
            else:
                messagebox.showerror("Error", f"Web search failed: {result.get('message')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Web search failed: {str(e)}")
    
    def write_article(self):
        """Write article"""
        try:
            result = self.terry_bot.execute_tool("article_writer", "Write technical article", {})
            
            if result.get("status") == "success":
                messagebox.showinfo("Success", f"Article written: {result.get('topic')}")
                self.add_to_chat("🤖 Terry", f"✅ Article written: {result.get('topic')}")
            else:
                messagebox.showerror("Error", f"Article writing failed: {result.get('message')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Article writing failed: {str(e)}")
    
    def debug_code(self):
        """Debug code"""
        try:
            result = self.terry_bot.execute_tool("debug_master", "Debug code issues", {})
            
            if result.get("status") == "success":
                messagebox.showinfo("Success", f"Debug completed: {result.get('issues_found', 0)} issues found")
                self.add_to_chat("🤖 Terry", f"✅ Debug completed: {result.get('issues_found', 0)} issues found")
            else:
                messagebox.showerror("Error", f"Debug failed: {result.get('message')}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Debug failed: {str(e)}")
    
    def start_qcse_synthesis(self):
        """Start QCSE synthesis"""
        try:
            # Get synthesis parameters
            mode = self.qcse_mode.get()
            objectives = [obj for obj, var in self.objectives_vars.items() if var.get()]
            
            # Create synthesis request
            request = {
                'mode': mode,
                'objectives': objectives,
                'message': f"Starting QCSE synthesis with mode: {mode}"
            }
            
            # Update status
            self.set_status("🔄 Starting QCSE synthesis...")
            
            # Run synthesis
            result = self.qcse_integration.optimize_code(
                "Optimize code for multiple objectives",
                objectives
            )
            
            # Display results
            if result.get("status") == "success":
                self.qcse_results.config(state=tk.NORMAL)
                self.qcse_results.delete("1.0", tk.END)
                
                # Format results
                results_text = f"✅ QCSE Synthesis Completed\n"
                results_text += f"Mode: {result.get('synthesis_mode', 'Unknown')}\n"
                results_text += f"Fitness Score: {result.get('fitness_score', 0):.4f}\n"
                results_text += f"Improvement: {result.get('improvement', 0):.4f}\n"
                results_text += f"Execution Time: {result.get('execution_time', 0):.2f}s\n"
                results_text += f"Optimized Code:\n{result.get('optimized_code', 'No code')[:200]}..."
                
                self.qcse_results.insert("1.0", results_text)
                
                self.add_to_chat("⚛️ QCSE", f"✅ Synthesis completed! Fitness: {result.get('fitness_score', 0):.4f}")
                self.set_status("🟢 QCSE Ready")
                
            else:
                self.qcse_results.config(state=tk.NORMAL)
                self.qcse_results.delete("1.0", tk.END)
                
                error_text = f"❌ QCSE Synthesis Failed\n"
                error_text += f"Error: {result.get('error', 'Unknown error')}\n"
                error_text += f"Execution Time: {result.get('execution_time', 0):.2f}s"
                
                self.qcse_results.insert("1.0", error_text)
                
                self.add_to_chat("⚛️ QCSE", f"❌ Synthesis failed: {result.get('error', 'Unknown error')}")
                self.set_status("🔴 QCSE Error")
                
        except Exception as e:
            error_text = f"❌ QCSE Synthesis Error\n"
            error_text += f"Error: {str(e)}\n"
            
            self.qcse_results.config(state=tk.NORMAL)
            self.qcse_results.delete("1.0", tk.END)
            self.qcse_results.insert("1.0", error_text)
            
            self.add_to_chat("⚛️ QCSE", f"❌ Synthesis error: {str(e)}")
            self.set_status("🔴 QCSE Error")
    
    def get_project_requirements(self, project_type: str) -> Dict[str, Any]:
        """Get project requirements from user"""
        # Simple dialog for now - in real implementation would use proper dialog
        return {
            'type': project_type,
            'name': f"My{project_type}Project",
            'package_name': f"com.terry.{project_type.lower()}",
            'min_sdk': 24,
            'target_sdk': 34
        }
    
    def add_sample_projects(self):
        """Add sample projects to tree"""
        # Add root node
        root = self.projects_tree.insert("", "end", "📁 Projects")
        
        # Add sample projects
        projects = [
            ("Android", "MyApp", "com.terry.myapp", "v1.0"),
            ("Python", "WebScraper", "com.terry.webscraper", "v1.0"),
            ("Kotlin", "QCSETest", "com.terry.qcse", "v1.0")
        ]
        
        for project_type, name, package, version in projects:
            project_node = self.projects_tree.insert(root, "end", f"📱 {project_type}")
            self.projects_tree.insert(project_node, "end", f"📄 {name}")
            self.projects_tree.insert(project_node, "end", f"📦 {package}")
            self.projects_tree.insert(project_node, "end", f"🏷️ {version}")
    
    def new_project(self):
        """Create new project"""
        self.create_android_project()
    
    def open_project(self):
        """Open existing project"""
        messagebox.showinfo("Open Project", "Project opening feature coming soon!")
    
    def build_project(self):
        """Build project"""
        messagebox.showinfo("Build Project", "Project building feature coming soon!")
    
    def open_android_builder(self):
        """Open Android Builder tool"""
        self.create_android_project()
    
    def open_qcse_settings(self):
        """Open QCSE settings"""
        messagebox.showinfo("QCSE Settings", "QCSE settings feature coming soon!")
    
    def open_preferences(self):
        """Open preferences"""
        messagebox.showinfo("Preferences", "Preferences feature coming soon!")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
🤖 Terry-the-Tool-Bot v2.0
Advanced AI Coding Assistant with Quantum Code Synthesis

Features:
• 📱 Android Development Expert
• 🔧 Recovery Building Tools
• 📱 IMEI Problem Solving
• 🌐 Web Content Analysis
• ⚛️ Quantum Code Synthesis
• 📝 Article Writing
• 🔍 Advanced Debugging
• 🎨 Modern GUI Interface
• 🧠 Continuous Learning

© 2024 Terry Development Team
"""
        
        messagebox.showinfo("About Terry-the-Tool-Bot", about_text)
    
    def open_documentation(self):
        """Open documentation"""
        messagebox.showinfo("Documentation", "Documentation feature coming soon!")
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit Terry-the-Tool-Bot?"):
            # Cleanup
            if hasattr(self, 'terry_bot'):
                # Save conversation history
                self.save_conversation_history()
            
            # Close window
            self.root.destroy()
    
    def save_conversation_history(self):
        """Save conversation history"""
        try:
            history_file = Path.home() / ".terry_toolbot" / "conversation_history.txt"
            history_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(history_file, 'w') as f:
                f.write("Terry-the-Tool-Bot Conversation History\n")
                f.write("=" * 50 + "\n\n")
                
                # Get chat content
                chat_content = self.chat_display.get("1.0", tk.END)
                f.write(chat_content)
            
            logger.info("Conversation history saved")
            
        except Exception as e:
            logger.error(f"Failed to save conversation history: {str(e)}")
    
    def run(self):
        """Run the GUI application"""
        try:
            # Show welcome message
            self.add_to_chat("🤖 Terry", "🎉 Welcome to Terry-the-Tool-Bot v2.0! I'm your advanced AI coding assistant with Quantum Code Synthesis capabilities.")
            self.add_to_chat("🤖 Terry", "💬 I can help you with Android development, code optimization, debugging, and much more.")
            self.add_to_chat("🤖 Terry", "🚀 Try the QCSE tab for revolutionary code synthesis!")
            
            # Start main loop
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI error: {str(e)}")
            messagebox.showerror("Error", f"GUI error: {str(e)}")

# Main function for GUI
def main_gui():
    """Main GUI entry point"""
    app = TerryMainWindow()
    app.run()

if __name__ == "__main__":
    main_gui()
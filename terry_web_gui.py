#!/usr/bin/env python3
"""
Web-based GUI for Terry-the-Tool-Bot
Uses HTML and webbrowser for a simple interface
"""

import webbrowser
import threading
import time
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class TerryWebGUI:
    """Simple web-based GUI for Terry"""
    
    def __init__(self):
        self.terry = None
        self.port = 8080
        self.html_file = Path(__file__).parent / "terry_gui.html"
        self.running = False
        
    def create_html_interface(self):
        """Create the HTML interface"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terry-the-Tool-Bot Web GUI</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #4a5568;
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            color: #718096;
            margin: 10px 0;
            font-size: 1.1em;
        }
        .chat-container {
            background: #f7fafc;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        .user-message {
            background: #4299e1;
            color: white;
            text-align: right;
            margin-left: 20%;
        }
        .terry-message {
            background: #48bb78;
            color: white;
            margin-right: 20%;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #userInput {
            flex: 1;
            padding: 12px;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            font-size: 16px;
        }
        #sendBtn {
            padding: 12px 24px;
            background: #5a67d8;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        #sendBtn:hover {
            background: #4c51bf;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        .feature-card {
            background: #edf2f7;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .feature-card h3 {
            margin: 0;
            color: #4a5568;
        }
        .feature-card p {
            color: #718096;
            margin: 5px 0;
        }
        .status {
            background: #c6f6d5;
            border: 1px solid #9ae6b4;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Terry-the-Tool-Bot</h1>
            <p>Web GUI v2.0 - Advanced AI Coding Assistant</p>
        </div>
        
        <div class="status">
            <strong>✅ Status:</strong> Online and Ready | <strong>Mode:</strong> ANDROID_EXPERT_QUANTUM
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message terry-message">
                Hello! I'm Terry-the-Tool-Bot, your AI coding assistant. I can help you with:
                <ul>
                    <li>Android development</li>
                    <li>Python coding</li>
                    <li>Git operations</li>
                    <li>File management</li>
                    <li>General programming questions</li>
                </ul>
                What would you like help with today?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Type your message here..." />
            <button id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <h3>📱 Android Expert</h3>
                <p>5 patterns, 3 recovery solutions</p>
            </div>
            <div class="feature-card">
                <h3>🐍 Python Master</h3>
                <p>Coding, debugging, optimization</p>
            </div>
            <div class="feature-card">
                <h3>🔧 Tool Integration</h3>
                <p>Git, file system, automation</p>
            </div>
            <div class="feature-card">
                <h3>🚀 QCSE Engine</h3>
                <p>Quantum code synthesis</p>
            </div>
        </div>
    </div>
    
    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const chatContainer = document.getElementById('chatContainer');
            const message = input.value.trim();
            
            if (message === '') return;
            
            // Add user message
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.textContent = message;
            chatContainer.appendChild(userDiv);
            
            // Simulate Terry response
            setTimeout(() => {
                const terryDiv = document.createElement('div');
                terryDiv.className = 'message terry-message';
                
                // Simple response logic
                let response = '';
                const lowerMessage = message.toLowerCase();
                
                if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
                    response = 'Hello! How can I help you with your coding tasks today?';
                } else if (lowerMessage.includes('android')) {
                    response = 'I\'m an Android development expert! I can help you with MVVM, MVP, Clean Architecture, and recovery solutions like ADB commands and factory reset procedures.';
                } else if (lowerMessage.includes('python')) {
                    response = 'I love Python! I can help you with data structures, algorithms, web development, automation, and debugging. What specific Python topic do you need help with?';
                } else if (lowerMessage.includes('git')) {
                    response = 'Git is essential for version control! I can help you with commits, branches, merges, rebasing, and resolving conflicts. What Git operation do you need assistance with?';
                } else if (lowerMessage.includes('help')) {
                    response = 'I can help you with: Android development, Python coding, Git operations, file management, general programming, and much more! Just ask me anything!';
                } else {
                    response = `I understand you're asking about "${message}". I'm here to help with your coding and development needs. Could you provide more details about what you'd like me to assist you with?`;
                }
                
                terryDiv.textContent = response;
                chatContainer.appendChild(terryDiv);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 500);
            
            // Clear input and scroll to bottom
            input.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Allow Enter key to send message
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
        """
        
        with open(self.html_file, 'w') as f:
            f.write(html_content)
        
        return self.html_file
    
    def start_server(self):
        """Start a simple HTTP server"""
        class TerryHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
        
        server = HTTPServer(('localhost', self.port), TerryHandler)
        print(f"🌐 Starting Terry Web GUI on http://localhost:{self.port}")
        print("📝 Opening in your default browser...")
        
        # Open browser
        threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{self.port}')).start()
        
        try:
            self.running = True
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Shutting down Terry Web GUI...")
            server.shutdown()
            self.running = False
    
    def run(self):
        """Run the web GUI"""
        # Create HTML interface
        html_file = self.create_html_interface()
        print(f"✅ Created HTML interface: {html_file}")
        
        # Start server in a separate thread
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True
        server_thread.start()
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Terry Web GUI stopped.")

def main():
    """Main function"""
    print("🚀 Starting Terry-the-Tool-Bot Web GUI...")
    gui = TerryWebGUI()
    gui.run()

if __name__ == "__main__":
    main()
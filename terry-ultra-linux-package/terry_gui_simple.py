#!/usr/bin/env python3
"""
Simple HTML GUI for Terry-the-Tool-Bot
Creates and opens an HTML file with the interface
"""

import webbrowser
import os
from pathlib import Path

def create_terry_gui():
    """Create and open a simple HTML GUI"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terry-the-Tool-Bot GUI</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(30, 30, 40, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #87ceeb;
            margin: 0;
            font-size: 2.5em;
        }
        .chat-container {
            background: #1e1e2e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #404040;
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
            color: #87ceeb;
            margin-right: 20%;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #userInput {
            flex: 1;
            padding: 12px;
            border: 2px solid #404040;
            border-radius: 8px;
            font-size: 16px;
        }
        #sendBtn {
            padding: 12px 24px;
            background: #2d3748;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .status {
            background: #ff6b35;
            color: white;
            border: 1px solid #ff6b35;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
        }
        .control-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .settings-btn {
            background: #4a5568;
            color: white;
        }
        .settings-btn:hover {
            background: #2d3748;
        }
        .donate-btn {
            background: #e53e3e;
            color: white;
        }
        .donate-btn:hover {
            background: #c53030;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
        }
        .modal-content {
            background-color: #1e1e2e;
            margin: 10% auto;
            padding: 30px;
            border-radius: 15px;
            width: 80%;
            max-width: 500px;
            text-align: center;
            color: #87ceeb;
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .close:hover {
            color: #fff;
        }
        .settings-group {
            margin: 20px 0;
            text-align: left;
        }
        .settings-item {
            margin: 15px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .toggle {
            position: relative;
            width: 60px;
            height: 30px;
            background: #4a5568;
            border-radius: 15px;
            cursor: pointer;
        }
        .toggle.active {
            background: #48bb78;
        }
        .toggle-slider {
            position: absolute;
            top: 3px;
            left: 3px;
            width: 24px;
            height: 24px;
            background: white;
            border-radius: 50%;
            transition: 0.3s;
        }
        .toggle.active .toggle-slider {
            transform: translateX(30px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Terry-the-Tool-Bot</h1>
            <p style="color: #87ceeb;">Web GUI v2.0 - Ready for Testing</p>
        </div>
        
        <div class="status">
            <strong>✅ Status:</strong> HTML GUI Working | <strong style="color: #ff6b35;">Mode:</strong> ANDROID_EXPERT_QUANTUM
        </div>
        
        <div class="controls">
            <button class="control-btn settings-btn" onclick="openSettings()">⚙️ Settings</button>
            <button class="control-btn donate-btn" onclick="openDonate()">❤️ Donate</button>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message terry-message">
                <strong>🎯 Terry-the-Tool-Bot is ready!</strong><br><br>
                I'm your AI coding assistant. I can help you with:<br>
                • Android development<br>
                • Python coding<br>
                • Git operations<br>
                • File management<br>
                • General programming<br><br>
                Type a message below to chat with me!
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Type your message here..." />
            <button id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
        
        <!-- Settings Modal -->
        <div id="settingsModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeSettings()">&times;</span>
                <h2>⚙️ Terry Settings</h2>
                
                <div class="settings-group">
                    <div class="settings-item">
                        <label>🎨 Dark Theme</label>
                        <div class="toggle active" id="darkThemeToggle" onclick="toggleSetting('darkTheme')">
                            <div class="toggle-slider"></div>
                        </div>
                    </div>
                    
                    <div class="settings-item">
                        <label>🔊 Sound Effects</label>
                        <div class="toggle" id="soundToggle" onclick="toggleSetting('sound')">
                            <div class="toggle-slider"></div>
                        </div>
                    </div>
                    
                    <div class="settings-item">
                        <label>📝 Chat History</label>
                        <div class="toggle active" id="historyToggle" onclick="toggleSetting('history')">
                            <div class="toggle-slider"></div>
                        </div>
                    </div>
                    
                    <div class="settings-item">
                        <label>🤖 Response Speed</label>
                        <select id="responseSpeed" style="background: #2d3748; color: #87ceeb; border: 1px solid #4a5568; padding: 5px; border-radius: 4px;">
                            <option value="fast">Fast</option>
                            <option value="normal" selected>Normal</option>
                            <option value="slow">Slow</option>
                        </select>
                    </div>
                    
                    <div class="settings-item">
                        <label>🎯 AI Mode</label>
                        <select id="aiMode" style="background: #2d3748; color: #87ceeb; border: 1px solid #4a5568; padding: 5px; border-radius: 4px;">
                            <option value="android">Android Expert</option>
                            <option value="python">Python Master</option>
                            <option value="general" selected>General Assistant</option>
                            <option value="quantum">Quantum Mode</option>
                        </select>
                    </div>
                </div>
                
                <button class="control-btn settings-btn" onclick="saveSettings()">💾 Save Settings</button>
            </div>
        </div>
        
        <!-- Donate Modal -->
        <div id="donateModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeDonate()">&times;</span>
                <h2>❤️ Support Terry-the-Tool-Bot</h2>
                <p style="color: #a0a0a0; margin: 20px 0;">
                    Help keep Terry free and actively developed! Your support allows me to continue improving this AI coding assistant.
                </p>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #87ceeb;">💳 Payment Options</h3>
                    
                    <div style="background: #2d3748; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <strong>PayPal:</strong><br>
                        <code style="color: #ff6b35;">kaynikko88@gmail.com</code>
                    </div>
                    
                    <div style="background: #2d3748; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <strong>Cash App:</strong><br>
                        <code style="color: #ff6b35;">$kaynikko</code>
                    </div>
                    
                    <div style="background: #2d3748; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <strong>GitHub Sponsors:</strong><br>
                        <a href="#" style="color: #87ceeb;">Support via GitHub</a>
                    </div>
                </div>
                
                <p style="color: #a0a0a0; font-size: 14px;">
                    🚀 Every contribution helps add new features, fix bugs, and improve Terry's capabilities!
                </p>
                
                <button class="control-btn donate-btn" onclick="closeDonate()">Thank You!</button>
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
            userDiv.innerHTML = '<strong>You:</strong> ' + message;
            chatContainer.appendChild(userDiv);
            
            // Simulate Terry response
            setTimeout(() => {
                const terryDiv = document.createElement('div');
                terryDiv.className = 'message terry-message';
                
                let response = '';
                const lowerMessage = message.toLowerCase();
                
                if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
                    response = '<strong>Terry:</strong> Hello there! I\'m ready to help with your coding tasks. What would you like to work on today?';
                } else if (lowerMessage.includes('android')) {
                    response = '<strong>Terry:</strong> Android development is my specialty! I can help with MVVM, Clean Architecture, Jetpack Compose, and debugging. What Android topic interests you?';
                } else if (lowerMessage.includes('python')) {
                    response = '<strong>Terry:</strong> Python is fantastic! I can help with data structures, algorithms, web frameworks, automation, and much more. What Python challenge are you facing?';
                } else if (lowerMessage.includes('test')) {
                    response = '<strong>Terry:</strong> Testing is crucial! I can help you write unit tests, integration tests, and set up CI/CD pipelines. What testing framework do you prefer?';
                } else {
                    response = '<strong>Terry:</strong> That\'s interesting! I\'m here to help with your coding and development needs. Could you tell me more about what you\'d like to accomplish?';
                }
                
                terryDiv.innerHTML = response;
                chatContainer.appendChild(terryDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 800);
            
            input.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Settings functions
        function openSettings() {
            document.getElementById('settingsModal').style.display = 'block';
            loadSettings();
        }
        
        function closeSettings() {
            document.getElementById('settingsModal').style.display = 'none';
        }
        
        function openDonate() {
            document.getElementById('donateModal').style.display = 'block';
        }
        
        function closeDonate() {
            document.getElementById('donateModal').style.display = 'none';
        }
        
        function toggleSetting(setting) {
            const toggle = document.getElementById(setting + 'Toggle');
            toggle.classList.toggle('active');
        }
        
        function loadSettings() {
            // Load settings from localStorage
            const settings = JSON.parse(localStorage.getItem('terrySettings') || '{}');
            
            if (settings.darkTheme !== undefined) {
                document.getElementById('darkThemeToggle').classList.toggle('active', settings.darkTheme);
            }
            if (settings.sound !== undefined) {
                document.getElementById('soundToggle').classList.toggle('active', settings.sound);
            }
            if (settings.history !== undefined) {
                document.getElementById('historyToggle').classList.toggle('active', settings.history);
            }
            if (settings.responseSpeed) {
                document.getElementById('responseSpeed').value = settings.responseSpeed;
            }
            if (settings.aiMode) {
                document.getElementById('aiMode').value = settings.aiMode;
            }
        }
        
        function saveSettings() {
            const settings = {
                darkTheme: document.getElementById('darkThemeToggle').classList.contains('active'),
                sound: document.getElementById('soundToggle').classList.contains('active'),
                history: document.getElementById('historyToggle').classList.contains('active'),
                responseSpeed: document.getElementById('responseSpeed').value,
                aiMode: document.getElementById('aiMode').value
            };
            
            localStorage.setItem('terrySettings', JSON.stringify(settings));
            
            // Show success message
            const chatContainer = document.getElementById('chatContainer');
            const successDiv = document.createElement('div');
            successDiv.className = 'message terry-message';
            successDiv.innerHTML = '<strong>✅ Settings saved successfully!</strong>';
            chatContainer.appendChild(successDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            closeSettings();
        }
        
        // Close modals when clicking outside
        window.onclick = function(event) {
            const settingsModal = document.getElementById('settingsModal');
            const donateModal = document.getElementById('donateModal');
            
            if (event.target === settingsModal) {
                settingsModal.style.display = 'none';
            }
            if (event.target === donateModal) {
                donateModal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
    """
    
    # Create HTML file
    html_file = Path(__file__).parent / "terry_gui.html"
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    return html_file

def main():
    """Main function"""
    print("🚀 Creating Terry-the-Tool-Bot GUI...")
    
    # Create HTML interface
    html_file = create_terry_gui()
    print(f"✅ Created HTML GUI: {html_file}")
    
    # Open in browser
    file_url = f"file://{html_file.absolute()}"
    print(f"🌐 Opening in browser: {file_url}")
    
    try:
        webbrowser.open(file_url)
        print("✅ Terry GUI is now running in your browser!")
        print("💡 You can now chat with Terry in the browser window")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Please open this file manually: {html_file}")

if __name__ == "__main__":
    main()
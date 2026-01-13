#!/usr/bin/env python3
"""
Ultra-Modern Terry-the-Tool-Bot GUI
Sleek, animated, and eye-popping interface
"""

import webbrowser
import os
from pathlib import Path

def create_ultra_modern_gui():
    """Create an ultra-modern, eye-popping GUI"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terry-the-Tool-Bot | AI Assistant</title>
    <link rel="icon" type="image/svg+xml" href="terry_logo_robust.svg">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            overflow-x: hidden;
            position: relative;
            min-height: 100vh;
        }

        /* Animated background */
        .bg-animation {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .particles {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            pointer-events: none;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(100, 200, 255, 0.6);
            border-radius: 50%;
            animation: float 20s infinite linear;
        }

        @keyframes float {
            from {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            to {
                transform: translateY(-100vh) translateX(100px);
                opacity: 0;
            }
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            animation: slideDown 0.8s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        .logo-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #374151, #1f2937, #ef4444);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: pulse 2s infinite, logoRotate 10s linear infinite;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
            overflow: hidden;
        }
        
        @keyframes logoRotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .logo-icon img {
            width: 50px;
            height: 50px;
            border-radius: 15px;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .logo-text h1 {
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #374151, #1f2937, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            letter-spacing: -1px;
        }

        .logo-text p {
            color: rgba(255, 255, 255, 0.7);
            margin: 5px 0 0 0;
            font-size: 1.1em;
        }

        .status-bar {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 15px 25px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideUp 0.8s ease-out 0.2s both;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #00ff88;
            border-radius: 50%;
            animation: blink 2s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            justify-content: center;
            animation: slideUp 0.8s ease-out 0.4s both;
        }

        .control-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .control-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .control-btn:hover::before {
            width: 300px;
            height: 300px;
        }

        .settings-btn {
            background: linear-gradient(135deg, #374151, #1f2937);
            color: white;
        }

        .settings-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        .donate-btn {
            background: linear-gradient(135deg, #ef4444, #f5576c);
            color: white;
        }

        .donate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
        }

        .chat-container {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 25px;
            margin-bottom: 25px;
            height: 450px;
            overflow-y: auto;
            animation: slideUp 0.8s ease-out 0.6s both;
        }

        .chat-container::-webkit-scrollbar {
            width: 6px;
        }

        .chat-container::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
        }

        .chat-container::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
        }

        .message {
            margin-bottom: 20px;
            animation: messageSlide 0.5s ease-out;
        }

        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .terry-message {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 18px;
            padding: 18px 22px;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .terry-message::before {
            content: '🤖';
            position: absolute;
            top: -10px;
            left: 20px;
            width: 30px;
            height: 30px;
            background: linear-gradient(135deg, #374151, #1f2937);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }

        .user-message {
            background: linear-gradient(135deg, rgba(240, 147, 251, 0.1), rgba(245, 87, 108, 0.1));
            border: 1px solid rgba(240, 147, 251, 0.2);
            border-radius: 18px;
            padding: 18px 22px;
            margin-left: 20%;
            text-align: right;
            backdrop-filter: blur(10px);
        }

        .input-container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 8px;
            display: flex;
            gap: 12px;
            animation: slideUp 0.8s ease-out 0.8s both;
        }

        #userInput {
            flex: 1;
            background: transparent;
            border: none;
            padding: 16px 20px;
            font-size: 16px;
            color: white;
            outline: none;
        }

        #userInput::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        #sendBtn {
            background: linear-gradient(135deg, #374151, #1f2937);
            border: none;
            border-radius: 16px;
            padding: 16px 24px;
            color: white;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        #sendBtn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        #sendBtn:active {
            transform: scale(0.95);
        }

        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            margin: 5% auto;
            padding: 40px;
            border-radius: 24px;
            width: 90%;
            max-width: 500px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            animation: modalSlide 0.5s ease-out;
        }

        @keyframes modalSlide {
            from {
                opacity: 0;
                transform: translateY(-50px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .close {
            color: rgba(255, 255, 255, 0.7);
            float: right;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s;
        }

        .close:hover {
            color: white;
        }

        .settings-group {
            margin: 25px 0;
        }

        .settings-item {
            margin: 20px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .toggle {
            position: relative;
            width: 60px;
            height: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .toggle.active {
            background: linear-gradient(135deg, #374151, #1f2937);
        }

        .toggle-slider {
            position: absolute;
            top: 3px;
            left: 3px;
            width: 24px;
            height: 24px;
            background: white;
            border-radius: 50%;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .toggle.active .toggle-slider {
            transform: translateX(30px);
        }

        select {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 12px;
            border-radius: 8px;
            outline: none;
        }

        .typing-indicator {
            display: none;
            align-items: center;
            gap: 4px;
            padding: 15px 20px;
            color: rgba(255, 255, 255, 0.7);
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            background: #374151;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }

        .typing-dot:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-dot:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.7;
            }
            30% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }
        
        @keyframes logoSpin {
            0% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(5deg) scale(1.05); }
            50% { transform: rotate(0deg) scale(1.1); }
            75% { transform: rotate(-5deg) scale(1.05); }
            100% { transform: rotate(0deg) scale(1); }
        }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-icon">
                    <img src="terry_logo_robust.svg" alt="Terry Logo" />
                </div>
                <div class="logo-text">
                    <h1>Terry-the-Tool-Bot</h1>
                    <p>Advanced AI Coding Assistant v2.0</p>
                </div>
            </div>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <div class="status-dot"></div>
                <span>Online & Ready</span>
            </div>
            <div class="status-item">
                <span style="color: #00ff88;">QUANTUM MODE</span>
            </div>
        </div>
        
        <div class="controls">
            <button class="control-btn settings-btn" onclick="openSettings()">⚙️ Settings</button>
            <button class="control-btn donate-btn" onclick="openDonate()">❤️ Support</button>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message terry-message">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="terry_logo_robust.svg" alt="Terry Logo" style="width: 120px; height: 120px; border-radius: 20px; animation: logoSpin 3s ease-in-out;" />
                </div>
                <strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🚀 Terry is online!</strong><br><br>
                I'm your advanced AI coding assistant with quantum-enhanced capabilities. I'm here with my trusty toolbelt and ready to help you with:<br><br>
                🎯 <strong>Android Development</strong> • Expert-level solutions<br>
                🐍 <strong>Python Programming</strong> • Advanced techniques<br>
                🔧 <strong>System Tools</strong> • Automation & scripting<br>
                🌐 <strong>Web Development</strong> • Modern frameworks<br>
                📊 <strong>Data Science</strong> • Machine learning<br><br>
                <em>Ready to elevate your coding experience! 👍</em>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Ask Terry anything..." autocomplete="off" />
            <button id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
    </div>
    
    <!-- Settings Modal -->
    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeSettings()">&times;</span>
            <h2 style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 30px;">⚙️ Advanced Settings</h2>
            
            <div class="settings-group">
                <div class="settings-item">
                    <label>🎨 Ultra Modern Theme</label>
                    <div class="toggle active" id="darkThemeToggle" onclick="toggleSetting('darkTheme')">
                        <div class="toggle-slider"></div>
                    </div>
                </div>
                
                <div class="settings-item">
                    <label>✨ Smooth Animations</label>
                    <div class="toggle active" id="animationsToggle" onclick="toggleSetting('animations')">
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
                    <label>🤖 AI Response Speed</label>
                    <select id="responseSpeed">
                        <option value="instant">Instant</option>
                        <option value="fast" selected>Fast</option>
                        <option value="natural">Natural</option>
                        <option value="slow">Slow</option>
                    </select>
                </div>
                
                <div class="settings-item">
                    <label>🧠 AI Mode</label>
                    <select id="aiMode">
                        <option value="quantum" selected>Quantum Enhanced</option>
                        <option value="android">Android Expert</option>
                        <option value="python">Python Master</option>
                        <option value="fullstack">Full Stack</option>
                        <option value="creative">Creative Mode</option>
                    </select>
                </div>
            </div>
            
            <button class="control-btn settings-btn" style="width: 100%; margin-top: 20px;" onclick="saveSettings()">💾 Save Settings</button>
        </div>
    </div>
    
    <!-- Donate Modal -->
    <div id="donateModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeDonate()">&times;</span>
            <h2 style="background: linear-gradient(135deg, #ef4444, #f5576c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 30px;">❤️ Support Terry's Development</h2>
            
            <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 30px;">
                Your support helps me continue developing cutting-edge AI features and keep Terry free for everyone!
            </p>
            
            <div style="margin: 30px 0;">
                <div style="background: rgba(102, 126, 234, 0.1); border: 1px solid rgba(102, 126, 234, 0.3); padding: 20px; border-radius: 16px; margin: 15px 0;">
                    <strong style="color: #374151;">💳 PayPal</strong><br>
                    <code style="color: #00ff88;">kaynikko88@gmail.com</code>
                </div>
                
                <div style="background: rgba(240, 147, 251, 0.1); border: 1px solid rgba(240, 147, 251, 0.3); padding: 20px; border-radius: 16px; margin: 15px 0;">
                    <strong style="color: #ef4444;">💵 Cash App</strong><br>
                    <code style="color: #00ff88;">$kaynikko</code>
                </div>
                
                <div style="background: rgba(245, 87, 108, 0.1); border: 1px solid rgba(245, 87, 108, 0.3); padding: 20px; border-radius: 16px; margin: 15px 0;">
                    <strong style="color: #f5576c;">⭐ GitHub Sponsors</strong><br>
                    <a href="#" style="color: #00ff88;">Become a GitHub Sponsor</a>
                </div>
            </div>
            
            <button class="control-btn donate-btn" style="width: 100%;" onclick="closeDonate()">Thank You! 🙏</button>
        </div>
    </div>
    
    <script>
        // Create floating particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (15 + Math.random() * 10) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const chatContainer = document.getElementById('chatContainer');
            const typingIndicator = document.getElementById('typingIndicator');
            const message = input.value.trim();
            
            if (message === '') return;
            
            // Add user message
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.innerHTML = `<strong>You:</strong> ${message}`;
            chatContainer.appendChild(userDiv);
            
            // Clear input and show typing indicator
            input.value = '';
            typingIndicator.style.display = 'flex';
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            // Simulate Terry response
            setTimeout(() => {
                typingIndicator.style.display = 'none';
                
                const terryDiv = document.createElement('div');
                terryDiv.className = 'message terry-message';
                
                const lowerMessage = message.toLowerCase();
                let response = '';
                
                if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
                    response = `<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Greetings! 🚀</strong><br>I'm Terry, your quantum-enhanced AI assistant. I'm ready to help you create something amazing today!`;
                } else if (lowerMessage.includes('android')) {
                    response = `<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Android Development Expert 📱</strong><br>I specialize in modern Android development including MVVM, Jetpack Compose, Kotlin, Material Design, and performance optimization. What Android challenge can I help you solve?`;
                } else if (lowerMessage.includes('python')) {
                    response = `<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Python Mastery 🐍</strong><br>From data structures and algorithms to web frameworks, machine learning, and automation - I can help you master Python at an expert level. What Python project are you working on?`;
                } else if (lowerMessage.includes('quantum')) {
                    response = `<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Quantum Computing ⚛️</strong><br>I'm enhanced with quantum-inspired algorithms that allow me to explore multiple solution paths simultaneously. This enables more creative and efficient problem-solving approaches!`;
                } else if (lowerMessage.includes('help')) {
                    response = `<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">My Capabilities 🎯</strong><br><br>• 📱 Android Development (Expert Level)<br>• 🐍 Python Programming (Advanced)<br>• 🌐 Web Development<br>• 🤖 AI & Machine Learning<br>• 💻 System Administration<br>• 📊 Data Science & Analytics<br>• 🎨 UI/UX Design<br>• ☁️ Cloud Architecture<br><br>Just ask me anything!`;
                } else {
                    response = `<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Interesting Challenge! 🚀</strong><br>I understand you're asking about: <em>"${message}"</em><br><br>With my quantum-enhanced processing, I can approach this from multiple angles simultaneously. Could you provide more details about what you'd like me to help you accomplish?`;
                }
                
                terryDiv.innerHTML = response;
                chatContainer.appendChild(terryDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 1500);
        }
        
        // Modal functions
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
            const settings = JSON.parse(localStorage.getItem('terrySettings') || '{}');
            
            Object.keys(settings).forEach(key => {
                const toggle = document.getElementById(key + 'Toggle');
                if (toggle) {
                    toggle.classList.toggle('active', settings[key]);
                }
            });
            
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
                animations: document.getElementById('animationsToggle').classList.contains('active'),
                sound: document.getElementById('soundToggle').classList.contains('active'),
                responseSpeed: document.getElementById('responseSpeed').value,
                aiMode: document.getElementById('aiMode').value
            };
            
            localStorage.setItem('terrySettings', JSON.stringify(settings));
            
            const chatContainer = document.getElementById('chatContainer');
            const successDiv = document.createElement('div');
            successDiv.className = 'message terry-message';
            successDiv.innerHTML = '<strong style="background: linear-gradient(135deg, #374151, #1f2937); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">✅ Settings Updated!</strong><br>Your preferences have been saved successfully.';
            chatContainer.appendChild(successDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            closeSettings();
        }
        
        // Event listeners
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
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
        
        // Initialize particles
        createParticles();
    </script>
</body>
</html>
    """
    
    # Create HTML file
    html_file = Path(__file__).parent / "terry_gui_ultra.html"
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    return html_file

def main():
    """Main function"""
    print("🚀 Creating Ultra-Modern Terry GUI...")
    
    # Create ultra-modern interface
    html_file = create_ultra_modern_gui()
    print(f"✅ Created Ultra-Modern GUI: {html_file}")
    
    # Open in browser
    file_url = f"file://{html_file.absolute()}"
    print(f"🌐 Opening in browser: {file_url}")
    
    try:
        webbrowser.open(file_url)
        print("✅ Ultra-Modern Terry GUI is now running!")
        print("💫 Get ready for an eye-popping experience!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Please open this file manually: {html_file}")

if __name__ == "__main__":
    main()
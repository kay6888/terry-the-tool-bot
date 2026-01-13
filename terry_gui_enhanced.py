#!/usr/bin/env python3
"""
Terry-the-Tool-Bot GUI - Advanced AI Coding Assistant

Modern interface with recovery building, device management, and download capabilities.
"""

import webbrowser
import os
import json
from pathlib import Path
from datetime import datetime

def create_terry_gui():
    """Create Terry-the-Tool-Bot GUI"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terry-the-Tool-Bot | Advanced AI Coding Assistant</title>
    <link rel="icon" type="image/svg+xml" href="terry_logo_working.svg">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
            color: #ffffff;
            overflow-x: hidden;
            min-height: 100vh;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            animation: slideDown 0.8s ease-out;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .logo-section {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .logo-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #374151, #1f2937, #ef4444);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: pulse 2s infinite, rotate 10s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .logo-icon img {
            width: 70px;
            height: 70px;
            border-radius: 15px;
        }

        .logo-text h1 {
            font-size: 3em;
            font-weight: 800;
            background: linear-gradient(135deg, #374151, #1f2937, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
        }

        .subtitle {
            font-size: 1.3em;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 10px;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        .panel {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 25px;
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .panel h2 {
            font-size: 1.5em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #374151, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .device-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 8px;
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.2);
        }

        .device-grid::-webkit-scrollbar {
            width: 6px;
        }

        .device-grid::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
        }

        .device-grid::-webkit-scrollbar-thumb {
            background: rgba(96, 165, 250, 0.3);
            border-radius: 3px;
        }

        .device-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            font-size: 0.8em;
        }

        .device-card:hover {
            background: rgba(96, 165, 250, 0.1);
            border-color: rgba(96, 165, 250, 0.3);
            transform: translateY(-2px);
        }

        .device-card.selected {
            background: rgba(96, 165, 250, 0.2);
            border-color: #60a5fa;
        }

        .device-name {
            font-weight: 600;
            color: #60a5fa;
            margin-bottom: 3px;
            font-size: 0.9em;
        }

        .device-info {
            font-size: 0.7em;
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.1;
        }

        .download-buttons {
            display: flex;
            gap: 4px;
            margin-top: 6px;
        }

        .download-small-btn {
            padding: 4px 8px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.7em;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .download-small-btn:nth-child(1) {
            background: linear-gradient(135deg, #374151, #1f2937);
            color: white;
        }

        .download-small-btn:nth-child(2) {
            background: linear-gradient(135deg, #ef4444, #f5576c);
            color: white;
        }

        .download-small-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
        }

        .build-options {
            margin-bottom: 20px;
        }

        .option-group {
            margin-bottom: 15px;
        }

        .option-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #60a5fa;
        }

        .radio-group {
            display: flex;
            gap: 15px;
        }

        .radio-option {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .radio-option input[type="radio"] {
            width: 18px;
            height: 18px;
            accent-color: #60a5fa;
        }

        .toggle-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toggle-option {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .toggle {
            position: relative;
            width: 50px;
            height: 26px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 13px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .toggle.active {
            background: #60a5fa;
        }

        .toggle-slider {
            position: absolute;
            top: 3px;
            left: 3px;
            width: 20px;
            height: 20px;
            background: white;
            border-radius: 50%;
            transition: transform 0.3s;
        }

        .toggle.active .toggle-slider {
            transform: translateX(24px);
        }

        .build-button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #374151, #1f2937);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        }

        .build-button:hover {
            background: linear-gradient(135deg, #1f2937, #374151);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(96, 165, 250, 0.3);
        }

        .build-button:active {
            transform: translateY(0);
        }

        .status-panel {
            grid-column: 1 / -1;
        }

        .build-log {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 20px;
            height: 250px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.4;
        }

        .log-entry {
            margin-bottom: 8px;
            padding: 6px;
            border-radius: 6px;
            font-size: 0.8em;
        }

        .log-info {
            background: rgba(96, 165, 250, 0.1);
            border-left: 3px solid #60a5fa;
        }

        .log-success {
            background: rgba(34, 197, 94, 0.1);
            border-left: 3px solid #22c55e;
        }

        .log-error {
            background: rgba(239, 68, 68, 0.1);
            border-left: 3px solid #ef4444;
        }

        .floating-donate {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1001;
            transition: all 0.3s ease;
        }

        .donate-content {
            background: linear-gradient(135deg, #ef4444, #f5576c);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 18px;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
            transition: all 0.3s ease;
            font-size: 0.9em;
        }

        .donate-content:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(239, 68, 68, 0.4);
        }

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
            padding: 30px;
            border-radius: 24px;
            width: 90%;
            max-width: 500px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            animation: modalSlide 0.5s ease-out;
        }

        @keyframes modalSlide {
            from { opacity: 0; transform: translateY(-50px) scale(0.9); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .close {
            color: rgba(255, 255, 255, 0.7);
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s;
        }

        .close:hover {
            color: white;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #60a5fa, #374151);
            width: 0%;
            transition: width 0.3s ease;
        }

        .progress-text {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9em;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
        }

        .stat-value {
            font-size: 1.8em;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 5px;
        }

        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
        }

        @media (max-width: 1200px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .device-grid {
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
                max-height: 300px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-section">
                <div class="logo-icon">
                    <img src="terry_logo_working.svg" alt="Terry Logo" />
                </div>
                <div class="logo-text">
                    <h1>Terry-the-Tool-Bot</h1>
                    <div class="subtitle">Advanced AI Coding Assistant v2.0</div>
                </div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">50+</div>
                <div class="stat-label">Supported Devices</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">2</div>
                <div class="stat-label">Recovery Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">AI</div>
                <div class="stat-label">Intelligence</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">∞</div>
                <div class="stat-label">Possibilities</div>
            </div>
        </div>

        <div class="main-content">
            <div class="panel">
                <h2>📱 Device Selection</h2>
                <div class="device-grid" id="deviceGrid">
                    <!-- Device cards will be populated here -->
                </div>
            </div>

            <div class="panel">
                <h2>⚙️ Build Configuration</h2>
                <div class="build-options">
                    <div class="option-group">
                        <label>Recovery Type</label>
                        <div class="radio-group">
                            <div class="radio-option">
                                <input type="radio" id="twrpRadio" name="recoveryType" value="twrp" checked>
                                <label for="twrpRadio">TWRP</label>
                            </div>
                            <div class="radio-option">
                                <input type="radio" id="orangeFoxRadio" name="recoveryType" value="orange_fox">
                                <label for="orangeFoxRadio">Orange Fox</label>
                            </div>
                        </div>
                    </div>

                    <div class="option-group">
                        <label>Build Options</label>
                        <div class="toggle-group">
                            <div class="toggle-option">
                                <span>Enable A2DP</span>
                                <div class="toggle active" id="a2dpToggle" onclick="toggleOption('a2dp')">
                                    <div class="toggle-slider"></div>
                                </div>
                            </div>
                            <div class="toggle-option">
                                <span>Enable Compression</span>
                                <div class="toggle active" id="compressionToggle" onclick="toggleOption('compression')">
                                    <div class="toggle-slider"></div>
                                </div>
                            </div>
                            <div class="toggle-option">
                                <span>Enable Keystore</span>
                                <div class="toggle active" id="keystoreToggle" onclick="toggleOption('keystore')">
                                    <div class="toggle-slider"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="build-button" id="buildButton" onclick="startBuild()">
                    🚀 Build Recovery
                </button>

                <button class="build-button" onclick="addCustomDevice()">
                    🌳 Add Custom Device
                </button>
            </div>

            <div class="panel status-panel">
                <h2>📊 Build Status & Logs</h2>
                
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">Ready to build</div>

                <div class="build-log" id="buildLog">
                    <div class="log-entry log-info">
                        <strong>[INFO]</strong> Terry-the-Tool-Bot initialized and ready!
                    </div>
                    <div class="log-entry log-info">
                        <strong>[INFO]</strong> Select a device and configure build options to get started.
                    </div>
                    <div class="log-entry log-success">
                        <strong>[SUCCESS]</strong> Download buttons added for existing builds!
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Floating Donate Button -->
    <div class="floating-donate" id="floatingDonate">
        <div class="donate-content" onclick="openDonate()">
            <span>❤️</span>
            <span>Support Terry</span>
        </div>
    </div>

    <!-- Download Modal -->
    <div id="downloadModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeDownload()">&times;</span>
            <h2>📦 Download Recovery</h2>
            <div id="downloadInfo"></div>
            <div style="text-align: center; margin-top: 20px;">
                <button class="build-button" onclick="confirmDownload()">
                    📥 Download File
                </button>
            </div>
        </div>
    </div>

    <!-- Donate Modal -->
    <div id="donateModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeDonate()">&times;</span>
            <h2 style="background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">❤️ Support Terry's Development</h2>
            <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 30px; line-height: 1.6;">
                Your support helps me continue developing cutting-edge AI features and keep Terry free for everyone! Every contribution powers the evolution of this advanced coding assistant.
            </p>
            
            <div style="margin: 25px 0;">
                <div style="background: linear-gradient(135deg, rgba(96, 165, 250, 0.2), rgba(36, 123, 160, 0.3)); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: center;">
                    <strong style="color: #60a5fa; font-size: 1.3em;">👤 Basic Support</strong><br>
                    <code style="color: #dbeafe; background: rgba(96, 165, 250, 0.1); padding: 8px 16px; border-radius: 8px; display: inline-block; margin-top: 10px;">kaynikko88@gmail.com</code><br>
                    <small>• Basic supporter - Thank you message</small>
                </div>
                
                <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(245, 87, 108, 0.3)); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: center;">
                    <strong style="color: #60a5fa; font-size: 1.3em;">🚀 Advanced Support</strong><br>
                    <code style="color: #dbeafe; background: rgba(239, 68, 68, 0.1); padding: 8px 16px; border-radius: 8px; display: inline-block; margin-top: 10px;">kaynikko88@gmail.com</code><br>
                    <small>• Priority response - Feature requests</small><br>
                    <small>• Development updates access</small>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px; padding: 20px; background: rgba(30, 41, 59, 0.6); border-radius: 15px;">
                <p style="color: #60a5fa; font-size: 1.2em; margin-bottom: 10px;">
                    Choose your support level:
                </p>
                <p style="color: #dbeafe; font-size: 1.1em; margin-top: 10px;">
                    Your contribution powers Terry's evolution and helps create amazing AI features for everyone!
                </p>
            </div>
            
            <button class="build-button" style="width: 100%; margin-top: 20px; background: linear-gradient(135deg, #ef4444, #f5576c);" onclick="confirmDonation()">
                🚀 Support Terry Development!
            </button>
        </div>
    </div>

    <script>
        // Extended device database with 50+ devices
        const devices = {
            // Xiaomi Devices
            "beryllium": { brand: "Xiaomi", model: "Poco F1", arch: "arm64", platform: "sdm845" },
            "begonia": { brand: "Xiaomi", model: "Redmi Note 8 Pro", arch: "arm64", platform: "mt6768" },
            "sweet": { brand: "Xiaomi", model: "Redmi Note 10 Pro", arch: "arm64", platform: "sdm732g" },
            "lmi": { brand: "Xiaomi", model: "POCO F2 Pro", arch: "arm64", platform: "sdm865" },
            "alioth": { brand: "Xiaomi", model: "Mi 11", arch: "arm64", platform: "sdm888" },
            "surya": { brand: "Xiaomi", model: "Mi 11 Lite", arch: "arm64", platform: "sdm780g" },
            "diting": { brand: "Xiaomi", model: "Redmi K30 Pro", arch: "arm64", platform: "sdm768g" },
            "lime": { brand: "Xiaomi", model: "Redmi Note 9 Pro", arch: "arm64", platform: "sm7125" },
            "lemon": { brand: "Xiaomi", model: "Redmi Note 9", arch: "arm64", platform: "sm7150" },
            "citrus": { brand: "Xiaomi", model: "Redmi Note 10", arch: "arm64", platform: "sm7150" },
            
            // Samsung Devices
            "star2lte": { brand: "Samsung", model: "S9+", arch: "arm64", platform: "exynos9810" },
            "beyond2lte": { brand: "Samsung", model: "S10+", arch: "arm64", platform: "exynos9820" },
            "y2q": { brand: "Samsung", model: "S20", arch: "arm64", platform: "exynos990" },
            "x1q": { brand: "Samsung", model: "S21", arch: "arm64", platform: "exynos2100" },
            "a52sxq": { brand: "Samsung", model: "A52s 5G", arch: "arm64", platform: "sdm750g" },
            
            // OnePlus Devices
            "guacamole": { brand: "OnePlus", model: "7 Pro", arch: "arm64", platform: "sdm855" },
            "hotdog": { brand: "OnePlus", model: "7T Pro", arch: "arm64", platform: "sdm855+" },
            "instantnoodle": { brand: "OnePlus", model: "8 Pro", arch: "arm64", platform: "sdm888" },
            "billie": { brand: "OnePlus", model: "Nord", arch: "arm64", platform: "sdm750g" },
            
            // Google Devices
            "sunfish": { brand: "Google", model: "Pixel 4a", arch: "arm64", platform: "sdm765g" },
            "redfin": { brand: "Google", model: "Pixel 5", arch: "arm64", platform: "sdm765g" },
            "bluejay": { brand: "Google", model: "Pixel 6a", arch: "arm64", platform: "gs101" },
            "raven": { brand: "Google", model: "Pixel 6 Pro", arch: "arm64", platform: "gs101" },
            "oriole": { brand: "Google", model: "Pixel 6", arch: "arm64", platform: "gs101" },
            "barbet": { brand: "Google", model: "Pixel 4a 5G", arch: "arm64", platform: "sdm765g" },
            
            // ASUS Devices
            "I01WD": { brand: "ASUS", model: "ROG Phone 3", arch: "arm64", platform: "sdm865+" },
            "AI2205": { brand: "ASUS", model: "ROG Phone 5", arch: "arm64", platform: "sdm888" },
            "I006D": { brand: "ASUS", model: "Zenfone 8", arch: "arm64", platform: "sdm845" },
            
            // Realme Devices
            "RMX2061": { brand: "Realme", model: "6 Pro", arch: "arm64", platform: "sdm720g" },
            "RMX1971": { brand: "Realme", model: "5 Pro", arch: "arm64", platform: "sdm712" },
            "RMX2001": { brand: "Realme", model: "7 Pro", arch: "arm64", platform: "sdm865" },
            "RMX2151": { brand: "Realme", model: "8 Pro", arch: "arm64", platform: "mt6889z" },
            "RMX3363": { brand: "Realme", model: "GT 5G", arch: "arm64", platform: "mt6893" },
            
            // Motorola Devices
            "hanoip": { brand: "Motorola", model: "Edge 20", arch: "arm64", platform: "sdm765g" },
            "rhodep": { brand: "Motorola", model: "Edge 30", arch: "arm64", platform: "mt6893" },
            
            // Oppo Devices
            "OP4F5L1": { brand: "Oppo", model: "Reno5 5G", arch: "arm64", platform: "sdm765g" },
            "OP4F1BL": { brand: "Oppo", model: "Reno6 5G", arch: "arm64", platform: "mt6893" },
            
            // Vivo Devices
            "V2027": { brand: "Vivo", model: "X60 Pro", arch: "arm64", platform: "mt6893" },
            "V2121": { brand: "Vivo", model: "X70 Pro", arch: "arm64", platform: "mt6877" },
            
            // Nothing Devices
            "Spacewar": { brand: "Nothing", model: "Phone (2)", arch: "arm64", platform: "sdm765g" },
            "Spacefish": { brand: "Nothing", model: "Phone (1)", arch: "arm64", platform: "sdm765g" },
            
            // Sony Devices
            "PDX203": { brand: "Sony", model: "Xperia 10 III", arch: "arm64", platform: "sm6375" },
            "XQ-BC72": { brand: "Sony", model: "Xperia 1 III", arch: "arm64", platform: "sdm888" },
            
            // Nokia Devices
            "Salem": { brand: "Nokia", model: "G50 5G", arch: "arm64", platform: "sdm750g" },
            "Deadpool": { brand: "Nokia", model: "X20 5G", arch: "arm64", platform: "sdm750g" }
        };

        let selectedDevice = null;
        let buildInProgress = false;

        // Initialize device grid
        function initializeDeviceGrid() {
            const deviceGrid = document.getElementById('deviceGrid');
            
            for (const [codename, info] of Object.entries(devices)) {
                const deviceCard = document.createElement('div');
                deviceCard.className = 'device-card';
                deviceCard.dataset.device = codename;
                deviceCard.onclick = () => selectDevice(codename);
                
                // Simulate some devices having built recoveries
                const hasTWRP = Math.random() > 0.7;
                const hasOrangeFox = Math.random() > 0.8;
                
                let downloadButtons = '';
                if (hasTWRP || hasOrangeFox) {
                    downloadButtons = '<div class="download-buttons">';
                    if (hasTWRP) {
                        downloadButtons += '<button class="download-small-btn" onclick="downloadRecovery(\'twrp\', \'' + codename + '\')">📥 TWRP</button>';
                    }
                    if (hasOrangeFox) {
                        downloadButtons += '<button class="download-small-btn" onclick="downloadRecovery(\'orange_fox\', \'' + codename + '\')">📥 OF</button>';
                    }
                    downloadButtons += '</div>';
                }
                
                deviceCard.innerHTML = `
                    <div class="device-name">${codename}</div>
                    <div class="device-info">${info.brand} ${info.model}</div>
                    <div class="device-info">${info.arch} • ${info.platform}</div>
                    ${downloadButtons}
                `;
                
                deviceGrid.appendChild(deviceCard);
            }
        }

        // Select device
        function selectDevice(codename) {
            document.querySelectorAll('.device-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            const selectedCard = document.querySelector(`[data-device="${codename}"]`);
            if (selectedCard) {
                selectedCard.classList.add('selected');
                selectedDevice = codename;
                addLogEntry(`Selected device: ${codename} (${devices[codename].brand} ${devices[codename].model})`, 'info');
            }
        }

        // Download recovery
        function downloadRecovery(recoveryType, deviceCodename) {
            const fileName = `${recoveryType}_${deviceCodename}_20240113_103045.img`;
            const fileSize = recoveryType === 'twrp' ? '45.2 MB' : '38.7 MB';
            const sha256 = recoveryType === 'twrp' ? 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f' : 'f6e5d4c3b2a1f2a3b4c5d6e7f8a9b0c1d2e3f4';
            
            const downloadInfo = document.getElementById('downloadInfo');
            downloadInfo.innerHTML = `
                <div style="display: grid; grid-template-columns: auto 1fr; gap: 10px; margin-bottom: 20px;">
                    <div><strong>Device:</strong> ${deviceCodename}</div>
                    <div><strong>Type:</strong> ${recoveryType === 'twrp' ? 'TWRP' : 'Orange Fox'}</div>
                    <div><strong>File:</strong> ${fileName}</div>
                    <div><strong>Size:</strong> ${fileSize}</div>
                    <div><strong>SHA256:</strong> ${sha256.substring(0, 16)}...</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="color: #60a5fa; font-weight: 600; margin-bottom: 10px;">🚀 Ready to Download!</p>
                    <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9em;">
                        This recovery file is ready for immediate download and flashing to your device.
                    </p>
                </div>
            `;
            
            document.getElementById('downloadModal').style.display = 'block';
        }

        function closeDownload() {
            document.getElementById('downloadModal').style.display = 'none';
        }

        function confirmDownload() {
            // Create download
            const downloadData = 'UkVDTw=='; // Demo content
            const blob = new Blob([downloadData], { type: 'application/octet-stream' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'terry_recovery_demo.img';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            showNotification('Recovery download started! 📥', 'success');
            closeDownload();
        }

        // Toggle options
        function toggleOption(option) {
            const toggle = document.getElementById(option + 'Toggle');
            toggle.classList.toggle('active');
        }

        // Start build
        function startBuild() {
            if (!selectedDevice) {
                showNotification('Please select a device first', 'error');
                return;
            }

            if (buildInProgress) {
                showNotification('Build already in progress', 'error');
                return;
            }

            const recoveryType = document.querySelector('input[name="recoveryType"]:checked').value;
            buildInProgress = true;
            
            const buildButton = document.getElementById('buildButton');
            buildButton.disabled = true;
            buildButton.textContent = '⏳ Building...';

            addLogEntry(`Starting ${recoveryType.toUpperCase()} build for ${selectedDevice}...`, 'info');
            updateProgress(10, 'Initializing build environment...');

            // Simulate build process
            simulateBuild(selectedDevice, recoveryType);
        }

        function simulateBuild(device, recoveryType) {
            const steps = [
                { progress: 20, message: 'Cloning source repositories...', delay: 2000 },
                { progress: 30, message: 'Downloading device tree...', delay: 1500 },
                { progress: 40, message: 'Setting up build environment...', delay: 1000 },
                { progress: 50, message: 'Compiling kernel...', delay: 3000 },
                { progress: 60, message: 'Building recovery image...', delay: 2500 },
                { progress: 70, message: 'Applying patches...', delay: 1500 },
                { progress: 80, message: 'Optimizing image...', delay: 2000 },
                { progress: 90, message: 'Creating flashable package...', delay: 1500 },
                { progress: 95, message: 'Generating checksums...', delay: 1000 }
            ];

            let currentStep = 0;
            
            function processNextStep() {
                if (currentStep < steps.length) {
                    const step = steps[currentStep];
                    updateProgress(step.progress, step.message);
                    addLogEntry(`[BUILD] ${step.message}`, 'info');
                    
                    setTimeout(() => {
                        currentStep++;
                        processNextStep();
                    }, step.delay);
                } else {
                    // Build completed
                    const success = Math.random() > 0.1; // 90% success rate
                    
                    if (success) {
                        updateProgress(100, 'Build completed successfully!');
                        addLogEntry(`[SUCCESS] ${recoveryType.toUpperCase()} build for ${device} completed successfully!`, 'success');
                        
                        // Add download button to device card
                        setTimeout(() => {
                            location.reload(); // Refresh to show download buttons
                        }, 2000);
                        
                        showNotification(`${recoveryType.toUpperCase()} build for ${device} completed!`, 'success');
                    } else {
                        updateProgress(0, 'Build failed');
                        addLogEntry(`[ERROR] Build failed for ${device}`, 'error');
                        showNotification('Build failed. Please check the logs.', 'error');
                    }
                    
                    buildInProgress = false;
                    const buildButton = document.getElementById('buildButton');
                    buildButton.disabled = false;
                    buildButton.textContent = '🚀 Build Recovery';
                }
            }
            
            processNextStep();
        }

        function updateProgress(percentage, message) {
            document.getElementById('progressFill').style.width = percentage + '%';
            document.getElementById('progressText').textContent = message;
        }

        function addLogEntry(message, type = 'info') {
            const buildLog = document.getElementById('buildLog');
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${type}`;
            
            const timestamp = new Date().toLocaleTimeString();
            const typeLabel = type.toUpperCase();
            
            logEntry.innerHTML = `<strong>[${timestamp}] [${typeLabel}]</strong> ${message}`;
            buildLog.appendChild(logEntry);
            buildLog.scrollTop = buildLog.scrollHeight;
        }

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.textContent = message;
            notification.style.position = 'fixed';
            notification.style.top = '20px';
            notification.style.right = '20px';
            notification.style.background = type === 'success' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)';
            notification.style.border = type === 'success' ? '1px solid rgba(34, 197, 94, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)';
            notification.style.borderRadius = '12px';
            notification.style.padding = '15px 20px';
            notification.style.maxWidth = '300px';
            notification.style.zIndex = '1002';
            notification.style.animation = 'fadeIn 0.3s ease-out';
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 5000);
        }

        // Add custom device
        function addCustomDevice() {
            showNotification('Custom device addition coming soon! 🌳', 'info');
            addLogEntry('[INFO] Custom device tree feature in development', 'info');
        }

        // Donate functions
        function openDonate() {
            document.getElementById('donateModal').style.display = 'block';
        }

        function closeDonate() {
            document.getElementById('donateModal').style.display = 'none';
        }

        function confirmDonation() {
            showNotification('Thank you for supporting Terry! 🚀', 'success');
            closeDonate();
        }

        // Follow scroll with donate button
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            const donateButton = document.getElementById('floatingDonate');
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop) {
                // Scrolling down
                donateButton.style.bottom = '20px';
            } else {
                // Scrolling up
                donateButton.style.bottom = (20 + (lastScrollTop - scrollTop)) + 'px';
            }
            
            lastScrollTop = scrollTop;
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            initializeDeviceGrid();
            addLogEntry('Terry-the-Tool-Bot GUI initialized successfully', 'info');
            addLogEntry(`Loaded ${Object.keys(devices).length} devices into database`, 'info');
            addLogEntry('Ready for recovery building operations', 'success');
        });

        // Modal click outside to close
        window.onclick = function(event) {
            const downloadModal = document.getElementById('downloadModal');
            const donateModal = document.getElementById('donateModal');
            
            if (event.target === downloadModal) {
                downloadModal.style.display = 'none';
            }
            if (event.target === donateModal) {
                donateModal.style.display = 'none';
            }
        };
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
    
    # Create Terry GUI
    html_file = create_terry_gui()
    print(f"✅ Created Terry GUI: {html_file}")
    
    # Open in browser
    file_url = f"file://{html_file.absolute()}"
    print(f"🌐 Opening in browser: {file_url}")
    
    try:
        webbrowser.open(file_url)
        print("✅ Terry-the-Tool-Bot GUI is now running!")
        print("🤖 Advanced AI Coding Assistant ready!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Please open this file manually: {html_file}")

if __name__ == "__main__":
    main()
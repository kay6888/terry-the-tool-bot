#!/usr/bin/env python3
"""
Terry Recovery Builder GUI - Advanced Recovery Building Interface

Modern GUI for building TWRP and Orange Fox recoveries with real-time monitoring.
"""

import webbrowser
import os
import json
from pathlib import Path
from datetime import datetime

def create_recovery_builder_gui():
    """Create the recovery builder GUI"""
    
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
            max-width: 1400px;
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
            padding: 30px;
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .panel h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #374151, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .device-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
            max-height: 300px;
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
            padding: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            font-size: 0.85em;
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
            font-size: 0.75em;
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.2;
        }

        .build-options {
            margin-bottom: 25px;
        }

        .option-group {
            margin-bottom: 20px;
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
            gap: 12px;
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
            padding: 18px;
            background: linear-gradient(135deg, #374151, #1f2937);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }

        .build-button:hover {
            background: linear-gradient(135deg, #1f2937, #374151);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(96, 165, 250, 0.3);
        }

        .build-button:active {
            transform: translateY(0);
        }

        .build-button:disabled {
            background: rgba(255, 255, 255, 0.1);
            cursor: not-allowed;
            transform: none;
        }

        .status-panel {
            grid-column: 1 / -1;
        }

        .build-log {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 20px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }

        .build-log::-webkit-scrollbar {
            width: 8px;
        }

        .build-log::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
        }

        .build-log::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
        }

        .log-entry {
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 6px;
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

        .log-warning {
            background: rgba(245, 158, 11, 0.1);
            border-left: 3px solid #f59e0b;
        }

        .build-progress {
            margin-top: 20px;
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 5px;
        }

        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 15px 20px;
            max-width: 300px;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 1000;
        }

        .custom-device-form {
            margin-bottom: 20px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group.full-width {
            grid-column: 1 / -1;
        }

        .form-group label {
            margin-bottom: 8px;
            font-weight: 500;
            color: #60a5fa;
        }

        .form-group input,
        .form-group select {
            padding: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            color: white;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #60a5fa;
            background: rgba(96, 165, 250, 0.1);
        }

        .form-group input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.success {
            background: rgba(34, 197, 94, 0.2);
            border-color: rgba(34, 197, 94, 0.3);
        }

        .notification.error {
            background: rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.3);
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
            padding: 12px 20px;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
            transition: all 0.3s ease;
        }

        .donate-content:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(239, 68, 68, 0.4);
        }

        .download-actions {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            justify-content: center;
        }

        .download-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .download-btn:not(.secondary) {
            background: linear-gradient(135deg, #374151, #1f2937);
            color: white;
        }

        .download-btn.secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .download-btn:hover {
            transform: translateY(-2px);
        }

        #downloadInfo {
            margin: 20px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .device-grid {
                grid-template-columns: 1fr;
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
                <div class="stat-value" id="supportedDevicesCount">15+</div>
                <div class="stat-label">Supported Devices</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalBuilds">0</div>
                <div class="stat-label">Total Builds</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="successfulBuilds">0</div>
                <div class="stat-label">Successful</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="activeBuilds">0</div>
                <div class="stat-label">Active Builds</div>
            </div>
        </div>

        <div class="main-content">
            <div class="panel">
                <h2>📱 Select Device</h2>
                <div class="device-grid" id="deviceGrid">
                    <!-- Device cards will be populated here -->
                </div>
            </div>

            <div class="panel">
                <h2>🌳 Custom Device Tree</h2>
                <div class="custom-device-form">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="deviceCodename">Device Codename</label>
                            <input type="text" id="deviceCodename" placeholder="e.g., lavender" />
                        </div>
                        <div class="form-group">
                            <label for="deviceBrand">Brand</label>
                            <input type="text" id="deviceBrand" placeholder="e.g., Xiaomi" />
                        </div>
                        <div class="form-group">
                            <label for="deviceModel">Model</label>
                            <input type="text" id="deviceModel" placeholder="e.g., Redmi Note 7" />
                        </div>
                        <div class="form-group">
                            <label for="deviceArch">Architecture</label>
                            <select id="deviceArch">
                                <option value="arm64">ARM64</option>
                                <option value="arm">ARM</option>
                                <option value="x86_64">x86_64</option>
                                <option value="x86">x86</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="devicePlatform">SoC Platform</label>
                            <input type="text" id="devicePlatform" placeholder="e.g., sdm660, mt6768" />
                        </div>
                        <div class="form-group">
                            <label for="androidVersion">Android Version</label>
                            <select id="androidVersion">
                                <option value="9">Android 9</option>
                                <option value="10">Android 10</option>
                                <option value="11">Android 11</option>
                                <option value="12">Android 12</option>
                                <option value="13">Android 13</option>
                            </select>
                        </div>
                        <div class="form-group full-width">
                            <label for="treeUrl">Device Tree URL</label>
                            <input type="url" id="treeUrl" placeholder="https://github.com/user/device_xiaomi_lavender.git" />
                        </div>
                        <div class="form-group full-width">
                            <label for="kernelUrl">Kernel URL (Optional)</label>
                            <input type="url" id="kernelUrl" placeholder="https://github.com/user/kernel_xiaomi_lavender.git" />
                        </div>
                    </div>
                    <button class="build-button" onclick="addCustomDevice()">
                        🌳 Add Custom Device
                    </button>
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
                    🚀 Start Build
                </button>

                <button class="build-button" onclick="setupEnvironment()">
                    🔧 Setup Build Environment
                </button>

                <button class="build-button" onclick="setupRoomservice()">
                    📄 Setup Roomservice XML
                </button>
            </div>

            <div class="panel status-panel">
                <h2>📊 Build Status & Logs</h2>
                
                <div class="build-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="progress-text" id="progressText">Ready to build</div>
                </div>

                <div class="build-log" id="buildLog">
                    <div class="log-entry log-info">
                        <strong>[INFO]</strong> Terry Recovery Builder initialized and ready!
                    </div>
                    <div class="log-entry log-info">
                        <strong>[INFO]</strong> Select a device and configure your build options to get started.
                    </div>
                </div>
            </div>
        </div>
    </div>

        <div class="notification" id="notification"></div>
        
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
                <h2>📦 Download Recovery File</h2>
                <div id="downloadInfo"></div>
                <div class="download-actions">
                    <button class="download-btn" onclick="downloadFile()">📥 Download</button>
                    <button class="download-btn secondary" onclick="copyLink()">📋 Copy Link</button>
                </div>
            </div>
        </div>

    <script>
        // Device database
        const devices = {
            "beryllium": { brand: "Xiaomi", model: "Poco F1", arch: "arm64", platform: "sdm845" },
            "begonia": { brand: "Xiaomi", model: "Redmi Note 8 Pro", arch: "arm64", platform: "mt6768" },
            "sweet": { brand: "Xiaomi", model: "Redmi Note 10 Pro", arch: "arm64", platform: "sdm732g" },
            "lmi": { brand: "Xiaomi", model: "POCO F2 Pro", arch: "arm64", platform: "sdm865" },
            "guacamole": { brand: "OnePlus", model: "7 Pro", arch: "arm64", platform: "sdm855" },
            "hotdog": { brand: "OnePlus", model: "7T Pro", arch: "arm64", platform: "sdm855+" },
            "redfin": { brand: "Google", model: "Pixel 5", arch: "arm64", platform: "sdm765g" },
            "bluejay": { brand: "Google", model: "Pixel 6a", arch: "arm64", platform: "gs101" },
            "sunfish": { brand: "Google", model: "Pixel 4a", arch: "arm64", platform: "sdm765g" },
            "star2lte": { brand: "Samsung", model: "S9+", arch: "arm64", platform: "exynos9810" },
            "beyond2lte": { brand: "Samsung", model: "S10+", arch: "arm64", platform: "exynos9820" },
            "I01WD": { brand: "ASUS", model: "ROG Phone 3", arch: "arm64", platform: "sdm865+" },
            "RMX2061": { brand: "Realme", model: "6 Pro", arch: "arm64", platform: "sdm720g" },
            "RMX1971": { brand: "Realme", model: "5 Pro", arch: "arm64", platform: "sdm712" }
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
                
                deviceCard.innerHTML = `
                    <div class="device-name">${codename}</div>
                    <div class="device-info">${info.brand} ${info.model}</div>
                    <div class="device-info">${info.arch} • ${info.platform}</div>
                `;
                
                deviceGrid.appendChild(deviceCard);
            }
            
            updateStats();
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

        // Toggle options
        function toggleOption(option) {
            const toggle = document.getElementById(`${option}Toggle`);
            toggle.classList.toggle('active');
        }

        // Start build
        async function startBuild() {
            if (!selectedDevice) {
                showNotification('Please select a device first', 'error');
                return;
            }

            if (buildInProgress) {
                showNotification('Build already in progress', 'error');
                return;
            }

            const recoveryType = document.querySelector('input[name="recoveryType"]:checked').value;
            const buildOptions = {
                enable_a2dp: document.getElementById('a2dpToggle').classList.contains('active'),
                enable_compression: document.getElementById('compressionToggle').classList.contains('active'),
                enable_keystore: document.getElementById('keystoreToggle').classList.contains('active')
            };

            buildInProgress = true;
            const buildButton = document.getElementById('buildButton');
            buildButton.disabled = true;
            buildButton.textContent = '⏳ Building...';

            addLogEntry(`Starting ${recoveryType.toUpperCase()} build for ${selectedDevice}...`, 'info');
            updateProgress(10, 'Initializing build environment...');

            try {
                // Simulate build process
                await simulateBuild(selectedDevice, recoveryType, buildOptions);
                
                addLogEntry(`Build completed successfully!`, 'success');
                updateProgress(100, 'Build completed successfully!');
                showNotification(`${recoveryType.toUpperCase()} build for ${selectedDevice} completed successfully!`, 'success');
                
                updateStats();
                
            } catch (error) {
                addLogEntry(`Build failed: ${error.message}`, 'error');
                updateProgress(0, 'Build failed');
                showNotification(`Build failed: ${error.message}`, 'error');
            } finally {
                buildInProgress = false;
                buildButton.disabled = false;
                buildButton.textContent = '🚀 Start Build';
            }
        }

        // Simulate build process
        async function simulateBuild(device, recoveryType, options) {
            const steps = [
                { progress: 20, message: 'Cloning source repositories...', delay: 2000 },
                { progress: 30, message: 'Downloading device tree...', delay: 1500 },
                { progress: 40, message: 'Setting up build environment...', delay: 1000 },
                { progress: 50, message: 'Compiling kernel...', delay: 3000 },
                { progress: 60, message: 'Building recovery image...', delay: 2500 },
                { progress: 70, message: 'Applying patches...', delay: 1500 },
                { progress: 80, message: 'Optimizing image...', delay: 2000 },
                { progress: 90, message: 'Creating flashable zip...', delay: 1500 },
                { progress: 95, message: 'Generating checksums...', delay: 1000 }
            ];

            for (const step of steps) {
                updateProgress(step.progress, step.message);
                addLogEntry(`[BUILD] ${step.message}`, 'info');
                await new Promise(resolve => setTimeout(resolve, step.delay));
            }

            // Simulate final result
            const success = Math.random() > 0.1; // 90% success rate
            if (!success) {
                throw new Error('Compilation failed with exit code 1');
            }
        }

        // Setup environment
        async function setupEnvironment() {
            addLogEntry('Setting up build environment...', 'info');
            updateProgress(25, 'Installing dependencies...');
            
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            updateProgress(50, 'Configuring build tools...');
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            updateProgress(75, 'Downloading source code...');
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            updateProgress(100, 'Build environment ready!');
            addLogEntry('Build environment setup completed successfully!', 'success');
            showNotification('Build environment setup completed!', 'success');
            
            setTimeout(() => {
                updateProgress(0, 'Ready to build');
            }, 3000);
        }

        // Update progress
        function updateProgress(percentage, message) {
            document.getElementById('progressFill').style.width = percentage + '%';
            document.getElementById('progressText').textContent = message;
        }

        // Add log entry
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

        // Show notification
        function showNotification(message, type = 'info') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type}`;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 5000);
        }

        // Update statistics
        function updateStats() {
            const deviceCount = Object.keys(devices).length;
            document.getElementById('supportedDevicesCount').textContent = deviceCount;
            
            // Simulate build stats (in real implementation, these would come from backend)
            const totalBuilds = parseInt(localStorage.getItem('totalBuilds') || '0');
            const successfulBuilds = parseInt(localStorage.getItem('successfulBuilds') || '0');
            
            document.getElementById('totalBuilds').textContent = totalBuilds;
            document.getElementById('successfulBuilds').textContent = successfulBuilds;
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            initializeDeviceGrid();
            addLogEntry('Terry Recovery Builder GUI initialized', 'info');
            addLogEntry(`${Object.keys(devices).length} devices loaded into database`, 'info');
        });

        // Add custom device functionality
        function addCustomDevice() {
            const codename = document.getElementById('deviceCodename').value.trim();
            const brand = document.getElementById('deviceBrand').value.trim();
            const model = document.getElementById('deviceModel').value.trim();
            const arch = document.getElementById('deviceArch').value;
            const platform = document.getElementById('devicePlatform').value.trim();
            const androidVersion = document.getElementById('androidVersion').value;
            const treeUrl = document.getElementById('treeUrl').value.trim();
            const kernelUrl = document.getElementById('kernelUrl').value.trim();

            if (!codename || !brand || !model || !platform || !treeUrl) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }

            // Add to device list
            const newDevice = {
                [codename]: {
                    brand: brand,
                    model: model,
                    arch: arch,
                    platform: platform
                }
            };
            
            // Update devices object
            Object.assign(devices, newDevice);

            // Add device card to grid
            const deviceGrid = document.getElementById('deviceGrid');
            const deviceCard = document.createElement('div');
            deviceCard.className = 'device-card selected';
            deviceCard.dataset.device = codename;
            deviceCard.onclick = () => selectDevice(codename);
            deviceCard.innerHTML = `
                <div class="device-name">${codename} 🌳</div>
                <div class="device-info">${brand} ${model}</div>
                <div class="device-info">${arch} • ${platform}</div>
            `;
            deviceGrid.appendChild(deviceCard);

            // Select the new device
            selectDevice(codename);

            // Clear form
            document.getElementById('deviceCodename').value = '';
            document.getElementById('deviceBrand').value = '';
            document.getElementById('deviceModel').value = '';
            document.getElementById('devicePlatform').value = '';
            document.getElementById('treeUrl').value = '';
            document.getElementById('kernelUrl').value = '';

            showNotification(`Custom device ${codename} added successfully!`, 'success');
            addLogEntry(`Custom device added: ${codename} (${brand} ${model})`, 'info');
        }

        // Setup roomservice.xml functionality
        function setupRoomservice() {
            if (!selectedDevice) {
                showNotification('Please select a device first', 'error');
                return;
            }

            const recoveryType = document.querySelector('input[name="recoveryType"]:checked').value;
            
            addLogEntry(`Setting up roomservice.xml for ${selectedDevice}...`, 'info');
            updateProgress(25, 'Generating roomservice.xml...');

            // Simulate roomservice generation
            setTimeout(() => {
                updateProgress(50, 'Configuring dependencies...');
                setTimeout(() => {
                    updateProgress(75, 'Creating manifest...');
                    setTimeout(() => {
                        updateProgress(100, 'Roomservice.xml created successfully!');
                        addLogEntry(`Roomservice.xml created for ${selectedDevice} (${recoveryType})`, 'success');
                        showNotification(`Roomservice.xml created for ${selectedDevice}!`, 'success');
                        
                        setTimeout(() => {
                            updateProgress(0, 'Ready to build');
                        }, 3000);
                    }, 1000);
                }, 1000);
            }, 1000);
        }

        // Store build stats (simulated)
        window.addEventListener('beforeunload', function() {
            if (buildInProgress) {
                const totalBuilds = parseInt(localStorage.getItem('totalBuilds') || '0') + 1;
                localStorage.setItem('totalBuilds', totalBuilds);
                
                // Assume successful for demo
                const successfulBuilds = parseInt(localStorage.getItem('successfulBuilds') || '0') + 1;
                localStorage.setItem('successfulBuilds', successfulBuilds);
            }
        });

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

        // Download functionality
        let currentDownloadFile = null;

        function openDownload(recoveryType, deviceCodename, fileName, fileSize, sha256) {
            currentDownloadFile = {
                type: recoveryType,
                device: deviceCodename,
                name: fileName,
                size: fileSize,
                sha256: sha256
            };

            const downloadInfo = document.getElementById('downloadInfo');
            downloadInfo.innerHTML = `
                <div style="display: grid; grid-template-columns: auto 1fr; gap: 10px;">
                    <div><strong>Device:</strong> ${deviceCodename}</div>
                    <div><strong>Type:</strong> ${recoveryType}</div>
                    <div><strong>File:</strong> ${fileName}</div>
                    <div><strong>Size:</strong> ${fileSize}</div>
                    <div><strong>SHA256:</strong> ${sha256}</div>
                </div>
            `;

            document.getElementById('downloadModal').style.display = 'block';
        }

        function closeDownload() {
            document.getElementById('downloadModal').style.display = 'none';
            currentDownloadFile = null;
        }

        function downloadFile() {
            if (currentDownloadFile) {
                // Create demo download
                const downloadUrl = `data:application/octet-stream;base64,UkVDTw==`; // Demo content
                
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = currentDownloadFile.name;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                
                showNotification(`Downloaded ${currentDownloadFile.name}`, 'success');
                closeDownload();
            }
        }

        function copyLink() {
            if (currentDownloadFile) {
                // Copy demo link to clipboard
                const demoLink = `https://terry-bot.example/downloads/${currentDownloadFile.name}`;
                navigator.clipboard.writeText(demoLink).then(() => {
                    showNotification('Download link copied to clipboard!', 'success');
                });
            }
        }

        // Add download buttons to device cards
        function addDownloadButtons() {
            const deviceCards = document.querySelectorAll('.device-card');
            deviceCards.forEach(card => {
                const deviceCodename = card.dataset.device;
                
                // Check if device has built recoveries
                const twrpExists = Math.random() > 0.7; // Simulate existing builds
                const orangeFoxExists = Math.random() > 0.8;
                
                if (twrpExists || orangeFoxExists) {
                    const downloadDiv = document.createElement('div');
                    downloadDiv.className = 'download-buttons';
                    downloadDiv.style.marginTop = '10px';
                    downloadDiv.style.display = 'flex';
                    downloadDiv.style.gap = '5px';
                    
                    if (twrpExists) {
                        const twrpBtn = document.createElement('button');
                        twrpBtn.className = 'download-small-btn';
                        twrpBtn.innerHTML = '📥 TWRP';
                        twrpBtn.onclick = () => openDownload('TWRP', deviceCodename, `twrp_${deviceCodename}_20240113_103045.img`, '45.2 MB', 'a1b2c3d4e5f6...');
                        downloadDiv.appendChild(twrpBtn);
                    }
                    
                    if (orangeFoxExists) {
                        const ofBtn = document.createElement('button');
                        ofBtn.className = 'download-small-btn';
                        ofBtn.innerHTML = '📥 Orange Fox';
                        ofBtn.onclick = () => openDownload('Orange Fox', deviceCodename, `orange_fox_${deviceCodename}_20240113_103045.img`, '38.7 MB', 'f6e5d4c3b2a1...');
                        downloadDiv.appendChild(ofBtn);
                    }
                    
                    card.appendChild(downloadDiv);
                }
            });
        }

        // Enhanced donate modal
        function openDonate() {
            // Create enhanced donate modal if not exists
            let donateModal = document.getElementById('donateModal');
            if (!donateModal) {
                donateModal = document.createElement('div');
                donateModal.id = 'donateModal';
                donateModal.className = 'modal';
                donateModal.innerHTML = `
                    <div class="modal-content">
                        <span class="close" onclick="closeDonate()">&times;</span>
                        <h2 style="background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">❤️ Support Terry's Development</h2>
                        <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 30px;">
                            Your support helps me continue developing cutting-edge AI features and keep Terry free for everyone!
                        </p>
                        
                        <div style="margin: 30px 0;">
                            <div style="background: linear-gradient(135deg, rgba(96, 165, 250, 0.2), rgba(36, 123, 160, 0.2)); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 15px; padding: 25px; margin-bottom: 20px;">
                                <strong style="color: #60a5fa; font-size: 1.4em;">👤 Support Terry</strong><br>
                                <code style="color: #dbeafe; background: rgba(96, 165, 250, 0.1); padding: 8px 16px; border-radius: 8px;">kaynikko88@gmail.com</code><br>
                                <small>• Every contribution helps improve AI capabilities</small>
                            </div>
                            
                            <div style="background: linear-gradient(135deg, rgba(36, 123, 160, 0.2), rgba(36, 123, 160, 0.3)); border:1px solid rgba(36, 123, 160, 0.3); border-radius: 15px; padding: 25px; margin-bottom: 20px;">
                                <strong style="color: #60a5fa; font-size: 1.4em;">🚀 Premium Support</strong><br>
                                <code style="color: #dbeafe; background: rgba(36, 123, 160, 0.1); padding: 8px 16px; border-radius: 8px;">kaynikko88@gmail.com</code><br>
                                <small>• Priority support & feature requests</small>
                            </div>
                            
                            <div style="background: linear-gradient(135deg, rgba(147, 51, 234, 0.1), rgba(147, 51, 234, 0.3)); border: 1px solid rgba(147, 51, 234, 0.3); border-radius: 15px; padding: 25px;">
                                <strong style="color: #60a5fa; font-size: 1.4em;">🏆 Elite Support</strong><br>
                                <code style="color: #dbeafe; background: rgba(147, 51, 234, 0.1); padding: 8px 16px; border-radius: 8px;">kaynikko88@gmail.com</code><br>
                                <small>• Full collaboration & custom development</small>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <p style="color: #60a5fa; font-size: 1.2em; margin-bottom: 10px;">
                                Choose your support level:
                            </p>
                            <p style="color: #dbeafe; font-size: 1.1em; margin-top: 10px;">
                                Your contribution powers Terry's evolution and helps create amazing AI features for everyone!
                            </p>
                        </div>
                        
                        <button class="control-btn donate-btn" style="width: 100%; margin-top: 30px;" onclick="confirmDonation()">
                            🚀 Support Terry Development!
                        </button>
                    </div>
                `;
                document.body.appendChild(donateModal);
            }
            
            donateModal.style.display = 'block';
        }

        function closeDonate() {
            const donateModal = document.getElementById('donateModal');
            if (donateModal) {
                donateModal.style.display = 'none';
            }
        }

        function confirmDonation() {
            showNotification('Thank you for supporting Terry! 🚀', 'success');
            closeDonate();
        }
    </script>
</body>
</html>
    """
    
    # Create HTML file
    html_file = Path(__file__).parent / "terry_recovery_builder_gui.html"
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    return html_file

def main():
    """Main function"""
    print("🔧 Creating Terry Recovery Builder GUI...")
    
    # Create recovery builder GUI
    html_file = create_recovery_builder_gui()
    print(f"✅ Created Recovery Builder GUI: {html_file}")
    
    # Open in browser
    file_url = f"file://{html_file.absolute()}"
    print(f"🌐 Opening in browser: {file_url}")
    
    try:
        webbrowser.open(file_url)
        print("✅ Terry Recovery Builder GUI is now running!")
        print("🚀 Expert recovery building at your fingertips!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Please open this file manually: {html_file}")

if __name__ == "__main__":
    main()
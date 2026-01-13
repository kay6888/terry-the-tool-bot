#!/usr/bin/env python3
"""
Enhanced Terry Logo Showcase
"""

import webbrowser
from pathlib import Path

def create_logo_showcase():
    """Create showcase of all enhanced logos"""
    
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 Enhanced Terry Logo Showcase</title>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e, #0f3460);
            color: white;
            margin: 0;
            padding: 40px;
            min-height: 100vh;
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            font-size: 3.5em;
            background: linear-gradient(135deg, #ec4899, #8b5cf6, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #a78bfa;
            margin-bottom: 50px;
        }
        
        .logo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        
        .logo-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 40px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .logo-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(139, 92, 246, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s;
            opacity: 0;
        }
        
        .logo-card:hover::before {
            animation: shimmer 0.6s ease-out;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); opacity: 0; }
            50% { opacity: 1; }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); opacity: 0; }
        }
        
        .logo-card:hover {
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 25px 50px rgba(139, 92, 246, 0.3);
            border-color: rgba(139, 92, 246, 0.3);
        }
        
        .logo-card h3 {
            color: #fbbf24;
            font-size: 1.4em;
            margin-bottom: 25px;
            font-weight: 700;
        }
        
        .logo-card img {
            border-radius: 20px;
            margin: 20px 0;
            filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.4));
            transition: transform 0.4s;
        }
        
        .logo-card:hover img {
            transform: scale(1.05);
        }
        
        .logo-card p {
            color: #c4b5fd;
            margin: 20px 0;
            font-size: 1.1em;
        }
        
        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #34d399, #059669);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            margin: 10px 5px;
        }
        
        .badge.premium {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
        }
        
        .badge.ultra {
            background: linear-gradient(135deg, #ec4899, #8b5cf6);
        }
        
        .features-section {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 24px;
            padding: 50px;
            margin-top: 50px;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .feature-item {
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 16px;
            padding: 25px;
            transition: all 0.3s;
        }
        
        .feature-item:hover {
            background: rgba(139, 92, 246, 0.15);
            transform: translateY(-5px);
        }
        
        .feature-item h4 {
            color: #fbbf24;
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .feature-item p {
            color: #a78bfa;
            line-height: 1.6;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Enhanced Terry Logo Gallery</h1>
        <p class="subtitle">Professional robot design with toolbelt and thumbs up gesture</p>
        
        <div class="logo-grid">
            <div class="logo-card">
                <h3>🎨 Original Logo</h3>
                <img src="terry_logo.svg" alt="Original Terry Logo" width="160" height="160" />
                <p>Classic robot design with blue-purple theme</p>
                <div>
                    <span class="badge">Professional</span>
                    <span class="badge">Clean</span>
                </div>
            </div>
            
            <div class="logo-card">
                <h3>✨ Enhanced Logo</h3>
                <img src="terry_logo_better.svg" alt="Enhanced Terry Logo" width="160" height="160" />
                <p>Improved gradients, better proportions, and enhanced details</p>
                <div>
                    <span class="badge">Advanced</span>
                    <span class="badge premium">Premium</span>
                </div>
            </div>
            
            <div class="logo-card">
                <h3>🚀 Ultra-Premium Logo</h3>
                <img src="terry_logo_premium.svg" alt="Ultra-Premium Terry Logo" width="160" height="160" />
                <p>Ultimate design with sparkles, premium gradients, and extra details</p>
                <div>
                    <span class="badge premium">Premium</span>
                    <span class="badge ultra">Ultra</span>
                </div>
            </div>
            
            <div class="logo-card">
                <h3>🔄 Animated Logo</h3>
                <img src="terry_logo_better.svg" alt="Animated Terry Logo" width="120" height="120" 
                     style="animation: logoFloat 3s ease-in-out infinite;" />
                <p>With smooth floating animation effects</p>
                <div>
                    <span class="badge">Dynamic</span>
                    <span class="badge ultra">Interactive</span>
                </div>
            </div>
        </div>
        
        <div class="features-section">
            <h2 style="font-size: 2.5em; text-align: center; background: linear-gradient(135deg, #34d399, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px;">🎯 Design Excellence</h2>
            
            <div class="features-grid">
                <div class="feature-item">
                    <h4>🤖 Personality</h4>
                    <p>Friendly robot with glowing eyes and happy expression</p>
                </div>
                <div class="feature-item">
                    <h4>🔧 Toolbelt</h4>
                    <p>Professional wrench, screwdriver, and hammer with metallic finish</p>
                </div>
                <div class="feature-item">
                    <h4>👍 Thumbs Up</h4>
                    <p>Positive gesture with sparkles and enhanced animation</p>
                </div>
                <div class="feature-item">
                    <h4>🎨 Premium Gradients</h4>
                    <p>Advanced color schemes from purple-pink to blue</p>
                </div>
                <div class="feature-item">
                    <h4>✨ Special Effects</h4>
                    <p>Glowing elements, shadows, and shimmer animations</p>
                </div>
                <div class="feature-item">
                    <h4>🚀 Tech Feel</h4>
                    <p>Antenna with signal waves and modern aesthetics</p>
                </div>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes logoFloat {
            0% { transform: translateY(0px) rotate(0deg); }
            25% { transform: translateY(-10px) rotate(2deg); }
            50% { transform: translateY(-5px) rotate(0deg); }
            75% { transform: translateY(-15px) rotate(-2deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
    </style>
</body>
</html>
    '''
    
    return html_content

def main():
    """Create logo showcase"""
    print("🎨 Creating Enhanced Logo Showcase...")
    
    html_content = create_logo_showcase()
    html_file = Path(__file__).parent / "terry_logo_showcase_enhanced.html"
    
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Enhanced logo showcase created: {html_file}")
    
    try:
        file_url = f"file://{html_file.absolute()}"
        webbrowser.open(file_url)
        print("🌐 Opening enhanced logo showcase in browser...")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Open manually: {html_file}")

if __name__ == "__main__":
    main()
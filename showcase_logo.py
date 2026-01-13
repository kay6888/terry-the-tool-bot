#!/usr/bin/env python3
"""
Terry-the-Tool-Bot Logo Showcase
Display the amazing logo variants
"""

def showcase_logos():
    """Showcase all logo variants"""
    
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terry Logo Showcase</title>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: white;
            margin: 0;
            padding: 40px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 50px;
        }
        .logo-showcase {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        .logo-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .logo-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        }
        .logo-card h3 {
            color: #87ceeb;
            margin-bottom: 20px;
        }
        .logo-card img {
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .features {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 40px;
            margin-top: 50px;
        }
        .features h2 {
            color: #87ceeb;
            margin-bottom: 30px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .feature-item {
            background: rgba(102, 126, 234, 0.1);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #667eea;
        }
        .feature-item h4 {
            color: #ff6b35;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Terry Logo Showcase</h1>
        
        <div class="logo-showcase">
            <div class="logo-card">
                <h3>Main Logo (200x200)</h3>
                <img src="terry_logo.svg" alt="Main Terry Logo" width="150" height="150" />
                <p>Perfect for headers and main branding</p>
            </div>
            
            <div class="logo-card">
                <h3>Small Logo (60x60)</h3>
                <img src="terry_logo_small.svg" alt="Small Terry Logo" width="60" height="60" />
                <p>Perfect for favicons and compact spaces</p>
            </div>
            
            <div class="logo-card">
                <h3>Animated Logo</h3>
                <img src="terry_logo.svg" alt="Animated Terry Logo" width="120" height="120" 
                     style="animation: logoSpin 3s ease-in-out infinite;" />
                <p>With rotating animation effect</p>
            </div>
        </div>
        
        <div class="features">
            <h2>🎨 Logo Design Features</h2>
            <div class="feature-grid">
                <div class="feature-item">
                    <h4>🤖 Friendly Robot</h4>
                    <p>Approachable design with glowing eyes</p>
                </div>
                <div class="feature-item">
                    <h4>🔧 Toolbelt</h4>
                    <p>Wrench, screwdriver, and hammer tools</p>
                </div>
                <div class="feature-item">
                    <h4>👍 Thumbs Up</h4>
                    <p>Positive, confident gesture</p>
                </div>
                <div class="feature-item">
                    <h4>🎨 Gradient Colors</h4>
                    <p>Matches Terry's purple-blue theme</p>
                </div>
                <div class="feature-item">
                    <h4>📡 Antenna</h4>
                    <p>Represents AI connectivity</p>
                </div>
                <div class="feature-item">
                    <h4>✨ Professional</h4>
                    <p>Clean, modern vector design</p>
                </div>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes logoSpin {
            0% { transform: rotate(0deg); }
            25% { transform: rotate(5deg); }
            50% { transform: rotate(0deg); }
            75% { transform: rotate(-5deg); }
            100% { transform: rotate(0deg); }
        }
    </style>
</body>
</html>
    '''
    
    return html_content

def main():
    """Create logo showcase"""
    print("🎨 Creating Terry Logo Showcase...")
    
    html_file = Path(__file__).parent / "terry_logo_showcase.html"
    with open(html_file, 'w') as f:
        f.write(showcase_logos())
    
    print(f"✅ Logo showcase created: {html_file}")
    
    import webbrowser
    file_url = f"file://{html_file.absolute()}"
    webbrowser.open(file_url)
    print("🌐 Opening logo showcase in browser...")

if __name__ == "__main__":
    main()
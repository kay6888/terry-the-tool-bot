#!/usr/bin/env python3
"""
Athletic Terry vs Robust Terry Comparison
Show the evolution from robust to athletic
"""

import webbrowser
from pathlib import Path

def create_athletic_comparison():
    """Create comparison between robust and athletic Terry"""
    
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏃 Terry: Robust → Athletic Evolution</title>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
            color: #e2e8f0;
            margin: 0;
            padding: 40px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 3.5em;
            background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        
        .header p {
            font-size: 1.3em;
            color: #94a3b8;
            margin: 0;
        }
        
        .comparison-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 50px;
        }
        
        .comparison-card {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(20px);
            border: 2px solid;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .comparison-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(148, 163, 184, 0.1), transparent);
            z-index: -1;
        }
        
        .comparison-card:hover {
            transform: translateY(-10px);
        }
        
        .robust {
            border-color: #ef4444;
        }
        
        .robust:hover {
            box-shadow: 0 20px 40px rgba(239, 68, 68, 0.3);
        }
        
        .athletic {
            border-color: #60a5fa;
        }
        
        .athletic:hover {
            box-shadow: 0 20px 40px rgba(96, 165, 250, 0.3);
        }
        
        .comparison-card h2 {
            font-size: 2em;
            margin-bottom: 30px;
            font-weight: 700;
        }
        
        .robust h2 {
            color: #ef4444;
        }
        
        .athletic h2 {
            color: #60a5fa;
        }
        
        .comparison-card img {
            border-radius: 15px;
            margin: 30px 0;
            filter: drop-shadow(0 15px 30px rgba(0, 0, 0, 0.4));
            transition: transform 0.4s;
        }
        
        .comparison-card:hover img {
            transform: scale(1.05);
        }
        
        .features {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            padding: 30px;
            text-align: left;
        }
        
        .feature-item {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .feature-item:hover {
            transform: translateX(10px);
        }
        
        .robust .feature-item {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
        }
        
        .athletic .feature-item {
            background: rgba(96, 165, 250, 0.1);
            border-left: 4px solid #60a5fa;
        }
        
        .feature-title {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .improvement {
            background: rgba(34, 197, 94, 0.1);
            border-left: 4px solid #22c55e;
        }
        
        .evolution-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }
        
        .evolution-item {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(96, 165, 250, 0.3);
            transition: all 0.3s;
        }
        
        .evolution-item:hover {
            background: rgba(30, 41, 59, 0.8);
            transform: scale(1.05);
        }
        
        .evolution-item h3 {
            color: #60a5fa;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            margin: 5px;
        }
        
        .badge.robust {
            background: linear-gradient(135deg, #ef4444, #991b1b);
            color: white;
        }
        
        .badge.athletic {
            background: linear-gradient(135deg, #60a5fa, #3b82f6);
            color: white;
        }
        
        .badge.improvement {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏃 Terry Evolution: Robust → Athletic</h1>
            <p>From Heavy-Duty Industrial to Sleek Athletic Design</p>
        </div>
        
        <div class="comparison-grid">
            <!-- Robust Terry -->
            <div class="comparison-card robust">
                <h2>🏭 Robust Terry</h2>
                <img src="terry_logo_robust.svg" alt="Robust Terry" width="200" height="200" />
                <div class="features">
                    <div class="feature-item">
                        <div class="feature-title">🎨 Color Scheme</div>
                        <div>Industrial gray/black with red eyes</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-title">🏭 Body Type</div>
                        <div>Heavy-duty, armored, robust</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-title">👍 Thumbs Up</div>
                        <div>Strong, industrial gesture</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-title">🔧 Tools</div>
                        <div>Heavy equipment, wrenches, drills</div>
                    </div>
                </div>
                <div>
                    <span class="badge robust">Industrial</span>
                    <span class="badge robust">Heavy-Duty</span>
                </div>
            </div>
            
            <!-- Athletic Terry -->
            <div class="comparison-card athletic">
                <h2>🏃 Athletic Terry</h2>
                <img src="terry_logo_slim_athletic.svg" alt="Athletic Terry" width="200" height="200" />
                <div class="features">
                    <div class="feature-item">
                        <div class="feature-title">🎨 Color Scheme</div>
                        <div>Industrial gray/black with BABY BLUE accents</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-title">🏃 Body Type</div>
                        <div>Slimmer, athletic, streamlined</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-title">👍 Thumbs Up</div>
                        <div>Much better! Higher angle, enhanced details, sparkle</div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-title">🔧 Tools</div>
                        <div>Streamlined, athletic, efficient</div>
                    </div>
                </div>
                <div>
                    <span class="badge athletic">Athletic</span>
                    <span class="badge improvement">Enhanced</span>
                </div>
            </div>
        </div>
        
        <div class="evolution-grid">
            <div class="evolution-item">
                <h3>💫 Key Improvements</h3>
                <p>• Slimmer, more athletic body shape<br>
                   • Baby blue eyes and mouth for personality<br>
                   • Much better thumbs up gesture<br>
                   • Athletic sparkle effects<br>
                   • Enhanced focus and confidence</p>
            </div>
            
            <div class="evolution-item">
                <h3>🎯 Athletic Benefits</h3>
                <p>• More approachable and friendly<br>
                   • Better thumbs up shows enthusiasm<br>
                   • Baby blue adds personality<br>
                   • Sleeker, more modern look<br>
                   • Maintains industrial strength</p>
            </div>
            
            <div class="evolution-item">
                <h3>🚀 Future Ready</h3>
                <p>• Perfect for advanced AI assistant<br>
                   • Athletic represents speed and efficiency<br>
                   • Baby blue shows intelligence<br>
                   • Robust features maintain power<br>
                   • Thumb up shows positive attitude</p>
            </div>
        </div>
    </div>
</body>
</html>
    '''
    
    return html_content

def main():
    """Create athletic comparison showcase"""
    print("🏃 Creating Athletic Terry Comparison...")
    
    html_content = create_athletic_comparison()
    html_file = Path(__file__).parent / "terry_athletic_comparison.html"
    
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Athletic comparison created: {html_file}")
    
    try:
        file_url = f"file://{html_file.absolute()}"
        webbrowser.open(file_url)
        print("🌐 Opening athletic comparison in browser...")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Open manually: {html_file}")

if __name__ == "__main__":
    main()
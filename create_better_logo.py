import xml.etree.ElementTree as ET

def create_better_terry_logo():
    """Create an improved, more professional and appealing Terry logo"""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- Enhanced gradients and effects -->
    <defs>
        <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#7c3aed;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#5b21b6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#312e81;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="headGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#8b5cf6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#6d28d9;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="beltGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f97316;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#dc2626;stop-opacity:1" />
        </linearGradient>
        <radialGradient id="eyeGrad">
            <stop offset="0%" style="stop-color:#34d399;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#059669;stop-opacity:0.8" />
        </radialGradient>
        <radialGradient id="shineGrad">
            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0" />
        </radialGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="shadow">
            <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
        </filter>
    </defs>
    
    <!-- Shadow layer -->
    <ellipse cx="100" cy="195" rx="45" ry="8" fill="black" opacity="0.2"/>
    
    <!-- Robot Body (more rounded and modern) -->
    <rect x="65" y="85" width="70" height="75" rx="20" fill="url(#bodyGrad)" stroke="#4c1d95" stroke-width="2" filter="url(#shadow)"/>
    
    <!-- Body panels for depth -->
    <rect x="75" y="95" width="50" height="25" rx="10" fill="#a78bfa" opacity="0.3"/>
    <circle cx="90" cy="130" r="8" fill="#fbbf24" opacity="0.8"/>
    <circle cx="110" cy="130" r="8" fill="#fbbf24" opacity="0.8"/>
    
    <!-- Enhanced Tool Belt -->
    <rect x="60" y="115" width="80" height="15" rx="8" fill="url(#beltGrad)" stroke="#991b1b" stroke-width="2" filter="url(#shadow)"/>
    
    <!-- Belt details -->
    <rect x="70" y="120" width="15" height="5" rx="2" fill="#fbbf24"/>
    <rect x="115" y="120" width="15" height="5" rx="2" fill="#fbbf24"/>
    
    <!-- Enhanced Tools on belt -->
    <!-- Premium Wrench -->
    <g transform="translate(68, 118)" filter="url(#shadow)">
        <rect x="0" y="0" width="5" height="10" rx="2" fill="#94a3b8" stroke="#64748b" stroke-width="1"/>
        <circle cx="2.5" cy="12" r="3" fill="#fbbf24" stroke="#f59e0b" stroke-width="1"/>
        <rect x="1" y="-2" width="3" height="2" fill="#64748b"/>
    </g>
    
    <!-- Digital Screwdriver -->
    <g transform="translate(88, 118)" filter="url(#shadow)">
        <rect x="0" y="0" width="3" height="9" rx="1" fill="#f59e0b" stroke="#d97706" stroke-width="1"/>
        <rect x="-1" y="9" width="5" height="2" rx="1" fill="#f59e0b"/>
        <circle cx="1.5" cy="-1" r="1" fill="#34d399"/>
    </g>
    
    <!-- High-Tech Hammer -->
    <g transform="translate(108, 118)" filter="url(#shadow)">
        <rect x="0" y="0" width="4" height="7" rx="1" fill="#64748b" stroke="#475569" stroke-width="1"/>
        <rect x="-2" y="7" width="8" height="4" rx="1" fill="#dc2626"/>
        <rect x="0" y="11" width="4" height="1" fill="#dc2626"/>
    </g>
    
    <!-- Robot Head (more sophisticated) -->
    <rect x="70" y="45" width="60" height="45" rx="15" fill="url(#headGrad)" stroke="#4c1d95" stroke-width="2" filter="url(#shadow)"/>
    
    <!-- Head panel for depth -->
    <rect x="80" y="55" width="40" height="20" rx="8" fill="#a78bfa" opacity="0.2"/>
    
    <!-- Enhanced Robot Eyes with more personality -->
    <!-- Left eye -->
    <ellipse cx="85" cy="65" rx="10" ry="8" fill="white" stroke="#4c1d95" stroke-width="2"/>
    <ellipse cx="85" cy="65" rx="7" ry="6" fill="url(#eyeGrad)" filter="url(#glow)"/>
    <ellipse cx="87" cy="63" rx="3" ry="2" fill="white"/>
    <ellipse cx="83" cy="67" rx="2" ry="1" fill="white" opacity="0.6"/>
    
    <!-- Right eye -->
    <ellipse cx="115" cy="65" rx="10" ry="8" fill="white" stroke="#4c1d95" stroke-width="2"/>
    <ellipse cx="115" cy="65" rx="7" ry="6" fill="url(#eyeGrad)" filter="url(#glow)"/>
    <ellipse cx="117" cy="63" rx="3" ry="2" fill="white"/>
    <ellipse cx="113" cy="67" rx="2" ry="1" fill="white" opacity="0.6"/>
    
    <!-- Enhanced expression (more personality) -->
    <path d="M 83 78 Q 100 85 117 78" stroke="#4c1d95" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- Small detail lines -->
    <path d="M 90 80 Q 100 82 110 80" stroke="#a78bfa" stroke-width="1" fill="none" opacity="0.5" stroke-linecap="round"/>
    
    <!-- Left Arm (more detailed) -->
    <rect x="45" y="95" width="20" height="14" rx="7" fill="url(#bodyGrad)" stroke="#4c1d95" stroke-width="2" filter="url(#shadow)"/>
    <!-- Arm joint -->
    <circle cx="65" cy="102" r="4" fill="#a78bfa" stroke="#6d28d9" stroke-width="1"/>
    
    <!-- Right Arm with Epic Thumbs Up! -->
    <g transform="translate(135, 95)" filter="url(#shadow)">
        <!-- Upper arm -->
        <rect x="0" y="0" width="22" height="14" rx="7" fill="url(#bodyGrad)" stroke="#4c1d95" stroke-width="2"/>
        <!-- Arm joint -->
        <circle cx="22" cy="7" r="4" fill="#a78bfa" stroke="#6d28d9" stroke-width="1"/>
        
        <!-- Hand (more detailed) -->
        <ellipse cx="30" cy="7" rx="10" ry="12" fill="#8b5cf6" stroke="#4c1d95" stroke-width="2"/>
        <!-- Hand details -->
        <ellipse cx="28" cy="7" rx="4" ry="6" fill="#a78bfa" opacity="0.5"/>
        
        <!-- Epic Thumbs Up! (more impressive) -->
        <g transform="translate(38, 0) rotate(-45 0 0)">
            <ellipse cx="0" cy="-3" rx="7" ry="10" fill="#8b5cf6" stroke="#4c1d95" stroke-width="2"/>
            <!-- Thumb nail and details -->
            <ellipse cx="0" cy="-10" rx="3" ry="2" fill="#fbbf24" stroke="#f59e0b" stroke-width="1"/>
            <!-- Thumb highlight -->
            <ellipse cx="2" cy="-5" rx="4" ry="6" fill="#c4b5fd" opacity="0.4"/>
            
            <!-- Shine on thumb -->
            <ellipse cx="-1" cy="-6" rx="2" ry="3" fill="white" opacity="0.6"/>
        </g>
    </g>
    
    <!-- Enhanced Antenna with more tech feel -->
    <line x1="100" y1="45" x2="100" y2="32" stroke="#4c1d95" stroke-width="4" stroke-linecap="round"/>
    <!-- Antenna base -->
    <circle cx="100" cy="45" r="3" fill="#8b5cf6" stroke="#4c1d95" stroke-width="1"/>
    <!-- Antenna tip with glow -->
    <g filter="url(#glow)">
        <circle cx="100" cy="30" r="6" fill="#34d399"/>
        <circle cx="100" cy="30" r="4" fill="#10b981"/>
        <circle cx="100" cy="30" r="2" fill="white"/>
    </g>
    <!-- Signal waves -->
    <circle cx="100" cy="30" r="10" fill="none" stroke="#34d399" stroke-width="1" opacity="0.3"/>
    <circle cx="100" cy="30" r="15" fill="none" stroke="#34d399" stroke-width="1" opacity="0.2"/>
    
    <!-- Robot Legs (more stylish) -->
    <rect x="75" y="160" width="18" height="30" rx="9" fill="url(#bodyGrad)" stroke="#4c1d95" stroke-width="2" filter="url(#shadow)"/>
    <rect x="107" y="160" width="18" height="30" rx="9" fill="url(#bodyGrad)" stroke="#4c1d95" stroke-width="2" filter="url(#shadow)"/>
    
    <!-- Leg joints -->
    <circle cx="84" cy="175" r="3" fill="#a78bfa" stroke="#6d28d9" stroke-width="1"/>
    <circle cx="116" cy="175" r="3" fill="#a78bfa" stroke="#6d28d9" stroke-width="1"/>
    
    <!-- Enhanced Robot Feet (more modern) -->
    <g filter="url(#shadow)">
        <ellipse cx="84" cy="193" rx="12" ry="8" fill="#6d28d9" stroke="#4c1d95" stroke-width="2"/>
        <ellipse cx="116" cy="193" rx="12" ry="8" fill="#6d28d9" stroke="#4c1d95" stroke-width="2"/>
        <!-- Foot details -->
        <ellipse cx="84" cy="193" rx="6" ry="3" fill="#a78bfa" opacity="0.4"/>
        <ellipse cx="116" cy="193" rx="6" ry="3" fill="#a78bfa" opacity="0.4"/>
    </g>
    
    <!-- Enhanced shine effects -->
    <ellipse cx="85" cy="100" rx="18" ry="10" fill="url(#shineGrad)" opacity="0.6"/>
    <ellipse cx="115" cy="120" rx="12" ry="8" fill="url(#shineGrad)" opacity="0.4"/>
    <ellipse cx="100" cy="65" rx="15" ry="8" fill="url(#shineGrad)" opacity="0.3"/>
</svg>'''
    
    return svg_content

def create_ultra_premium_logo():
    """Create an ultra-premium version with extra details"""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="300" height="300" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- Ultra-premium gradients -->
    <defs>
        <linearGradient id="premiumBody" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#ec4899;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#8b5cf6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
        </linearGradient>
        <radialGradient id="premiumEye">
            <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:0.9" />
        </radialGradient>
        <filter id="premiumGlow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Premium robot with enhanced details -->
    <g transform="scale(1.2) translate(-20, -15)">
        <!-- All the same elements as above but with premium gradients -->
        <rect x="65" y="85" width="70" height="75" rx="20" fill="url(#premiumBody)" stroke="#4c1d95" stroke-width="3" filter="url(#premiumGlow)"/>
        
        <!-- Ultra-toolbelt with premium finish -->
        <rect x="60" y="115" width="80" height="15" rx="8" fill="linear-gradient(135deg, #f59e0b, #dc2626)" stroke="#991b1b" stroke-width="3"/>
        
        <!-- Enhanced tools with metallic finish -->
        <g transform="translate(68, 118)">
            <rect x="0" y="0" width="5" height="10" rx="2" fill="linear-gradient(135deg, #fbbf24, #f59e0b)"/>
            <circle cx="2.5" cy="12" r="3" fill="#34d399"/>
        </g>
        
        <!-- Premium head with extra shine -->
        <rect x="70" y="45" width="60" height="45" rx="15" fill="linear-gradient(135deg, #a78bfa, #7c3aed)" stroke="#4c1d95" stroke-width="3"/>
        
        <!-- Ultra-detailed eyes with star-shaped pupils -->
        <ellipse cx="85" cy="65" rx="10" ry="8" fill="white" stroke="#4c1d95" stroke-width="3"/>
        <ellipse cx="85" cy="65" rx="7" ry="6" fill="url(#premiumEye)" filter="url(#premiumGlow)"/>
        <!-- Star-shaped highlight -->
        <path d="M 87 63 L 87.5 64 L 88 63 L 87.5 62 L 87 63 Z" fill="white"/>
        
        <ellipse cx="115" cy="65" rx="10" ry="8" fill="white" stroke="#4c1d95" stroke-width="3"/>
        <ellipse cx="115" cy="65" rx="7" ry="6" fill="url(#premiumEye)" filter="url(#premiumGlow)"/>
        <path d="M 117 63 L 117.5 64 L 118 63 L 117.5 62 L 117 63 Z" fill="white"/>
        
        <!-- Super happy expression -->
        <path d="M 83 78 Q 100 87 117 78" stroke="#4c1d95" stroke-width="3" fill="none" stroke-linecap="round"/>
        
        <!-- Enhanced thumbs up with sparkles -->
        <g transform="translate(135, 95)">
            <rect x="0" y="0" width="22" height="14" rx="7" fill="url(#premiumBody)" stroke="#4c1d95" stroke-width="3"/>
            <ellipse cx="30" cy="7" rx="10" ry="12" fill="#a78bfa" stroke="#4c1d95" stroke-width="3"/>
            
            <!-- Super thumbs up -->
            <g transform="translate(38, 0) rotate(-45 0 0)">
                <ellipse cx="0" cy="-3" rx="8" ry="12" fill="#fbbf24" stroke="#f59e0b" stroke-width="3"/>
                <ellipse cx="0" cy="-10" rx="4" ry="3" fill="#34d399"/>
                <!-- Sparkles around thumb -->
                <circle cx="-5" cy="-8" r="1.5" fill="#fbbf24" opacity="0.8"/>
                <circle cx="5" cy="-12" r="1" fill="#34d399" opacity="0.6"/>
                <circle cx="8" cy="-5" r="0.8" fill="#fbbf24" opacity="0.9"/>
            </g>
        </g>
        
        <!-- Premium antenna with dual lights -->
        <line x1="100" y1="45" x2="100" y2="30" stroke="#4c1d95" stroke-width="5" stroke-linecap="round"/>
        <circle cx="100" cy="30" r="8" fill="#fbbf24" filter="url(#premiumGlow)"/>
        <circle cx="100" cy="30" r="3" fill="white"/>
        <!-- Second antenna light -->
        <circle cx="110" cy="35" r="3" fill="#34d399" filter="url(#premiumGlow)"/>
        
        <!-- Premium legs with enhanced design -->
        <rect x="75" y="160" width="18" height="30" rx="9" fill="url(#premiumBody)" stroke="#4c1d95" stroke-width="3"/>
        <rect x="107" y="160" width="18" height="30" rx="9" fill="url(#premiumBody)" stroke="#4c1d95" stroke-width="3"/>
        
        <!-- Premium feet -->
        <ellipse cx="84" cy="193" rx="12" ry="8" fill="#8b5cf6" stroke="#4c1d95" stroke-width="3"/>
        <ellipse cx="116" cy="193" rx="12" ry="8" fill="#8b5cf6" stroke="#4c1d95" stroke-width="3"/>
    </g>
</svg>'''
    
    return svg_content

def main():
    """Create enhanced Terry logos"""
    print("🎨 Creating Better-Looking Terry Logo...")
    
    # Enhanced main logo
    better_logo = create_better_terry_logo()
    with open('terry_logo_better.svg', 'w') as f:
        f.write(better_logo)
    
    # Ultra-premium logo
    premium_logo = create_ultra_premium_logo()
    with open('terry_logo_premium.svg', 'w') as f:
        f.write(premium_logo)
    
    print("✅ Enhanced logos created successfully!")
    print("📁 Files created:")
    print("  • terry_logo_better.svg - Enhanced professional design")
    print("  • terry_logo_premium.svg - Ultra-premium version")
    print("\n🚀 Enhanced Features:")
    print("  • Better proportions and styling")
    print("  • Enhanced gradients (purple-pink-blue)")
    print("  • More detailed tools with metallic finish")
    print("  • Star-shaped eye highlights")
    print("  • More expressive happy face")
    print("  • Improved thumbs up with sparkles")
    print("  • Enhanced depth and shadows")
    print("  • Premium antenna with signal effects")
    print("  • Professional glass-morphism effects")
    
    # Update ultra-modern GUI with new logo
    print("\n🔄 Updating ultra-modern GUI with enhanced logo...")
    
    # Update the ultra-modern GUI to use the better logo
    import os
    from pathlib import Path
    
    gui_file = Path(__file__).parent / "terry_gui_ultra.py"
    if gui_file.exists():
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Update logo references
        content = content.replace('terry_logo.svg', 'terry_logo_better.svg')
        content = content.replace('terry_logo_small.svg', 'terry_logo_better.svg')
        
        with open(gui_file, 'w') as f:
            f.write(content)
        
        print("✅ Ultra-modern GUI updated with enhanced logo!")

if __name__ == "__main__":
    main()
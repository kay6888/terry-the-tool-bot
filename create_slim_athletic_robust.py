#!/usr/bin/env python3
"""
Slimmer Athletic Terry with Better Thumbs Up
Robust but sleek with baby blue accents
"""

def create_slim_athletic_robust_logo():
    """Create slimmer, athletic robust Terry with better thumbs up and baby blue features"""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- Athletic gradients with baby blue -->
    <defs>
        <linearGradient id="slimBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#374151;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#1f2937;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="slimHeadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#475569;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#1f2937;stop-opacity:1" />
        </linearGradient>
        <radialGradient id="babyBlueEye">
            <stop offset="0%" style="stop-color:#60a5fa;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:0.8" />
        </radialGradient>
        <radialGradient id="babyBlueMouth">
            <stop offset="0%" style="stop-color:#60a5fa;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2563eb;stop-opacity:0.9" />
        </radialGradient>
        <linearGradient id="athleticBelt">
            <stop offset="0%" style="stop-color:#ea580c;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#c2410c;stop-opacity:1" />
        </linearGradient>
        <filter id="athleticShadow">
            <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
        </filter>
        <filter id="babyBlueGlow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Ground shadow -->
    <ellipse cx="100" cy="195" rx="45" ry="8" fill="#000000" opacity="0.25"/>
    
    <!-- Slimmer Robot Body -->
    <rect x="65" y="92" width="70" height="70" rx="18" fill="url(#slimBodyGrad)" stroke="#000000" stroke-width="2.5" filter="url(#athleticShadow)"/>
    
    <!-- Athletic body panels -->
    <rect x="75" y="102" width="50" height="20" rx="8" fill="#374151" opacity="0.4"/>
    <rect x="80" y="132" width="40" height="2" fill="#6b7280"/>
    
    <!-- Slimmer ventilation slots -->
    <g opacity="0.6">
        <rect x="68" y="107" width="1.5" height="12" rx="0.5" fill="#111827"/>
        <rect x="130.5" y="107" width="1.5" height="12" rx="0.5" fill="#111827"/>
        <rect x="68" y="125" width="1.5" height="12" rx="0.5" fill="#111827"/>
        <rect x="130.5" y="125" width="1.5" height="12" rx="0.5" fill="#111827"/>
    </g>
    
    <!-- Athletic Tool Belt (slimmer) -->
    <rect x="58" y="122" width="84" height="15" rx="6" fill="url(#athleticBelt)" stroke="#000000" stroke-width="1.5" filter="url(#athleticShadow)"/>
    
    <!-- Belt details -->
    <circle cx="72" cy="129.5" r="1.5" fill="#000000"/>
    <circle cx="100" cy="129.5" r="1.5" fill="#000000"/>
    <circle cx="128" cy="129.5" r="1.5" fill="#000000"/>
    
    <!-- Athletic Tools (more streamlined) -->
    <!-- Sleek Wrench -->
    <g transform="translate(68, 119)" filter="url(#athleticShadow)">
        <rect x="0" y="0" width="5" height="9" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <circle cx="2.5" cy="11" r="3" fill="#000000"/>
        <rect x="1" y="-1" width="3" height="2" rx="0.5" fill="#6b7280"/>
    </g>
    
    <!-- Streamlined Drill -->
    <g transform="translate(92, 119)" filter="url(#athleticShadow)">
        <rect x="0" y="0" width="3.5" height="8" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <rect x="-1.5" y="8" width="6.5" height="2.5" rx="1" fill="#ea580c"/>
        <circle cx="1.75" cy="-1" r="1.5" fill="#60a5fa" filter="url(#babyBlueGlow)"/>
    </g>
    
    <!-- Athletic Hammer -->
    <g transform="translate(116, 119)" filter="url(#athleticShadow)">
        <rect x="0" y="0" width="4" height="7" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <rect x="-2" y="7" width="8" height="3" rx="1" fill="#374151"/>
        <rect x="0" y="10" width="4" height="1.5" fill="#374151"/>
    </g>
    
    <!-- Slimmer Athletic Head -->
    <rect x="72" y="52" width="56" height="42" rx="12" fill="url(#slimHeadGrad)" stroke="#000000" stroke-width="2.5" filter="url(#athleticShadow)"/>
    
    <!-- Head armor (more athletic) -->
    <rect x="80" y="58" width="40" height="18" rx="6" fill="#475569" opacity="0.5"/>
    <rect x="88" y="62" width="24" height="8" rx="3" fill="#374151" opacity="0.3"/>
    
    <!-- Baby Blue Athletic Eyes -->
    <!-- Left eye (more focused) -->
    <ellipse cx="85" cy="66" rx="9" ry="7" fill="#000000"/>
    <ellipse cx="85" cy="66" rx="6" ry="5" fill="url(#babyBlueEye)" filter="url(#babyBlueGlow)"/>
    <rect x="84" y="64" width="2" height="3" rx="0.5" fill="#000000"/>
    <!-- Eye highlight -->
    <ellipse cx="86" cy="65" rx="2" ry="1.5" fill="#93c5fd"/>
    <ellipse cx="83" cy="67" rx="1" ry="0.5" fill="#dbeafe" opacity="0.8"/>
    
    <!-- Right eye (more focused) -->
    <ellipse cx="115" cy="66" rx="9" ry="7" fill="#000000"/>
    <ellipse cx="115" cy="66" rx="6" ry="5" fill="url(#babyBlueEye)" filter="url(#babyBlueGlow)"/>
    <rect x="114" y="64" width="2" height="3" rx="0.5" fill="#000000"/>
    <!-- Eye highlight -->
    <ellipse cx="116" cy="65" rx="2" ry="1.5" fill="#93c5fd"/>
    <ellipse cx="113" cy="67" rx="1" ry="0.5" fill="#dbeafe" opacity="0.8"/>
    
    <!-- Baby Blue Athletic Mouth (more expressive) -->
    <rect x="88" y="78" width="24" height="6" rx="3" fill="#000000"/>
    <rect x="90" y="79.5" width="20" height="3" rx="1.5" fill="url(#babyBlueMouth)" filter="url(#babyBlueGlow)"/>
    
    <!-- Athletic mouth curve (more confident) -->
    <path d="M 92 81 Q 100 83 108 81" stroke="#60a5fa" stroke-width="1" fill="none" stroke-linecap="round" opacity="0.6"/>
    
    <!-- Baby Blue status light -->
    <circle cx="100" cy="81" r="1" fill="#60a5fa" filter="url(#babyBlueGlow)"/>
    
    <!-- Athletic Left Arm (slimmer) -->
    <rect x="40" y="102" width="25" height="14" rx="7" fill="url(#slimBodyGrad)" stroke="#000000" stroke-width="2.5" filter="url(#athleticShadow)"/>
    <!-- Arm joint -->
    <circle cx="65" cy="109" r="2.5" fill="#6b7280" stroke="#000000" stroke-width="1"/>
    
    <!-- Athletic Right Arm with EPIC Thumbs Up! (much better) -->
    <g transform="translate(135, 102)" filter="url(#athleticShadow)">
        <!-- Slimmer upper arm -->
        <rect x="0" y="0" width="22" height="14" rx="7" fill="url(#slimBodyGrad)" stroke="#000000" stroke-width="2.5"/>
        <!-- Athletic joint -->
        <rect x="22" y="5" width="4" height="4" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <circle cx="24" cy="7" r="1.5" fill="#000000"/>
        
        <!-- Athletic Hand (slimmer) -->
        <ellipse cx="30" cy="7" rx="9" ry="11" fill="#475569" stroke="#000000" stroke-width="2"/>
        <!-- Hand details -->
        <rect x="25" y="4" width="8" height="4" rx="2" fill="#374151" opacity="0.4"/>
        <circle cx="27" cy="6" r="1.5" fill="#6b7280"/>
        
        <!-- EPIC Thumbs Up! (much better) -->
        <g transform="translate(37, 0) rotate(-35 0 0)">
            <!-- Enhanced thumb shape -->
            <ellipse cx="0" cy="-4" rx="7" ry="11" fill="#475569" stroke="#000000" stroke-width="2"/>
            
            <!-- Thumb armor plates -->
            <rect x="-1.5" y="-7" width="3" height="7" rx="1" fill="#374151" opacity="0.6"/>
            
            <!-- Thumb joint (more athletic) -->
            <circle cx="0" cy="-4" r="1.5" fill="#6b7280" stroke="#000000" stroke-width="1"/>
            
            <!-- Enhanced thumb tip -->
            <ellipse cx="1" cy="-13" rx="3" ry="4" fill="#60a5fa" filter="url(#babyBlueGlow)"/>
            
            <!-- Thumb highlights -->
            <ellipse cx="-0.5" cy="-8" rx="2" ry="4" fill="#93c5fd" opacity="0.7"/>
            <ellipse cx="1.5" cy="-11" rx="1.5" ry="2" fill="#dbeafe" opacity="0.8"/>
            
            <!-- Athletic sparkle on thumb -->
            <g transform="translate(2, -14)">
                <circle cx="0" cy="0" r="1" fill="#60a5fa" opacity="0.9"/>
                <circle cx="0" cy="0" r="0.5" fill="#dbeafe"/>
                <!-- Sparkle rays -->
                <line x1="0" y1="-2" x2="0" y2="-3" stroke="#dbeafe" stroke-width="0.5"/>
                <line x1="-2" y1="0" x2="-3" y2="0" stroke="#dbeafe" stroke-width="0.5"/>
                <line x1="2" y1="0" x2="3" y2="0" stroke="#dbeafe" stroke-width="0.5"/>
                <line x1="0" y1="2" x2="0" y2="3" stroke="#dbeafe" stroke-width="0.5"/>
            </g>
        </g>
    </g>
    
    <!-- Athletic Antenna Array -->
    <line x1="100" y1="52" x2="100" y2="38" stroke="#000000" stroke-width="3" stroke-linecap="round"/>
    <circle cx="100" cy="52" r="3" fill="#6b7280" stroke="#000000" stroke-width="1.5"/>
    
    <!-- Baby blue antenna lights -->
    <g filter="url(#babyBlueGlow)">
        <circle cx="100" cy="36" r="4" fill="#60a5fa"/>
        <circle cx="100" cy="36" r="2.5" fill="#3b82f6"/>
        <circle cx="100" cy="36" r="1" fill="#dbeafe"/>
        
        <!-- Secondary antenna light -->
        <circle cx="108" cy="40" r="1.5" fill="#60a5fa"/>
    </g>
    
    <!-- Athletic signal waves -->
    <circle cx="100" cy="36" r="10" fill="none" stroke="#60a5fa" stroke-width="0.8" opacity="0.3"/>
    <circle cx="100" cy="36" r="15" fill="none" stroke="#60a5fa" stroke-width="0.5" opacity="0.2"/>
    
    <!-- Athletic Legs (slimmer) -->
    <rect x="77" y="162" width="18" height="28" rx="9" fill="url(#slimBodyGrad)" stroke="#000000" stroke-width="2.5" filter="url(#athleticShadow)"/>
    <rect x="105" y="162" width="18" height="28" rx="9" fill="url(#slimBodyGrad)" stroke="#000000" stroke-width="2.5" filter="url(#athleticShadow)"/>
    
    <!-- Athletic leg armor and joints -->
    <rect x="82" y="172" width="8" height="12" rx="2" fill="#6b7280"/>
    <rect x="110" y="172" width="8" height="12" rx="2" fill="#6b7280"/>
    <circle cx="86" cy="176" r="1.5" fill="#000000"/>
    <circle cx="114" cy="176" r="1.5" fill="#000000"/>
    
    <!-- Athletic Robot Feet (sleeker) -->
    <g filter="url(#athleticShadow)">
        <rect x="72" y="187" width="28" height="6" rx="3" fill="#1f2937" stroke="#000000" stroke-width="2"/>
        <rect x="100" y="187" width="28" height="6" rx="3" fill="#1f2937" stroke="#000000" stroke-width="2"/>
        <!-- Athletic tread details -->
        <rect x="74" y="190" width="24" height="1.5" fill="#000000"/>
        <rect x="102" y="190" width="24" height="1.5" fill="#000000"/>
    </g>
</svg>'''
    
    return svg_content

def main():
    """Create slimmer athletic robust Terry"""
    print("🏃 Creating Slimmer Athletic Terry Logo...")
    
    slimmer_logo = create_slim_athletic_robust_logo()
    with open('terry_logo_slim_athletic.svg', 'w') as f:
        f.write(slimmer_logo)
    
    print("✅ Slimmer Athletic Terry created successfully!")
    print("📁 File created: terry_logo_slim_athletic.svg")
    print("\n🏃 Athletic Features:")
    print("  • Slimmer, athletic body design")
    print("  • Baby blue eyes with better focus")
    print("  • Baby blue mouth with expressive curve")
    print("  • Much better thumbs up gesture")
    print("    • Higher angle (-35° for more enthusiasm)")
    print("    • Enhanced thumb shape and details")
    print("    • Athletic sparkle on thumb")
    print("    • Baby blue thumb tip")
    print("    • Armor plates and joints")
    print("  • Athletic antenna with baby blue lights")
    print("  • Sleeker armor and ventilation")
    print("  • Streamlined tools")
    print("  • More focused, confident expression")
    print("  • Maintains robust industrial feel")
    
    # Update GUI to use slimmer athletic logo
    print("\n🔄 Updating ultra-modern GUI with slimmer athletic design...")
    
    from pathlib import Path
    gui_file = Path(__file__).parent / "terry_gui_ultra.py"
    if gui_file.exists():
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Update to use slimmer athletic logo
        content = content.replace('terry_logo_robust.svg', 'terry_logo_slim_athletic.svg')
        
        # Ensure baby blue colors are maintained in GUI
        # The GUI already uses baby blue (#87ceeb) which matches perfectly
        
        with open(gui_file, 'w') as f:
            f.write(content)
        
        print("✅ Ultra-modern GUI updated with slimmer athletic Terry!")

if __name__ == "__main__":
    main()
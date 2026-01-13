#!/usr/bin/env python3
"""
Leaner Terry - Less Fat, Same Head, Athletic Features
"""

def create_leaner_terry_logo():
    """Create leaner Terry with same head but thinner body"""
    
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- Lean gradients with baby blue -->
    <defs>
        <linearGradient id="leanBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#374151;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#1f2937;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="sameHeadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
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
        <linearGradient id="leanBelt">
            <stop offset="0%" style="stop-color:#ea580c;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#c2410c;stop-opacity:1" />
        </linearGradient>
        <filter id="leanShadow">
            <feDropShadow dx="2" dy="2" stdDeviation="2.5" flood-opacity="0.25"/>
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
    <ellipse cx="100" cy="195" rx="40" ry="6" fill="#000000" opacity="0.2"/>
    
    <!-- Leaner Robot Body (much less fat) -->
    <rect x="70" y="95" width="60" height="60" rx="15" fill="url(#leanBodyGrad)" stroke="#000000" stroke-width="2" filter="url(#leanShadow)"/>
    
    <!-- Lean body panels -->
    <rect x="78" y="102" width="44" height="16" rx="6" fill="#374151" opacity="0.4"/>
    <rect x="82" y="128" width="36" height="2" fill="#6b7280"/>
    
    <!-- Slimmer ventilation slots -->
    <g opacity="0.5">
        <rect x="71" y="107" width="1" height="10" rx="0.5" fill="#111827"/>
        <rect x="128" y="107" width="1" height="10" rx="0.5" fill="#111827"/>
        <rect x="71" y="123" width="1" height="10" rx="0.5" fill="#111827"/>
        <rect x="128" y="123" width="1" height="10" rx="0.5" fill="#111827"/>
    </g>
    
    <!-- Leaner Tool Belt -->
    <rect x="62" y="120" width="76" height="12" rx="5" fill="url(#leanBelt)" stroke="#000000" stroke-width="1.5" filter="url(#leanShadow)"/>
    
    <!-- Belt details -->
    <circle cx="74" cy="126" r="1.2" fill="#000000"/>
    <circle cx="100" cy="126" r="1.2" fill="#000000"/>
    <circle cx="126" cy="126" r="1.2" fill="#000000"/>
    
    <!-- Leaner Tools -->
    <!-- Streamlined Wrench -->
    <g transform="translate(68, 117)" filter="url(#leanShadow)">
        <rect x="0" y="0" width="4.5" height="8" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <circle cx="2.25" cy="10" r="2.5" fill="#000000"/>
        <rect x="1" y="-1" width="2.5" height="1.5" rx="0.5" fill="#6b7280"/>
    </g>
    
    <!-- Lean Drill -->
    <g transform="translate(92, 117)" filter="url(#leanShadow)">
        <rect x="0" y="0" width="3" height="7" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <rect x="-1" y="7" width="5" height="2" rx="1" fill="#ea580c"/>
        <circle cx="1.5" cy="-1" r="1.2" fill="#60a5fa" filter="url(#babyBlueGlow)"/>
    </g>
    
    <!-- Lean Hammer -->
    <g transform="translate(115, 117)" filter="url(#leanShadow)">
        <rect x="0" y="0" width="3.5" height="6" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <rect x="-1.5" y="6" width="6.5" height="2.5" rx="1" fill="#374151"/>
        <rect x="0" y="8.5" width="3.5" height="1.2" fill="#374151"/>
    </g>
    
    <!-- SAME SIZE HEAD (unchanged) -->
    <rect x="72" y="52" width="56" height="42" rx="12" fill="url(#sameHeadGrad)" stroke="#000000" stroke-width="2.5" filter="url(#leanShadow)"/>
    
    <!-- Head armor (unchanged) -->
    <rect x="80" y="58" width="40" height="18" rx="6" fill="#475569" opacity="0.5"/>
    <rect x="88" y="62" width="24" height="8" rx="3" fill="#374151" opacity="0.3"/>
    
    <!-- Baby Blue Eyes (unchanged position and size) -->
    <!-- Left eye -->
    <ellipse cx="85" cy="66" rx="9" ry="7" fill="#000000"/>
    <ellipse cx="85" cy="66" rx="6" ry="5" fill="url(#babyBlueEye)" filter="url(#babyBlueGlow)"/>
    <rect x="84" y="64" width="2" height="3" rx="0.5" fill="#000000"/>
    <!-- Eye highlight -->
    <ellipse cx="86" cy="65" rx="2" ry="1.5" fill="#93c5fd"/>
    <ellipse cx="83" cy="67" rx="1" ry="0.5" fill="#dbeafe" opacity="0.8"/>
    
    <!-- Right eye -->
    <ellipse cx="115" cy="66" rx="9" ry="7" fill="#000000"/>
    <ellipse cx="115" cy="66" rx="6" ry="5" fill="url(#babyBlueEye)" filter="url(#babyBlueGlow)"/>
    <rect x="114" y="64" width="2" height="3" rx="0.5" fill="#000000"/>
    <!-- Eye highlight -->
    <ellipse cx="116" cy="65" rx="2" ry="1.5" fill="#93c5fd"/>
    <ellipse cx="113" cy="67" rx="1" ry="0.5" fill="#dbeafe" opacity="0.8"/>
    
    <!-- Baby Blue Mouth (unchanged) -->
    <rect x="88" y="78" width="24" height="6" rx="3" fill="#000000"/>
    <rect x="90" y="79.5" width="20" height="3" rx="1.5" fill="url(#babyBlueMouth)" filter="url(#babyBlueGlow)"/>
    
    <!-- Athletic mouth curve (unchanged) -->
    <path d="M 92 81 Q 100 83 108 81" stroke="#60a5fa" stroke-width="1" fill="none" stroke-linecap="round" opacity="0.6"/>
    
    <!-- Baby Blue status light (unchanged) -->
    <circle cx="100" cy="81" r="1" fill="#60a5fa" filter="url(#babyBlueGlow)"/>
    
    <!-- Leaner Left Arm (thinner) -->
    <rect x="45" y="105" width="25" height="12" rx="6" fill="url(#leanBodyGrad)" stroke="#000000" stroke-width="2" filter="url(#leanShadow)"/>
    <!-- Arm joint -->
    <circle cx="70" cy="111" r="2" fill="#6b7280" stroke="#000000" stroke-width="1"/>
    
    <!-- Leaner Right Arm with SAME GREAT Thumbs Up! -->
    <g transform="translate(130, 105)" filter="url(#leanShadow)">
        <!-- Leaner upper arm -->
        <rect x="0" y="0" width="20" height="12" rx="6" fill="url(#leanBodyGrad)" stroke="#000000" stroke-width="2"/>
        <!-- Athletic joint -->
        <rect x="20" y="5" width="3.5" height="3" rx="1" fill="#6b7280" stroke="#000000" stroke-width="1"/>
        <circle cx="21.75" cy="6.5" r="1.2" fill="#000000"/>
        
        <!-- Leaner hand -->
        <ellipse cx="27" cy="6" rx="7" ry="9" fill="#475569" stroke="#000000" stroke-width="2"/>
        <!-- Hand details -->
        <rect x="23" y="3.5" width="6" height="3" rx="1.5" fill="#374151" opacity="0.4"/>
        <circle cx="25" cy="5" r="1.2" fill="#6b7280"/>
        
        <!-- SAME GREAT THUMBS UP! (unchanged excellence) -->
        <g transform="translate(33, 0) rotate(-35 0 0)">
            <!-- Enhanced thumb shape -->
            <ellipse cx="0" cy="-4" rx="6" ry="9.5" fill="#475569" stroke="#000000" stroke-width="2"/>
            
            <!-- Thumb armor plates -->
            <rect x="-1.5" y="-6" width="2.5" height="6" rx="1" fill="#374151" opacity="0.6"/>
            
            <!-- Thumb joint -->
            <circle cx="0" cy="-4" r="1.3" fill="#6b7280" stroke="#000000" stroke-width="1"/>
            
            <!-- Enhanced thumb tip -->
            <ellipse cx="0.8" cy="-12" rx="2.5" ry="3.5" fill="#60a5fa" filter="url(#babyBlueGlow)"/>
            
            <!-- Thumb highlights -->
            <ellipse cx="-0.5" cy="-7" rx="1.5" ry="3.5" fill="#93c5fd" opacity="0.7"/>
            <ellipse cx="1.2" cy="-10" rx="1.2" ry="2" fill="#dbeafe" opacity="0.8"/>
            
            <!-- Athletic sparkle on thumb -->
            <g transform="translate(1.5, -13)">
                <circle cx="0" cy="0" r="0.8" fill="#60a5fa" opacity="0.9"/>
                <circle cx="0" cy="0" r="0.4" fill="#dbeafe"/>
                <!-- Sparkle rays -->
                <line x1="0" y1="-1.5" x2="0" y2="-2.5" stroke="#dbeafe" stroke-width="0.4"/>
                <line x1="-1.5" y1="0" x2="-2.5" y2="0" stroke="#dbeafe" stroke-width="0.4"/>
                <line x1="1.5" y1="0" x2="2.5" y2="0" stroke="#dbeafe" stroke-width="0.4"/>
                <line x1="0" y1="1.5" x2="0" y2="2.5" stroke="#dbeafe" stroke-width="0.4"/>
            </g>
        </g>
    </g>
    
    <!-- Leaner Antenna (same) -->
    <line x1="100" y1="52" x2="100" y2="38" stroke="#000000" stroke-width="3" stroke-linecap="round"/>
    <circle cx="100" cy="52" r="3" fill="#6b7280" stroke="#000000" stroke-width="1.5"/>
    
    <!-- Baby blue antenna lights (same) -->
    <g filter="url(#babyBlueGlow)">
        <circle cx="100" cy="36" r="4" fill="#60a5fa"/>
        <circle cx="100" cy="36" r="2.5" fill="#3b82f6"/>
        <circle cx="100" cy="36" r="1" fill="#dbeafe"/>
        
        <!-- Secondary antenna light -->
        <circle cx="108" cy="40" r="1.5" fill="#60a5fa"/>
    </g>
    
    <!-- Athletic signal waves (same) -->
    <circle cx="100" cy="36" r="10" fill="none" stroke="#60a5fa" stroke-width="0.8" opacity="0.3"/>
    <circle cx="100" cy="36" r="15" fill="none" stroke="#60a5fa" stroke-width="0.5" opacity="0.2"/>
    
    <!-- Leaner Legs (thinner) -->
    <rect x="78" y="155" width="16" height="30" rx="8" fill="url(#leanBodyGrad)" stroke="#000000" stroke-width="2" filter="url(#leanShadow)"/>
    <rect x="106" y="155" width="16" height="30" rx="8" fill="url(#leanBodyGrad)" stroke="#000000" stroke-width="2" filter="url(#leanShadow)"/>
    
    <!-- Leg armor and joints (leaner) -->
    <rect x="82" y="165" width="6" height="12" rx="2" fill="#6b7280"/>
    <rect x="110" y="165" width="6" height="12" rx="2" fill="#6b7280"/>
    <circle cx="86" cy="170" r="1.2" fill="#000000"/>
    <circle cx="114" cy="170" r="1.2" fill="#000000"/>
    
    <!-- Leaner Robot Feet (sleeker) -->
    <g filter="url(#leanShadow)">
        <rect x="74" y="182" width="24" height="5" rx="2.5" fill="#1f2937" stroke="#000000" stroke-width="2"/>
        <rect x="102" y="182" width="24" height="5" rx="2.5" fill="#1f2937" stroke="#000000" stroke-width="2"/>
        <!-- Leaner tread details -->
        <rect x="76" y="185.5" width="20" height="1.2" fill="#000000"/>
        <rect x="104" y="185.5" width="20" height="1.2" fill="#000000"/>
    </g>
</svg>'''
    
    return svg_content

def main():
    """Create leaner Terry"""
    print("💪 Creating Leaner Terry Logo...")
    
    leaner_logo = create_leaner_terry_logo()
    with open('terry_logo_leaner.svg', 'w') as f:
        f.write(leaner_logo)
    
    print("✅ Leaner Terry created successfully!")
    print("📁 File created: terry_logo_leaner.svg")
    print("\n💪 Leaner Features:")
    print("  • MUCH LESS FAT body")
    print("  • SAME head size and features")
    print("  • Baby blue eyes (unchanged)")
    print("  • Baby blue mouth (unchanged)")
    print("  • Same GREAT thumbs up gesture")
    print("  • Thinner arms and legs")
    print("  • Leaner toolbelt")
    print("  • Streamlined tools")
    print("  • Athletic but leaner design")
    print("  • Maintains baby blue personality")
    print("  • More proportions and balance")
    
    # Update GUI to use leaner logo
    print("\n🔄 Updating ultra-modern GUI with leaner design...")
    
    from pathlib import Path
    gui_file = Path(__file__).parent / "terry_gui_ultra.py"
    if gui_file.exists():
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Update to use leaner logo
        content = content.replace('terry_logo_slim_athletic.svg', 'terry_logo_leaner.svg')
        
        with open(gui_file, 'w') as f:
            f.write(content)
        
        print("✅ Ultra-modern GUI updated with leaner Terry!")

if __name__ == "__main__":
    main()
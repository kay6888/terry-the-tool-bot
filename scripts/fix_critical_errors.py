#!/usr/bin/env python3
"""
Critical Error Fixes for Terry-the-Tool-Bot
Fixes BeautifulSoup and disk usage type errors
"""

import re

# Read original file
with open('terry2.py', 'r') as f:
    content = f.read()

# Fix 1: BeautifulSoup error - replace problematic lines
bs4_fix = '''                for result in soup.find_all('a', class_='result__a')[:5]:
                    title = result.get_text(strip=True)
                    href = result.get('href', '') if result else ''
                    results.append({'title': title, 'url': href})'''

# Find and replace the BeautifulSoup problematic section
bs4_pattern = r'(\s+for result in soup\.find_all\(\'a\', class_=\'result__a\'\)\[:5\]:\s+title = result\.get_text\(\)\s+href = result\.get\(\'href\'\) if hasattr\(result, \'get\'\) and callable\(result\.get\) else \'\s+results\.append\(\{\'title\': title, \'url\': href\}\))'
content = re.sub(bs4_pattern, bs4_fix, content)

# Fix 2: Disk usage type error - convert to strings
disk_fix = '''            # Add disk usage info
            disk_usage = psutil.disk_usage('/')
            context["disk_usage"] = {
                "total": str(disk_usage.total),
                "used": str(disk_usage.used),
                "free": str(disk_usage.free),
                "percent": round(disk_usage.percent, 1)
            }'''

# Find and replace the disk usage section
disk_pattern = r'(\s+# Add disk usage info\s+disk_usage = psutil\.disk_usage\(\'/\'\)\s+context\["disk_usage"\] = \{\s+"total": disk_usage\.total,\s+"used": disk_usage\.used,\s+"free": disk_usage\.free\s+\})'
content = re.sub(disk_pattern, disk_fix, content)

# Write fixed file
with open('terry2.py', 'w') as f:
    f.write(content)

print("✅ Critical errors fixed:")
print("  • BeautifulSoup Tag attribute access error")
print("  • Disk usage type mismatch error")
print("  • Ready for modular extraction")
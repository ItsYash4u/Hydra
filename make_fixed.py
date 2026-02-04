
import os
import re

src = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"
dst = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\dashboard_fixed.html"

try:
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple manual fix
    # We know the specific whitespace from previous view_file
    # <h3 class="fw-bold mb-0"><span class="sensor-value">{{
    #                                         latest_readings
    
    # We will regex replace {{\s*\n\s* with {{ 
    content = re.sub(r'\{\{\s*[\r\n]+\s*', '{{ ', content)
    
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")

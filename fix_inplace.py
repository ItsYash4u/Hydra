
import os
import re

file_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex replace {{\s*\n\s* with {{ 
    new_content = re.sub(r'\{\{\s*[\r\n]+\s*', '{{ ', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("FIXED IN PLACE")
except Exception as e:
    print(f"ERROR: {e}")

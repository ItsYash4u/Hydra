import re
import os

path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex 1: Fix split {{ variable }} tags
    # matches {{ followed by newline, whitespace, content, newline/whitespace, }}
    content = re.sub(r'\{\{\s*\n\s*(.*?)\s*\}\}', r'{{ \1 }}', content)

    # Regex 2: Fix split <small ...> tags which often follow the split variable
    # Matches </span> <small followed by newline whitespace class=
    content = re.sub(r'</span> <small\s*\n\s*class=', r'</span> <small class=', content)
    
    # Regex 3: Fix extra whitespace inside key tags if specific ones failed
    # <h3 class="fw-bold mb-0"><span class="sensor-value">{{ latest_readings...
    # Just in case some didn't match the newlines exactly
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully processed index.html")

except Exception as e:
    print(f"Error: {e}")

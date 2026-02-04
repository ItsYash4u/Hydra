
import re

file_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index_fixed.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Aggressive flattening regex
# Find: {{ followed by anything including newlines until }}
# Replace with single line match
content = re.sub(r'\{\{\s*[\r\n]+\s*(.*?)\s*\}\}', r'{{ \1 }}', content)

# Also fix the <span ...> <small> break if it exists
content = re.sub(r'</span>\s*<small', r'</span> <small', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed index_fixed.html")

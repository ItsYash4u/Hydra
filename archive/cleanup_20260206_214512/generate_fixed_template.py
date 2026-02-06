
import re
import os

source_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"
dest_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index_fixed.html"

with open(source_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix pattern: {{ followed by anything including newlines until }}
# Use a non-greedy match for content
new_content = re.sub(r'\{\{\s*[\r\n]+\s*(.*?)\s*\}\}', r'{{ \1 }}', content)

# Check if changes happened
if new_content == content:
    print("Warning: No regex changes made. Trying manual string replace for safety.")
    # Fallback: specific string replacement
    # Match the specific split I saw in view_file
    target = 'class="sensor-value">{{\n                                        latest_readings'
    replacement = 'class="sensor-value">{{ latest_readings'
    if target in content:
        new_content = content.replace(target, replacement)
        print("Manual replacement applied.")
    else:
        # It's possible the newlines are different
        # Regex should have caught it, but let's try reading line by line
        pass

with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Written to {dest_path}")

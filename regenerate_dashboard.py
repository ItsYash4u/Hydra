
import re
import os

# Paths
source_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"
dest_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\dashboard_v3.html"

# 1. Read the original 'broken' index.html
with open(source_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 2. Apply the fix: Collapse multi-line Django tags
# Matches {{ followed by newlines/spaces, replaces with {{ + space
fixed_content = re.sub(r'\{\{\s*[\r\n]+\s*', '{{ ', content)

# 3. Write to dashboard_v3.html (overwriting my previous partial version)
with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Successfully created {dest_path} with fixed tags from {source_path}")

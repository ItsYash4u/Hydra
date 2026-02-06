
import os
import re

# Use absolute paths
src = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"
dst = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\dashboard_v4.html"

if not os.path.exists(src):
    print(f"FATAL: Source {src} missing.")
    exit(1)

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# Apply the regex fix for any lingering split tags
# Replace {{ \n ... }} with {{ ... }}
fixed_content = re.sub(r'\{\{\s*[\r\n]+\s*', '{{ ', content)

# Check for the bad include specifically and kill it if found
if "index_partials/device_list.html" in fixed_content:
    print("Removing bad include...")
    fixed_content = fixed_content.replace("{% include 'pages/index_partials/device_list.html' %}", "")

with open(dst, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"SUCCESS: Created {dst} ({len(fixed_content)} bytes)")

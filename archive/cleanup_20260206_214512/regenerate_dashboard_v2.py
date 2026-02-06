
import os
import re
import time

src = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"
dst = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\dashboard_v3.html"

print(f"Starting regeneration from {src}...")

if not os.path.exists(src):
    print(f"ERROR: Source file {src} does not exist!")
    exit(1)

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Read {len(content)} bytes from source.")

# Apply regex fix for split tags
fixed_content = re.sub(r'\{\{\s*[\r\n]+\s*', '{{ ', content)

# Check for the bad include that causes the crash and remove it if present
bad_include = "{% include 'pages/index_partials/device_list.html' %}"
if bad_include in fixed_content:
    print("WARNING: Found bad include in source. Removing it.")
    fixed_content = fixed_content.replace(bad_include, "")

# Write to destination
try:
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print(f"Successfully wrote {len(fixed_content)} bytes to {dst}")
except Exception as e:
    print(f"ERROR writing file: {e}")
    exit(1)

# Verify
if os.path.exists(dst):
    size = os.path.getsize(dst)
    print(f"Verification: File size is {size} bytes.")
else:
    print("Verification: File was NOT created!")

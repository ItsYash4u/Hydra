
import os
import re

# Source is the known-good index.html (except for split tags maybe, but content is correct)
src = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"
dst = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\dashboard_final.html"

try:
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply the split-line fix (flatten {{ ... }} to single line)
    # Matches {{ <newline/space> <content> <newline/space> }} and makes it {{ <content> }}
    content = re.sub(r'\{\{\s*[\r\n]+\s*', '{{ ', content)
    
    # Just in case, ensure no device_list include exists (it shouldn't in index.html, but safety first)
    bad_include = "{% include 'pages/index_partials/device_list.html' %}"
    if bad_include in content:
        print("WARNING: Found bad include in index.html! Removing it.")
        content = content.replace(bad_include, "")

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Created {dst} with size {len(content)}")

except Exception as e:
    print(f"ERROR: {e}")

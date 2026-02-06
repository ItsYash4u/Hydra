import re

file_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the regex pattern to capture the multi-line template tags
# Matches: {{ <newline/spaces> variable <newline/spaces> }}
pattern = r'\{\{\s*[\r\n]+\s*([a-zA-Z0-9_\|\.\:]+)\s*\}\}'

# Function to flatten the match
def flatten(match):
    return '{{ ' + match.group(1) + ' }}'

new_content = re.sub(pattern, flatten, content)

# Check if changes were made
if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Normalized multi-line template tags.")
else:
    print("NO CHANGES: Pattern did not match any text.")

# Preview the specific lines to verify
lines = new_content.splitlines()
for i, line in enumerate(lines):
    if "latest_readings" in line and "Temperature" in line:
        print(f"Line {i+1}: {line.strip()}")

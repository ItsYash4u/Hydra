import re
import os

file_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"

if not os.path.exists(file_path):
    print("File not found!")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: {{ followed by newline and whitespace
pattern = r'\{\{\s*\n\s*'
replacement = r'{{ '

# Perform substitution
new_content, count = re.subn(pattern, replacement, content)

print(f"Replacements made: {count}")

if count > 0:
    # Also fix the trailing split part if needed: }}</span> <small
    # pattern2: \s*}}\s*\n\s*</span>
    # The view_file output: ...1 }}</span> <small
    # It seems the `}}` and `</span>` are on the 2nd line, so they are fine. 
    # The split is only at the start `{{`
    
    # Just in case, fix the newline after }}
    # 427: ...format:1 }}</span> <small
    # This looks like it's on one line.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("File saved successfully.")
else:
    print("No matches found. Debugging snippet:")
    start = content.find("Temperature")
    if start != -1:
        print(content[start:start+200].replace('\n', '\\n'))


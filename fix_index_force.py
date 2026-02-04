
import os

file_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False

for i in range(len(lines)):
    if skip:
        skip = False
        continue
    
    line = lines[i]
    if 'sensor-value">{{' in line:
        # Found the start of the split tag
        # e.g. <h3 ...><span class="sensor-value">{{
        
        # Get next line
        if i + 1 < len(lines):
            next_line = lines[i+1]
            # e.g. latest_readings... }}</span> <small
            
            # Combine them
            # We want to keep the indentation of the first line
            start_indent = line[:line.find('<h3')] # approximate indentation
            
            # Actually just strip both and combine with space
            # But we need to preserve the indentation of the first line
            
            clean_first = line.rstrip()
            clean_second = next_line.strip()
            
            combined = clean_first + " " + clean_second + "\n"
            new_lines.append(combined)
            skip = True
            print(f"Fixed split at line {i+1}")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done.")


# Script to merge split lines in Django templates
file_path = r"c:\Users\AYUSH\OneDrive\Desktop\noone\Hydroponics\Greeva\greeva\templates\pages\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False

for i in range(len(lines)):
    if skip_next:
        skip_next = False
        continue

    line = lines[i]
    stripped = line.strip()

    # Check for the specific split pattern: ends with {{
    if stripped.endswith('{{') and i + 1 < len(lines):
        next_line = lines[i+1]
        next_stripped = next_line.strip()
        
        # Check if the next line closes the tag
        if '}}' in next_stripped and 'latest_readings' in next_stripped:
            # Merge them
            # Keep the indentation of the first line
            start_part = line.rstrip() # remove newline and trailing spaces
            # Extract content from next line (e.g. "latest... }}</span> <small...")
            # We want to merge the curly braces.
            # actually the first line usually has <span ...>{{
            
            # effective merge:
            merged = start_part + " " + next_stripped.lstrip()
            new_lines.append(merged + "\n")
            skip_next = True
            print(f"Merged lines {i+1} and {i+2}")
            continue

    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done processing file.")

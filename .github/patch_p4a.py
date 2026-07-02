"""Patch p4a hostpython3/python3 recipes to use Python 3.12.8."""
import re
import sys
import os

p4a_dir = sys.argv[1]
target_version = sys.argv[2]

for recipe in ['hostpython3', 'python3']:
    filepath = os.path.join(p4a_dir, 'recipes', recipe, '__init__.py')
    with open(filepath) as f:
        content = f.read()

    # Replace any line like: version = "3.14.2" or version = '3.14.2'
    # Use a simple string replacement instead of regex to avoid edge cases
    old_line = None
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('version = ') and ('3.14' in stripped or '3.12' in stripped):
            # Determine the quote style
            for q in ['"', "'"]:
                if q in stripped:
                    old_line = stripped
                    break
            break

    if old_line is None:
        print(f"WARNING: No version line found in {recipe}")
        continue

    # Replace preserving indentation
    indent = len(old_line) - len(old_line.lstrip())
    quote = '"' if '"' in old_line else "'"
    new_line = ' ' * indent + f'version = {quote}{target_version}{quote}'
    content = content.replace(old_line, new_line, 1)

    with open(filepath, 'w') as f:
        f.write(content)

    # Verify
    patched = False
    with open(filepath) as f:
        for line in f:
            if target_version in line and 'version' in line:
                print(f'Patched {recipe} -> {target_version}')
                patched = True
                break
    if not patched:
        print(f'ERROR: {recipe} was NOT patched correctly')
        sys.exit(1)

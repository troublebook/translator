"""Patch p4a hostpython3/python3 recipes to use a specific Python version."""
import re
import sys
import os

p4a_dir = sys.argv[1]
target_version = sys.argv[2]

for recipe in ['hostpython3', 'python3']:
    filepath = os.path.join(p4a_dir, 'recipes', recipe, '__init__.py')
    with open(filepath) as f:
        content = f.read()

    # Match version = "..." or version = '...'
    pattern = r"(version\s*=\s*)(['\"])([^'\"]+)\2"
    replacement = rf"\1\2{target_version}\2"
    new_content = re.sub(pattern, replacement, content, count=1)

    with open(filepath, 'w') as f:
        f.write(new_content)

    # Verify
    with open(filepath) as f:
        for line in f:
            if 'version' in line and target_version in line:
                print(f'Patched {recipe} -> {target_version}')
                break

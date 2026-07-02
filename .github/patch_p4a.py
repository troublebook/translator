"""Patch p4a hostpython3/python3 recipes to use Python 3.12.8."""
import sys
import os

p4a_dir = sys.argv[1]
target_version = sys.argv[2]

for recipe in ['hostpython3', 'python3']:
    filepath = os.path.join(p4a_dir, 'recipes', recipe, '__init__.py')
    with open(filepath, 'rb') as f:
        content = f.read()

    # Replace version = "3.14.2" or version = '3.14.2' with version = "3.12.8"
    # Work on raw bytes to avoid encoding/line-ending issues
    import re
    # Match version = '...' or version = "..." where the value is 3.1x
    pattern = rb"version\s*=\s*['\"][^'\"]*3\.1\d[^'\"]*['\"]"
    replacement = f'version = "{target_version}"'.encode()
    new_content = re.sub(pattern, replacement, content, count=1)

    if new_content == content:
        print(f"WARNING: No version line found in {recipe}")
        continue

    with open(filepath, 'wb') as f:
        f.write(new_content)

    # Verify
    with open(filepath, 'rb') as f:
        for line in f:
            if target_version.encode() in line:
                print(f'Patched {recipe} -> {target_version}')
                break
        else:
            print(f'ERROR: {recipe} was NOT patched correctly')
            sys.exit(1)

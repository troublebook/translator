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

    # Replace version = "..." or version = '...' with version = "3.12.8"
    # Pattern includes the closing quote so replacer can reconstruct properly
    def replacer(m):
        q = m.group(2)
        return m.group(1) + q + target_version + q

    new_content = re.sub(r"(version\s*=\s*)(['\"])([^'\"]+)(['\"])", replacer, content, count=1)

    with open(filepath, 'w') as f:
        f.write(new_content)

    # Verify
    with open(filepath) as f:
        for line in f:
            if 'version' in line and target_version in line:
                print(f'Patched {recipe} -> {target_version}')
                break

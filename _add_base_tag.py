"""
Batch script: Add <base> tag to all HTML files' <head> section.
- GitHub Pages deployment: uncomment <base href="/first/">
- Local file open: keep <base href="./"> active
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]

# The base tag block to insert right after <head>
BASE_BLOCK = """    <!-- ✅ 部署到 GitHub 时取消注释此行 -->
    <!-- <base href="/first/"> -->

    <!-- ✅ 本地双击打开时取消注释此行（注意末尾斜杠） -->
    <base href="./">"""

modified = []
skipped = []

for filename in html_files:
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if base tag already exists
    if '<base href' in content:
        skipped.append(filename)
        continue

    # Insert base block right after <head> tag
    pattern = r'(<head>)'
    replacement = r'\1\n' + BASE_BLOCK

    new_content = re.sub(pattern, replacement, content, count=1)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified.append(filename)
    else:
        skipped.append(f"{filename} (no <head> found)")

print(f"Modified ({len(modified)} files):")
for f in modified:
    print(f"  ✅ {f}")

if skipped:
    print(f"\nSkipped ({len(skipped)} files):")
    for f in skipped:
        print(f"  ⏭️  {f}")

print(f"\nTotal: {len(modified)} modified, {len(skipped)} skipped, {len(html_files)} total")

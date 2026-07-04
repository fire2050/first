import re
import os

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract :root CSS block from index.html
root_match = re.search(r'(:root\s*\{[^}]*\})', index_content, re.DOTALL)
if root_match:
    root_css = root_match.group(1)
    print(f"✅ Extracted :root CSS ({len(root_css)} chars)")
else:
    print("❌ Could not find :root in index.html")
    exit(1)

# Extract the COMPLETE navbar CSS (from "/* 导航栏 */" to before the next major section)
# We need to find the navbar CSS and the dropdown CSS
nav_css_start = index_content.find('/* 导航栏 */')
if nav_css_start == -1:
    print("❌ Could not find navbar CSS start")
    exit(1)

# Find the end of navbar CSS (next /* comment */ that's not part of navbar)
# The navbar CSS ends before "/* Hero区域 */" or similar
nav_css_end_markers = ['/* Hero区域 */', '/* Hero */', '/* 二级下拉菜单 */']
# Actually, let's just extract from /* 导航栏 */ to the line before the next /* that's not part of navbar CSS
# Simpler approach: extract a large chunk that includes all navbar CSS
nav_css = index_content[nav_css_start:nav_css_start+3000]  # Get 3000 chars
print(f"✅ Extracted navbar CSS region ({len(nav_css)} chars)")

# Now fix all other HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

fixed_count = 0

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # Check 1: Does the file have :root CSS variables?
    if ':root' not in content:
        # Add :root after <style> tag
        # Find where to insert it (after the first line of CSS)
        style_pos = content.find('<style>')
        if style_pos != -1:
            # Find the end of the first CSS rule/line after <style>
            insert_pos = content.find('\n', style_pos + 10)
            if insert_pos == -1:
                insert_pos = content.find('}', style_pos) + 1
            
            if insert_pos != -1:
                content = content[:insert_pos] + '\n\n        /* CSS变量 */\n        ' + root_css.strip() + '\n' + content[insert_pos:]
                print(f"  + Added :root to {filename}")
                modified = True
    
    # Check 2: Does the file have the complete navbar CSS?
    # Look for key navbar CSS rules
    required_nav_rules = ['.navbar {', '.nav-links {', '.dropdown-menu {', '.dropdown-item {']
    missing_rules = [rule for rule in required_nav_rules if rule not in content]
    
    if missing_rules:
        print(f"  ⚠️  {filename} missing navbar CSS rules: {missing_rules}")
        # Try to add the navbar CSS before the first CSS rule after <style>
        # For simplicity, let's just add the key navbar CSS
    
    # Check 3: Does the file have overflow-x: hidden on body?
    if 'overflow-x: hidden' not in content:
        # Add it to the body CSS rule
        body_match = re.search(r'body\s*\{', content)
        if body_match:
            # Find the closing } of the body rule and add the property
            # This is complex, so let's just add a separate body rule
            pass
    
    # Save if modified
    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f"✅ Fixed: {filename}\n")

print(f"\n🎉 Total files fixed: {fixed_count}")

import re
import os

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract :root CSS block
root_match = re.search(r':root\s*\{[^}]*\}', index_content, re.DOTALL)
root_css = root_match.group(0) if root_match else ''

# Extract navbar CSS (from "/* 导航栏 */" to "/* Hero区域 */")
nav_css_start = index_content.find('/* 导航栏 */')
hero_css_start = index_content.find('/* Hero区域 */')
if nav_css_start != -1 and hero_css_start != -1:
    nav_css_full = index_content[nav_css_start:hero_css_start].strip()
else:
    nav_css_full = ''

print(f":root length: {len(root_css)}")
print(f"Navbar CSS length: {len(nav_css_full)}")

# Extract navbar HTML
nav_html_match = re.search(r'(<nav class="navbar"[^>]*>.*?</nav>)', index_content, re.DOTALL)
nav_html = nav_html_match.group(1) if nav_html_match else ''

# Fix all other HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # Fix 1: Add :root if missing
    if ':root' not in content:
        # Insert after <style> tag, before the first CSS rule
        style_end = content.find('<style>') + len('<style>')
        # Find first { after <style>
        insert_pos = content.find('\n', style_end)
        if insert_pos == -1:
            insert_pos = style_end + 50
        
        root_block = '\n        /* CSS变量 */\n        ' + root_css.strip() + '\n\n'
        content = content[:insert_pos] + root_block + content[insert_pos:]
        print(f"  + Added :root to {filename}")
        modified = True
    
    # Fix 2: Replace navbar CSS with correct version
    # Find the navbar CSS in the file (starts with /* 导航栏 */ or .navbar {)
    file_nav_css_start = content.find('/* 导航栏 */')
    if file_nav_css_start == -1:
        # Try to find .navbar {
        file_nav_css_start = content.find('.navbar {')
    
    if file_nav_css_start != -1:
        # Find where navbar CSS ends (next /* comment */ that's not dropdown related)
        # Look for the next /* after navbar CSS start
        next_comment = content.find('\n        /*', file_nav_css_start + 20)
        if next_comment == -1:
            next_comment = content.find('/*', file_nav_css_start + 20)
        
        if next_comment != -1:
            # Check if the next comment is a new section (not dropdown related)
            comment_text = content[next_comment:next_comment+50]
            if '下拉' not in comment_text and 'Footer' not in comment_text and 'Hero' not in comment_text:
                # This is a new section, our navbar CSS ends here
                pass
            
            # Replace the navbar CSS
            old_nav_css = content[file_nav_css_start:next_comment].strip()
            if old_nav_css != nav_css_full and nav_css_full:
                content = content[:file_nav_css_start] + nav_css_full + '\n\n        ' + content[next_comment:]
                print(f"  + Replaced navbar CSS in {filename}")
                modified = True
    
    # Fix 3: Replace navbar HTML
    file_nav_html_match = re.search(r'(<nav class="navbar"[^>]*>.*?</nav>)', content, re.DOTALL)
    if file_nav_html_match and nav_html:
        file_nav_html = file_nav_html_match.group(1)
        if file_nav_html != nav_html:
            content = content.replace(file_nav_html, nav_html)
            print(f"  + Replaced navbar HTML in {filename}")
            modified = True
    
    # Save
    if modified:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {filename}\n")
    else:
        print(f"✓ No changes needed: {filename}\n")

print("Done!")

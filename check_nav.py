import re
import os

# Read index.html and extract navbar HTML
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

nav_html_match = re.search(r'(<nav class="navbar"[^>]*>.*?</nav>)', index_content, re.DOTALL)
correct_nav = nav_html_match.group(1) if nav_html_match else ''

print(f"Correct navbar length: {len(correct_nav)} chars\n")

# Check all other HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

all_ok = True
for filename in sorted(html_files):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_nav_match = re.search(r'(<nav class="navbar"[^>]*>.*?</nav>)', content, re.DOTALL)
    if file_nav_match:
        file_nav = file_nav_match.group(1)
        if file_nav == correct_nav:
            print(f"[OK] {filename} - navbar identical")
        else:
            print(f"[DIFF] {filename} - navbar differs!")
            # Show what's different
            print(f"  File nav length: {len(file_nav)}")
            all_ok = False
    else:
        print(f"[MISSING] {filename} - no navbar found!")
        all_ok = False

if all_ok:
    print("\n✅ All navbars are identical!")
else:
    print("\n⚠️ Some navbars differ - need fixing")

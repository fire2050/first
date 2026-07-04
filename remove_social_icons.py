import os
import re

pages_dir = r"C:\Users\fire2\WorkBuddy\2026-06-30-11-01-53"
html_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
html_files.sort()

for fname in html_files:
    fpath = os.path.join(pages_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 删除 footer-social 整个 div（含换行）
    content = re.sub(r'\s*<div class="footer-social">\s*<a href="#" title="微信">💬</a>\s*<a href="#" title="微博">📢</a>\s*<a href="#" title="知乎">📖</a>\s*</div>', '', content)

    # 同时删除对应的 CSS（.footer-social 及相关样式）
    # 先找到 style 标签中的 footer-social CSS 并删除
    # 匹配 .footer-social { ... } 块
    content = re.sub(r'\s*\.footer-social\s*\{[^}]*\}\s*', '', content)
    content = re.sub(r'\s*\.footer-social a\s*\{[^}]*\}\s*', '', content)
    content = re.sub(r'\s*\.footer-social a:hover\s*\{[^}]*\}\s*', '', content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] {fname}")
    else:
        print(f"  [SKIP] {fname} (no social icons found)")

print("\nDone. All footer social icons removed.")

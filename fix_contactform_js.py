import re

# Find all HTML files with the buggy contactForm code
import glob

files = glob.glob("*.html")
fixed = []

for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read()

    original = content

    # Fix: wrap contactForm.addEventListener in a null check
    old = """        // 表单提交\n        document.getElementById('contactForm').addEventListener('submit', function(e) {\n            e.preventDefault();\n            alert('感谢您的咨询！我们将尽快与您联系。');\n            this.reset();\n        });"""

    new = """        // 表单提交（仅当表单存在时执行）\n        const contactForm = document.getElementById('contactForm');\n        if (contactForm) {\n            contactForm.addEventListener('submit', function(e) {\n                e.preventDefault();\n                alert('感谢您的咨询！我们将尽快与您联系。');\n                this.reset();\n            });\n        }"""

    content = content.replace(old, new)

    if content != original:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(content)
        fixed.append(f)
        print(f"Fixed: {f}")

print(f"\nTotal fixed: {len(fixed)}")

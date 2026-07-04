import re

pages = [
    "product-wuying.html",
    "product-wuying-hardware.html",
    "product-jvs.html",
    "product-agentbay.html"
]

for page in pages:
    with open(page, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Fix 1: footer-content grid columns 4 -> 5
    content = content.replace(
        "grid-template-columns: 2fr 1fr 1fr 1fr;",
        "grid-template-columns: 2fr 1fr 1fr 1fr 1fr;"
    )

    # Fix 2: JS contactForm error - wrap in null check
    old_js = """        // 表单提交\n        document.getElementById('contactForm').addEventListener('submit', function(e) {\n            e.preventDefault();\n            alert('感谢您的咨询！我们将尽快与您联系。');\n            this.reset();\n        });"""
    new_js = """        // 表单提交（仅当表单存在时执行）\n        const contactForm = document.getElementById('contactForm');\n        if (contactForm) {\n            contactForm.addEventListener('submit', function(e) {\n                e.preventDefault();\n                alert('感谢您的咨询！我们将尽快与您联系。');\n                this.reset();\n            });\n        }"""
    content = content.replace(old_js, new_js)

    if content != original:
        with open(page, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed: {page}")
    else:
        print(f"Unchanged: {page}")

print("Done")

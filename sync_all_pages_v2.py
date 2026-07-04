#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""同步所有HTML页面的 :root CSS变量、导航栏和底部，确保与首页一致"""

import os
import re

BASE = r"C:\Users\fire2\WorkBuddy\2026-06-30-11-01-53"

# 标准 :root CSS变量块（从已修复的product-wuying.html提取）
ROOT_CSS = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --deep-space: #0a0e1a;
            --tech-blue: #1a2a4a;
            --neon-cyan: #00d4ff;
            --electric-purple: #8b5cf6;
            --text-primary: #e8eaed;
            --text-secondary: #9aa0a6;
            --light-gray: #3c4043;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            background: var(--deep-space);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }
"""

# 标准底部HTML（与首页完全一致）
FOOTER_HTML = """
    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-column">
                <div class="footer-logo">智慧解决方案</div>
                <p class="footer-desc">智慧解决方案事业部致力于为企业客户提供一站式数字化转型服务，成为客户数字化与智能化转型的首选合作伙伴。</p>
            </div>
            <div class="footer-column">
                <h4 class="footer-title">生态产品</h4>
                <ul class="footer-links">
                    <li><a href="product-wuying.html">无影云电脑商业版</a></li>
                    <li><a href="product-wuying-hardware.html">无影硬件</a></li>
                    <li><a href="product-jvs.html">JVS Computer</a></li>
                    <li><a href="product-agentbay.html">AgentBay 开发套件</a></li>
                    <li><a href="product-meetingboard.html">音视频会议平板</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h4 class="footer-title">解决方案</h4>
                <ul class="footer-links">
                    <li><a href="solution-ai.html">AI 应用解决方案</a></li>
                    <li><a href="solution-communication.html">融合通信解决方案</a></li>
                    <li><a href="solution-avintegration.html">音视频集成解决方案</a></li>
                    <li><a href="solution-smartoffice.html">智慧办公解决方案</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h4 class="footer-title">专业服务</h4>
                <ul class="footer-links">
                    <li><a href="service.html#ai-landing">AI 应用落地</a></li>
                    <li><a href="service.html#system-integration">系统集成</a></li>
                    <li><a href="service.html#maintenance">专业维护</a></li>
                    <li><a href="service.html#expert">专家服务</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h4 class="footer-title">联系我们</h4>
                <ul class="footer-links">
                    <li><a href="contact.html">联系方式</a></li>
                    <li><a href="contact.html">在线咨询</a></li>
                    <li><a href="contact.html">服务网点</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 智慧解决方案事业部 版权所有 | 备案号：XX-XXXXX</p>
            <div class="footer-social">
                <a href="#" title="微信">💬</a>
                <a href="#" title="微博">📢</a>
                <a href="#" title="知乎">📖</a>
            </div>
        </div>
    </footer>
"""

# 需要处理的页面
WUYING_PAGES = [
    "product-wuying-hardware.html",
    "product-jvs.html",
    "product-agentbay.html",
]

def fix_root_css(filepath):
    """确保每个文件都有 :root CSS变量定义"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 如果没有 :root，在 <head> 结束后、第一个 <style> 前插入
    if ':root' not in content:
        # 在 </head> 后插入标准CSS变量
        insert_block = "</head>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        :root {\n            --deep-space: #0a0e1a;\n            --tech-blue: #1a2a4a;\n            --neon-cyan: #00d4ff;\n            --electric-purple: #8b5cf6;\n            --text-primary: #e8eaed;\n            --text-secondary: #9aa0a6;\n            --light-gray: #3c4043;\n        }\n        body {\n            font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif;\n            background: var(--deep-space);\n            color: var(--text-primary);\n            line-height: 1.6;\n            overflow-x: hidden;\n        }\n    </style>\n"
        content = content.replace('</head>', insert_block)
        modified = True
        print(f"  + 添加 :root CSS变量: {os.path.basename(filepath)}")
    
    return content, modified

def fix_footer(filepath, content):
    """确保底部与首页一致"""
    # 找到现有底部并替换
    footer_pattern = r'<footer class="footer">.*?</footer>\s*</body>'
    # 更精确的方式：找到 <footer class="footer"> 到 </body> 之间的内容
    
    # 先找到 footer 开始位置
    footer_start = content.find('<footer class="footer">')
    if footer_start == -1:
        print(f"  ! 未找到 footer: {os.path.basename(filepath)}")
        return content, False
    
    # 找到 </body>
    body_end = content.find('</body>', footer_start)
    if body_end == -1:
        print(f"  ! 未找到 </body>: {os.path.basename(filepath)}")
        return content, False
    
    # 替换从 <footer 到 </body> 的内容
    new_content = content[:footer_start] + FOOTER_HTML + "\n    </body>\n</html>"
    
    print(f"  + 底部已同步: {os.path.basename(filepath)}")
    return new_content, True

def fix_js_contactform(filepath, content):
    """修复 contactForm JS 报错"""
    if 'getElementById(\'contactForm\')' in content and 'if (contactForm)' not in content:
        old = '        document.getElementById(\'contactForm\').addEventListener'
        new = '        var cf = document.getElementById(\'contactForm\');\n        if (cf) { cf.addEventListener'
        content = content.replace(old, new)
        # 找到对应的关闭括号
        # 简单处理：在 </script> 前加 }
        content = content.replace('    </script>', '        }\n    </script>')
        print(f"  + JS contactForm 已修复: {os.path.basename(filepath)}")
        return content, True
    return content, False

# 主流程
for page in WUYING_PAGES:
    filepath = os.path.join(BASE, page)
    if not os.path.exists(filepath):
        print(f"文件不存在: {page}")
        continue
    
    print(f"\n处理: {page}")
    content, modified = fix_root_css(filepath)
    content, m2 = fix_footer(filepath, content)
    content, m3 = fix_js_contactform(filepath, content)
    
    if modified or m2 or m3:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  => 已保存: {page}")
    else:
        print(f"  = 无需修改: {page}")

print("\n完成！")

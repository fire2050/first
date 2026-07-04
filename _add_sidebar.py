#!/usr/bin/env python3
"""给4个亿联产品页面添加左侧类别标签侧边栏"""

import re

# 4个亿联产品文件及其对应信息
products = [
    ('product-meetingboard.html', '音视频会议平板', '📺'),
    ('product-audiovideo.html', '会议室音视频', '🎥'),
    ('product-meetingsmart.html', '会议室智能', '🤖'),
    ('product-iphone.html', 'IP话机', '📞'),
]

# 侧边栏CSS
sidebar_css = """
        /* 产品类别侧边栏 */
        .product-layout {
            display: flex;
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .category-sidebar {
            width: 220px;
            min-width: 220px;
            flex-shrink: 0;
            position: sticky;
            top: 100px;
            align-self: flex-start;
        }
        .category-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 16px;
            margin-bottom: 12px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.15);
        }
        .category-title-text {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
        }
        .category-arrow {
            font-size: 12px;
            color: var(--text-secondary);
        }
        .category-nav {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .category-item {
            display: block;
            padding: 14px 20px;
            border-radius: 10px;
            text-decoration: none;
            font-size: 15px;
            color: var(--text-secondary);
            transition: all 0.25s ease;
            border: 1px solid transparent;
        }
        .category-item:hover {
            background: rgba(0, 212, 255, 0.08);
            color: var(--neon-cyan);
            border-color: rgba(0, 212, 255, 0.15);
        }
        .category-item.active {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 180, 216, 0.10));
            color: #00D4FF;
            font-weight: 600;
            border-color: rgba(0, 212, 255, 0.3);
        }

        /* 右侧内容区 */
        .product-content-main {
            flex: 1;
            min-width: 0;
        }

        @media (max-width: 900px) {
            .product-layout { flex-direction: column; }
            .category-sidebar { 
                width: 100%; 
                position: static; 
                margin-bottom: 30px; 
            }
            .category-nav { 
                flex-direction: row; 
                flex-wrap: wrap; 
            }
            .category-item {
                padding: 8px 16px;
                font-size: 13px;
            }
        }
"""

# 生成侧边栏HTML（根据当前页面决定哪个active）
def gen_sidebar_html(current_file):
    items_html = ''
    for fname, title, icon in products:
        active_class = ' active' if fname == current_file else ''
        items_html += f'                <a href="{fname}" class="category-item{active_class}">{icon} {title}</a>\n'
    return f'''    <!-- 产品类别侧边栏 -->
    <div class="product-layout">
        <aside class="category-sidebar">
            <div class="category-header">
                <span class="category-title-text">类别</span>
                <span class="category-arrow">▼</span>
            </div>
            <nav class="category-nav" id="categoryNav">
{items_html}            </nav>
        </aside>
        <main class="product-content-main">
'''

# 关闭标签
sidebar_close = '''        </main>
    </div>
'''

for current_file, current_title, current_icon in products:
    with open(current_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # === 1. 添加CSS ===
    # 在 } 后面、@media 前面插入 sidebar CSS
    css_marker = '    @media (max-width: 768px) {'
    if css_marker in content:
        content = content.replace(css_marker, sidebar_css + '\n' + css_marker)

    # === 2. 包装Hero之后的内容区域 ===
    # 找到第一个 section（在hero之后），在其前面插入 sidebar 开始标签
    # 找到 footer 标签，在其前面插入 sidebar 结束标签

    # 用正则匹配 hero 区域后的第一个 section
    pattern = r'(</section>\s*\n\s*<section class="section">)'
    
    # 插入sidebar开始
    def insert_sidebar_open(match):
        return match.group(0) + '\n' + gen_sidebar_html(current_file)
    
    content = re.sub(pattern, insert_sidebar_open, content, count=1)
    
    # 在footer之前插入关闭标签
    content = content.replace(
        '<footer class="footer">',
        sidebar_close + '\n    <footer class="footer">'
    )

    # 写回文件
    with open(current_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] {current_file} - sidebar added")

print("\nAll done!")

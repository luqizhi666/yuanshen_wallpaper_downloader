import os
from pathlib import Path

def generate_html():
    base_dir = Path.cwd()
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    categories = {}
    for root, _, files in os.walk(base_dir):
        root_path = Path(root)
        if any(part.startswith('.') for part in root_path.parts):
            continue
        
        rel_path = root_path.relative_to(base_dir)
        category = str(rel_path).split(os.sep)[0] if rel_path != Path('.') else "根目录"
        
        for file in files:
            if Path(file).suffix.lower() in image_exts:
                img_path = rel_path / file
                if category not in categories:
                    categories[category] = []
                categories[category].append(str(img_path).replace('\\', '/'))

    # 构建快速预览部分
    quick_preview_html = ''
    for cat in categories:
        for img in categories[cat][:5]:
            quick_preview_html += f'<a href="#{cat}" class="scroll-item"><img src="{img}" alt="{Path(img).name}"></a>\n'

    # 构建分类展示部分
    category_sections_html = ''
    for cat, imgs in categories.items():
        category_sections_html += f'''
    <section class="gallery-section" id="{cat}">
        <h2>{cat}</h2>
        <div class="grid-container">
'''
        for img in imgs:
            category_sections_html += f'''
            <div class="grid-item">
                <img src="{img}" loading="lazy">
                <div>
                    <a href="{img}" download class="download-btn">下载高清版</a>
                </div>
            </div>
'''
        category_sections_html += '''
        </div>
    </section>
'''

    # 组合完整 HTML 内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>原神壁纸库</title>
    <style>
        :root {{ --scroll-speed: 30s; }}
        body {{ font-family: "Microsoft Yahei", sans-serif; background: #f0f2f5; }}
        
        .gallery-section {{ margin: 2rem 0; }}
        h2 {{ color: #1a1a1a; border-left: 4px solid #ff6b6b; padding-left: 1rem; }}
        
        .scroll-container {{
            overflow-x: auto;
            white-space: nowrap;
            padding: 1rem 0;
            scroll-behavior: smooth;
        }}
        .scroll-item {{
            display: inline-block;
            margin-right: 1rem;
            transition: transform 0.3s;
        }}
        .scroll-item:hover {{ transform: scale(1.05); }}
        .scroll-item img {{
            height: 200px;
            width: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .grid-item {{ text-align: center; }}
        .grid-item img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }}
        .download-btn {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #4CAF50;
            color: white!important;
            border-radius: 20px;
            text-decoration: none;
            transition: background 0.3s;
        }}
        .download-btn:hover {{ background: #45a049; }}
    </style>
</head>
<body>
    <h1 style="text-align: center; color: #2c3e50;">🎨 原神活动壁纸合集</h1>

    <!-- 横向滚动展示区 -->
    <section class="gallery-section">
        <h2>快速浏览</h2>
        <div class="scroll-container">
            {quick_preview_html}
        </div>
    </section>

    <!-- 分类总览 -->
    {category_sections_html}
</body>
</html>
'''

    # 写入 HTML 文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    generate_html()

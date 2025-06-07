import os
from pathlib import Path
from urllib.parse import quote  # 新增
from PIL import Image  # 新增
import random  # 新增
import shutil  # 新增

def generate_html():
    base_dir = Path.cwd()
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    categories = {}
    all_pc_imgs = {}
    all_mobile_imgs = {}

    for root, _, files in os.walk(base_dir):
        root_path = Path(root)
        if any(part.startswith('.') for part in root_path.parts):
            continue
        
        rel_path = root_path.relative_to(base_dir)
        category = str(rel_path).split(os.sep)[0] if rel_path != Path('.') else "根目录"
        
        for file in files:
            if Path(file).suffix.lower() in image_exts:
                img_path = os.path.relpath(root_path / file, base_dir)
                img_path = './' + img_path.replace('\\', '/')
                if category not in categories:
                    categories[category] = []
                categories[category].append(img_path)

    # --- 随机壁纸功能 ---
    random_dir = Path(base_dir) / "random"
    if not random_dir.exists():
        random_dir.mkdir()
    # 清空 random 目录
    for f in random_dir.iterdir():
        if f.is_file():
            f.unlink()

    # 收集所有分辨率的图片
    pc_size_map = {}
    mobile_size_map = {}
    for cat, imgs in categories.items():
        if cat == "根目录":
            continue
        for img in imgs:
            img_path = img.lstrip('./')
            try:
                with Image.open(img_path) as im:
                    w, h = im.size
                    size_str = f"{w}x{h}"
                    # 只统计真实存在的图片，且避免重复
                    if w >= h:
                        pc_size_map.setdefault(size_str, set()).add(img_path)
                    else:
                        mobile_size_map.setdefault(size_str, set()).add(img_path)
            except Exception:
                continue

    # 随机复制每种分辨率的图片到 random 目录
    for size, imgset in pc_size_map.items():
        imglist = list(imgset)
        if imglist:
            pick = random.choice(imglist)
            ext = os.path.splitext(pick)[1]
            shutil.copy(pick, random_dir / f"{size}{ext}")
    for size, imgset in mobile_size_map.items():
        imglist = list(imgset)
        if imglist:
            pick = random.choice(imglist)
            ext = os.path.splitext(pick)[1]
            shutil.copy(pick, random_dir / f"{size}{ext}")

    # 构建快速预览部分
    quick_preview_html = ''
    for cat in categories:
        if cat == "根目录":
            continue  # 跳过根目录
        for img in categories[cat][:5]:
            img_url = quote(img)  # 路径编码
            quick_preview_html += f'<a href="#{cat}" class="scroll-item"><img src="{img_url}" alt="{Path(img).name}"></a>\n'

    # 构建分类展示部分（区分横/竖图）
    category_sections_html = ''
    for cat, imgs in categories.items():
        if cat == "根目录":
            continue  # 跳过根目录
        # 分类图片分组
        pc_imgs = []
        mobile_imgs = []
        for img in imgs:
            img_path = img.lstrip('./')
            try:
                with Image.open(img_path) as im:
                    w, h = im.size
                    if w >= h:
                        pc_imgs.append(img)
                    else:
                        mobile_imgs.append(img)
            except Exception:
                pc_imgs.append(img)  # 读取失败默认归为PC

        category_sections_html += f'''
    <section class="gallery-section" id="{cat}">
        <h2>{cat}</h2>
        <div class="grid-container-title pc-title">电脑壁纸</div>
        <div class="grid-container pc-container">
'''
        for img in pc_imgs:
            img_url = quote(img)
            category_sections_html += f'''
            <div class="grid-item">
                <img data-src="{img_url}" alt="{Path(img).name}">
                <div class="download-btn-wrap">
                    <a href="{img_url}" download class="download-btn" title="下载">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;">
                            <path d="M12 3v12m0 0l-4-4m4 4l4-4M4 21h16" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </a>
                </div>
            </div>
'''
        category_sections_html += '''
        </div>
        <div class="grid-container-title mobile-title">手机壁纸</div>
        <div class="grid-container mobile-container">
'''
        for img in mobile_imgs:
            img_url = quote(img)
            category_sections_html += f'''
            <div class="grid-item">
                <img data-src="{img_url}" alt="{Path(img).name}">
                <div class="download-btn-wrap">
                    <a href="{img_url}" download class="download-btn" title="下载">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;">
                            <path d="M12 3v12m0 0l-4-4m4 4l4-4M4 21h16" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </a>
                </div>
            </div>
'''
        category_sections_html += '''
        </div>
    </section>
'''

    # 构建侧边栏主题列表
    sidebar_html = '''
    <div class="sidebar" id="sidebar">
        <div class="sidebar-title">
            分类主题
            <button id="sidebar-toggle" title="隐藏/显示侧边栏" style="float:right;background:none;border:none;cursor:pointer;font-size:1.2em;color:#4CAF50;">⮜</button>
        </div>
        <ul>
    '''
    for cat in categories:
        if cat == "根目录":
            continue
        sidebar_html += f'<li><a href="#{cat}">{cat}</a></li>'
    sidebar_html += '</ul></div>'

    max_cat_len = max((len(cat) for cat in categories if cat != "根目录"), default=4)
    # 估算宽度：每个汉字约16px，英文约9px，取最大长度，+80px留空
    sidebar_width = min(max(80 + max_cat_len * 18, 180), 420)  # 180~420px自适应

    # 组合完整 HTML 内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>原神壁纸库</title>
    <link rel="icon" type="image/png" href="venti.png">
    <style>
        :root {{ --scroll-speed: 30s; --primary: #4CAF50; --secondary: #ff6b6b; }}
        body {{
            font-family: "Microsoft Yahei", "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #f0f2f5 0%, #e3f0ff 100%);
            margin: 0;
            padding: 0;
        }}
        .sidebar {{
            position: fixed;
            top: 80px;
            left: 0;
            width: {sidebar_width}px;
            min-width: 120px;
            max-width: 420px;
            background: #f8fafc;
            border-radius: 0 16px 16px 0;
            box-shadow: 2px 0 12px rgba(76,175,80,0.07);
            padding: 1.2em 0.7em 1.2em 1.2em;
            z-index: 100;
            max-height: 80vh;
            overflow-y: auto;
            transition: left 0.3s, box-shadow 0.3s, width 0.3s;
        }}
        .sidebar.hide {{
            left: -{sidebar_width - 50}px;
            box-shadow: none;
        }}
        .sidebar-title {{
            font-weight: bold;
            color: var(--primary);
            font-size: 1.1em;
            margin-bottom: 1em;
            letter-spacing: 1px;
            user-select: none;
        }}
        .sidebar ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .sidebar li {{
            margin-bottom: 0.7em;
            word-break: break-all;
        }}
        .sidebar a {{
            color: #333;
            text-decoration: none;
            font-size: 1.05em;
            border-left: 3px solid transparent;
            padding-left: 0.5em;
            transition: color 0.2s, border 0.2s;
        }}
        .sidebar a:hover, .sidebar a.active {{
            color: var(--secondary);
            border-left: 3px solid var(--secondary);
            background: #e3f0ff;
            border-radius: 0 8px 8px 0;
        }}
        .sidebar #sidebar-toggle {{
            margin-left: 10px;
        }}
        @media (max-width: 900px) {{
            .sidebar {{ display: none; }}
            .main-container {{ margin-left: 0 !important; }}
        }}
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.07);
            padding: 0.5rem;
            margin-left: {sidebar_width + 20}px;
            transition: margin-left 0.3s;
        }}
        .sidebar.hide ~ .main-container {{
            margin-left: 60px;
        }}
        .gallery-section {{ margin: 2rem 0; }}
        h1 {{
            color: #222;
            font-size: 2.3em;
            letter-spacing: 2px;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
            text-shadow: 0 2px 8px rgba(76,175,80,0.08);
        }}
        h2 {{
            color: #1a1a1a;
            border-left: 4px solid var(--secondary);
            padding-left: 1rem;
            font-size: 1.35em;
            margin-bottom: 1.2rem;
            margin-top: 2.2rem;
            font-weight: 600;
        }}
        .grid-container-title {{
            font-size: 1.08em;
            color: var(--primary);
            margin: 0.5em 0 0.2em 0.5em;
            font-weight: bold;
            letter-spacing: 1px;
        }}
        .hidden-title {{ display: none !important; }}
        .scroll-container {{
            overflow-x: auto;
            white-space: nowrap;
            padding: 1rem 0;
            scroll-behavior: smooth;
            position: relative;
            background: #f8fafc;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(76,175,80,0.04);
        }}
        .scroll-item {{
            display: inline-block;
            margin-right: 1rem;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .scroll-item:hover {{
            transform: scale(1.07);
            box-shadow: 0 4px 16px rgba(76,175,80,0.15);
        }}
        .scroll-item img {{
            height: 180px;
            width: auto;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 2px solid #e3f0ff;
            background: #fff;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1.2rem;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(76,175,80,0.04);
        }}
        .grid-item {{
            text-align: center;
            position: relative;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: box-shadow 0.3s;
        }}
        .grid-item img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            transition: box-shadow 0.3s;
            background: #f0f2f5;
            opacity: 0;
            transition: opacity 0.4s, box-shadow 0.3s;
        }}
        .grid-item img.loaded {{
            opacity: 1;
        }}
        .grid-item:hover {{
            box-shadow: 0 4px 16px rgba(76,175,80,0.13);
        }}
        .download-btn-wrap {{
            position: absolute;
            top: 10px;
            right: 10px;
            opacity: 1;
            pointer-events: auto;
            z-index: 2;
        }}
        .download-btn {{
            display: inline-block;
            padding: 0.5rem;
            background: var(--primary);
            border-radius: 50%;
            text-decoration: none;
            transition: background 0.3s, box-shadow 0.3s;
            color: white !important;
            box-shadow: 0 2px 8px rgba(76,175,80,0.15);
            border: none;
        }}
        .download-btn:hover {{
            background: var(--secondary);
            box-shadow: 0 4px 16px rgba(255,107,107,0.18);
        }}
        .download-btn::after {{ content: ""; }}
        /* 手机适配 */
        @media (max-width: 600px) {{
            .main-container {{ padding: 0.5rem; }}
            .scroll-item img {{ height: 100px; }}
            .grid-container {{
                grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
                gap: 0.5rem;
                padding: 0.5rem;
            }}
            .grid-item img {{ margin-bottom: 0.2rem; }}
            .download-btn-wrap {{ top: 4px; right: 4px; }}
            .download-btn {{ padding: 0.3rem; }}
        }}
        .search-bar {{
            display: flex;
            justify-content: center;
            margin: 2rem 0 1rem 0;
        }}
        .search-bar input {{
            width: 350px;
            font-size: 1.1em;
            padding: 0.5em 1em;
            border-radius: 20px;
            border: 1.5px solid var(--primary);
            outline: none;
            transition: border 0.3s, box-shadow 0.3s;
            background: #f8fafc;
        }}
        .search-bar input:focus {{
            border: 1.5px solid var(--secondary);
            box-shadow: 0 2px 8px rgba(255,107,107,0.08);
        }}
        .highlight {{
            outline: 2px solid var(--secondary);
            outline-offset: 2px;
        }}
        .hidden-section {{ display: none !important; }}
        .hidden-img {{ display: none !important; }}
        .filter-bar {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        .filter-btn {{
            padding: 0.4em 1.2em;
            border-radius: 20px;
            border: 1.5px solid var(--primary);
            background: #fff;
            color: var(--primary);
            font-size: 1em;
            cursor: pointer;
            transition: background 0.2s, color 0.2s, border 0.2s;
        }}
        .filter-btn.active, .filter-btn:hover {{
            background: var(--primary);
            color: #fff;
            border: 1.5px solid var(--secondary);
        }}
        #resolutionSelect {{
            margin-left:1em;
            padding:0.4em 1em;
            border-radius:20px;
            border:1.5px solid var(--primary);
            font-size:1em;
            background: #f8fafc;
            color: var(--primary);  /* 绿色字体 */
            outline: none;
            transition: border 0.2s;
        }}
        #resolutionSelect:focus {{
            border:1.5px solid var(--secondary);
        }}
        #resolutionSelect option {{
            color: var(--primary);  /* 绿色字体 */
            background: #fff;
        }}
        /* 强制APlayer字体颜色为深色，防止透明或白色 */
        .aplayer, .aplayer * {{
            color: #222 !important;
            font-family: "Microsoft Yahei", "Segoe UI", Arial, sans-serif !important;
            opacity: 1 !important;
            text-shadow: none !important;
        }}
        .aplayer .aplayer-lrc p {{
            color: #222 !important;
            opacity: 1 !important;
        }}
        .aplayer-info {{
            display: block !important;
        }}
        .aplayer-title, .aplayer-author, .aplayer-ptime, .aplayer-dtime, .aplayer-lrc, .aplayer-list-title, .aplayer-list-author {{
            color: #222 !important;
            opacity: 1 !important;
            text-shadow: none !important;
        }}
        /* 若有透明背景，强制白色背景 */
        .aplayer {{
            background: #fff !important;
        }}
        .aplayer-notice {{
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            min-height: 0 !important;
            min-width: 0 !important;
            max-height: 0 !important;
            max-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            background: none !important;
        }}
    </style>
    <!-- MetingJS & APlayer -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.css">
    <script src="https://cdn.jsdelivr.net/npm/aplayer/dist/APlayer.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/meting@2.0.1/dist/Meting.min.js"></script>
</head>
<body>
    ''' + sidebar_html + '''
    <div class="main-container" id="main-container">
    <h1 style="text-align: center;">
        <img src="venti.png" alt="Venti" style="height:2.2em;vertical-align:middle;margin-right:0.5em;">
        原神活动壁纸合集
    </h1>
    <!-- 网易云歌单播放器 -->
    <div id="aplayer-wrap" style="max-width:420px;margin:0 auto 1.5em auto;display:block !important;">
        <meting-js
            server="netease"
            type="playlist"
            id="13812854633"
            fixed="true"
            mini="false"
            order="random"
            preload="auto"
            theme="#4CAF50"
            loop="all"
            list-max-height="320px"
            volume="0.7"
            lrc-type="1"
            list-folded="false"
            mutex="true"
            autoplay="false"
            style="display:block !important;">
        </meting-js>
    </div>
    <script>
    // 强制显示APlayer和MetingJS组件
    document.addEventListener("DOMContentLoaded", function() {
        setTimeout(function() {
            var ap = document.querySelector('.aplayer');
            if (ap) ap.style.display = 'block';
            var meting = document.querySelector('meting-js');
            if (meting) meting.style.display = 'block';
        }, 800);
    });
    </script>
    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="🔍 搜索图片文件名或分类..." oninput="searchImages()">
    </div>
    <div class="filter-bar">
        <button class="filter-btn active" onclick="setSizeFilter('all', this)">全部</button>
        <button class="filter-btn" onclick="setSizeFilter('mobile', this)">只看手机壁纸</button>
        <button class="filter-btn" onclick="setSizeFilter('pc', this)">只看电脑壁纸</button>
        <select id="resolutionSelect">
            <option value="all">全部分辨率</option>
            <option value="720x1280">720x1280</option>
            <option value="1080x1920">1080x1920</option>
            <option value="1440x2560">1440x2560</option>
            <option value="1920x1080">1920x1080</option>
            <option value="2560x1440">2560x1440</option>
            <option value="3840x2160">3840x2160</option>
        </select>
    </div>
    <!-- 横向滚动展示区 -->
    <section class="gallery-section">
        <h2>快速浏览</h2>
        <div class="scroll-container" id="scrollContainer">
            ''' + quick_preview_html + '''
        </div>
    </section>
    <!-- 分类总览 -->
    ''' + category_sections_html + '''
    </div>
    <script>
    // 侧边栏高亮当前分类
    document.addEventListener("DOMContentLoaded", function() {
        var sidebarLinks = document.querySelectorAll('.sidebar a');
        function highlightSidebar() {
            var scrollPos = window.scrollY || window.pageYOffset;
            var sections = document.querySelectorAll('.gallery-section[id]');
            var currentId = "";
            for (var i = 0; i < sections.length; i++) {
                var sec = sections[i];
                if (sec.offsetTop - 80 <= scrollPos) {
                    currentId = sec.id;
                }
            }
            sidebarLinks.forEach(function(link) {
                link.classList.toggle('active', link.getAttribute('href') === '#' + currentId);
            });
        }
        window.addEventListener('scroll', highlightSidebar);
        highlightSidebar();

        // 侧边栏隐藏/显示
        var sidebar = document.getElementById('sidebar');
        var mainContainer = document.getElementById('main-container');
        var toggleBtn = document.getElementById('sidebar-toggle');
        var hide = false;
        toggleBtn.onclick = function() {
            hide = !hide;
            if (hide) {
                sidebar.classList.add('hide');
                mainContainer.style.marginLeft = '60px';
                toggleBtn.innerText = '⮞';
            } else {
                sidebar.classList.remove('hide');
                mainContainer.style.marginLeft = '290px';
                toggleBtn.innerText = '⮜';
            }
        };
    });
    // 懒加载实现
    document.addEventListener("DOMContentLoaded", function() {
        if ('IntersectionObserver' in window) {
            var imgs = document.querySelectorAll('.grid-item img[data-src]');
            var observer = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        var img = entry.target;
                        img.src = img.getAttribute('data-src');
                        img.onload = function() { img.classList.add('loaded'); };
                        observer.unobserve(img);
                    }
                });
            }, { rootMargin: "100px" });
            imgs.forEach(function(img) { observer.observe(img); });
        } else {
            // 不支持IntersectionObserver时直接加载
            var imgs = document.querySelectorAll('.grid-item img[data-src]');
            imgs.forEach(function(img) {
                img.src = img.getAttribute('data-src');
                img.onload = function() { img.classList.add('loaded'); };
            });
        }
    });
    var sizeFilter = 'all';
    var resolutionFilter = 'all';
    document.getElementById('resolutionSelect').addEventListener('change', function() {
        resolutionFilter = this.value;
        searchImages();
    });

    function setSizeFilter(type, btn) {
        sizeFilter = type;
        document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        searchImages();
    }

    function searchImages() {
        var input = document.getElementById('searchInput').value.trim().toLowerCase();
        var sections = document.querySelectorAll('.gallery-section[id]');
        sections.forEach(function(section) {
            var catTitle = section.querySelector('h2').textContent.toLowerCase();
            var pcTitle = section.querySelector('.pc-title');
            var mobileTitle = section.querySelector('.mobile-title');
            var pcContainer = section.querySelector('.pc-container');
            var mobileContainer = section.querySelector('.mobile-container');
            var pcItems = pcContainer ? pcContainer.querySelectorAll('.grid-item') : [];
            var mobileItems = mobileContainer ? mobileContainer.querySelectorAll('.grid-item') : [];
            var sectionMatch = false;
            var pcMatch = false;
            var mobileMatch = false;
            // PC壁纸
            pcItems.forEach(function(item) {
                var img = item.querySelector('img');
                var alt = img.getAttribute('alt') || '';
                var src = img.getAttribute('src') || '';
                var filename = alt.toLowerCase() || src.split('/').pop().toLowerCase();
                var show = true;
                if (!(input === '' || catTitle.includes(input) || filename.includes(input))) {
                    show = false;
                }
                var ratio = img.naturalWidth && img.naturalHeight ? img.naturalWidth / img.naturalHeight : 0;
                // 分辨率筛选
                if (resolutionFilter !== 'all') {
                    var res = resolutionFilter.split('x');
                    var w = parseInt(res[0]), h = parseInt(res[1]);
                    if (!(img.naturalWidth === w && img.naturalHeight === h)) show = false;
                }
                if (sizeFilter === 'mobile' && ratio >= 1) show = false;
                if (sizeFilter === 'pc' && ratio < 1) show = false;
                if (show) {
                    item.classList.remove('hidden-img');
                    img.classList.toggle('highlight', input !== '' && filename.includes(input));
                    pcMatch = true;
                    sectionMatch = true;
                } else {
                    item.classList.add('hidden-img');
                    img.classList.remove('highlight');
                }
            });
            // 手机壁纸
            mobileItems.forEach(function(item) {
                var img = item.querySelector('img');
                var alt = img.getAttribute('alt') || '';
                var src = img.getAttribute('src') || '';
                var filename = alt.toLowerCase() || src.split('/').pop().toLowerCase();
                var show = true;
                if (!(input === '' || catTitle.includes(input) || filename.includes(input))) {
                    show = false;
                }
                var ratio = img.naturalWidth && img.naturalHeight ? img.naturalWidth / img.naturalHeight : 0;
                // 分辨率筛选
                if (resolutionFilter !== 'all') {
                    var res = resolutionFilter.split('x');
                    var w = parseInt(res[0]), h = parseInt(res[1]);
                    if (!(img.naturalWidth === w && img.naturalHeight === h)) show = false;
                }
                if (sizeFilter === 'mobile' && ratio >= 1) show = false;
                if (sizeFilter === 'pc' && ratio < 1) show = false;
                if (show) {
                    item.classList.remove('hidden-img');
                    img.classList.toggle('highlight', input !== '' && filename.includes(input));
                    mobileMatch = true;
                    sectionMatch = true;
                } else {
                    item.classList.add('hidden-img');
                    img.classList.remove('highlight');
                }
            });
            // 分类标题和容器显示/隐藏
            if (sizeFilter === 'mobile') {
                if (pcTitle) pcTitle.classList.add('hidden-title');
                if (pcContainer) pcContainer.style.display = 'none';
                if (mobileTitle) {
                    if (mobileMatch) {
                        mobileTitle.classList.remove('hidden-title');
                        if (mobileContainer) mobileContainer.style.display = '';
                    } else {
                        mobileTitle.classList.add('hidden-title');
                        if (mobileContainer) mobileContainer.style.display = 'none';
                    }
                }
            } else if (sizeFilter === 'pc') {
                if (mobileTitle) mobileTitle.classList.add('hidden-title');
                if (mobileContainer) mobileContainer.style.display = 'none';
                if (pcTitle) {
                    if (pcMatch) {
                        pcTitle.classList.remove('hidden-title');
                        if (pcContainer) pcContainer.style.display = '';
                    } else {
                        pcTitle.classList.add('hidden-title');
                        if (pcContainer) pcContainer.style.display = 'none';
                    }
                }
            } else {
                if (pcTitle) {
                    if (pcMatch) {
                        pcTitle.classList.remove('hidden-title');
                        if (pcContainer) pcContainer.style.display = '';
                    } else {
                        pcTitle.classList.add('hidden-title');
                        if (pcContainer) pcContainer.style.display = 'none';
                    }
                }
                if (mobileTitle) {
                    if (mobileMatch) {
                        mobileTitle.classList.remove('hidden-title');
                        if (mobileContainer) mobileContainer.style.display = '';
                    } else {
                        mobileTitle.classList.add('hidden-title');
                        if (mobileContainer) mobileContainer.style.display = 'none';
                    }
                }
            }
            // 整个分类显示/隐藏
            if (sectionMatch) {
                section.classList.remove('hidden-section');
            } else {
                section.classList.add('hidden-section');
            }
        });
    }

    // 图片加载后自动刷新筛选（确保宽高可用）
    window.addEventListener('load', function() {
        document.querySelectorAll('.grid-item img').forEach(function(img) {
            img.onload = searchImages;
        });
    });

    // 循环滚动效果
    (function() {
        var container = document.getElementById('scrollContainer');
        var scrollSpeed = 1;
        var interval = null;
        function duplicateContent() {
            if (container.scrollWidth <= container.clientWidth) return;
            var html = container.innerHTML;
            container.innerHTML += html;
        }
        duplicateContent();
        function startScroll() {
            if (interval) return;
            interval = setInterval(function() {
                if (container.scrollWidth <= container.clientWidth) return;
                container.scrollLeft += scrollSpeed;
                if (container.scrollLeft >= container.scrollWidth / 2) {
                    container.scrollLeft = 0;
                }
            }, 20);
        }
        function stopScroll() {
            clearInterval(interval);
            interval = null;
        }
        container.addEventListener('mouseenter', stopScroll);
        container.addEventListener('mouseleave', startScroll);
        startScroll();
    })();
    </script>
</body>
</html>
'''

    # 写入 HTML 文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    generate_html()

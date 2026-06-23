import re
import plotly.graph_objects as go
import os
import hashlib
from pathlib import Path
from config import (
    OUTPUT_TREE,
    OUTPUT_HTML,
    OUTPUT_PREVIEW,
    ROOT_NAME,
    MAX_DEPTH,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    IMAGE_SCALE,
    GENERATE_PREVIEW,
    PLOTLY_JS_MODE,
)

# ================= 配置映射 =================
INPUT_FILE = OUTPUT_TREE
OUTPUT_FILE = OUTPUT_HTML
IMAGE_OUTPUT_FILE = OUTPUT_PREVIEW
# ===========================================


def parse_tree_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.readlines()

    if not content:
        print(f"❌ 错误：无法读取文件 {filepath}，请检查文件是否存在或编码格式。")
        return {}

    nodes = {}
    # 路径栈: [(depth, full_id)]
    path_stack = [(-1, ROOT_NAME)]
    nodes[ROOT_NAME] = {"label": ROOT_NAME, "parent": ""}

    for line in content:
        line = line.rstrip()

        # 正则匹配缩进和节点名，非格式行（如首行绝对路径、代码块标记）将直接被过滤
        match = re.search(r"([│\s]*)(├──|└──)\s+(.*)", line)
        if not match:
            continue

        prefix = match.group(1)
        name = match.group(3).strip()

        # 计算深度 (每4个字符算一级)
        depth = len(prefix) // 4

        # 栈维护：回退到正确的父级层级
        while len(path_stack) > depth + 1:
            path_stack.pop()

        parent_id = path_stack[-1][1]

        # 构建唯一ID
        current_id = f"{parent_id}/{name}"

        nodes[current_id] = {"label": name, "parent": parent_id}

        # 将当前节点推入栈中
        path_stack.append((depth, current_id))

    return nodes


def generate_sunburst(nodes):
    ids = []
    labels = []
    parents = []
    values = []

    for node_id, data in nodes.items():
        ids.append(node_id)
        labels.append(data["label"])
        parents.append(data["parent"] if data["label"] != ROOT_NAME else "")
        # 给每个节点一个基础大小
        values.append(1)

    if not ids:
        print("❌ 警告：没有解析到任何节点，请检查 tree.md 内容格式是否正确。")
        return None

    # 创建旭日图
    fig = go.Figure(
        go.Sunburst(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            maxdepth=MAX_DEPTH,  # 动态读取 TOML 中的最大层级
            insidetextorientation="radial",
            hoverinfo="label+percent parent",
            marker=dict(colorscale="Viridis", line=dict(color="white", width=0.5)),
            textfont=dict(
                size=24,          
                family="Arial Black"
            ),
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Inter, sans-serif",
        font_color="#f3f4f6",
        margin=dict(t=10, l=10, r=10, b=10),
    )

    return fig


def get_file_md5(filepath):
    """计算文件的 MD5 校验和"""
    if not os.path.exists(filepath):
        return ""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def make_sunburst():
    print(f"1. 正在读取 {INPUT_FILE}...")
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到 {INPUT_FILE}")
        return

    nodes = parse_tree_file(INPUT_FILE)
    if not nodes:
        return

    print(f"2. 解析完成，共提取 {len(nodes)} 个节点。")

    print("3. 正在生成可视化图表...")
    try:
        fig = generate_sunburst(nodes)
        if fig:
            print(f"4. 正在保存为 {OUTPUT_FILE}...")
            # 导出为图表片段并嵌入符合 HTML5 规范的暗黑卡片模板中，开启动态自适应缩放响应
            chart_html = fig.to_html(include_plotlyjs=PLOTLY_JS_MODE, full_html=False, config={'responsive': True})
            
            html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Knowledge Graph</title>
    <!-- 引入高档 Inter 字体 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #151b23; /* 默认暗夜背景 */
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.1) 0px, transparent 50%);
            color: #f3f4f6;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
            transition: background-color 0.4s ease, color 0.4s ease;
        }}
        
        /* 白天模式 */
        body.light {{
            background-color: #f8fafc;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.06) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.06) 0px, transparent 50%);
            color: #0f172a;
        }}

        .container {{
            width: 90%;
            max-width: 1000px;
            height: 90vh;
            max-height: 800px;
            display: flex;
            flex-direction: column;
            background: rgba(22, 27, 34, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.8),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 30px;
            box-sizing: border-box;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        body.light .container {{
            background: rgba(255, 255, 255, 0.5);
            border-color: rgba(15, 23, 42, 0.08);
            box-shadow: 
                0 30px 60px rgba(15, 23, 42, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.6);
        }}

        .container:hover {{
            border-color: rgba(255, 255, 255, 0.12);
        }}
        
        body.light .container:hover {{
            border-color: rgba(15, 23, 42, 0.12);
        }}

        h1 {{
            font-size: 28px;
            margin-top: 0;
            margin-bottom: 20px;
            font-weight: 700;
            letter-spacing: -0.75px;
            background: linear-gradient(135deg, #818cf8, #c084fc, #e879f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            flex-shrink: 0;
            transition: all 0.4s ease;
        }}
        
        body.light h1 {{
            background: linear-gradient(135deg, #4f46e5, #7c3aed, #d946ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .chart-wrapper {{
            flex: 1;
            min-height: 0;
            width: 100%;
            position: relative;
            border-radius: 16px;
            background: rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.03);
            padding: 10px;
            box-sizing: border-box;
            transition: all 0.4s ease;
        }}
        
        body.light .chart-wrapper {{
            background: rgba(15, 23, 42, 0.03);
            border-color: rgba(15, 23, 42, 0.03);
        }}

        .tip-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 6px 16px;
            border-radius: 9999px;
            margin-top: 20px;
            font-size: 13px;
            color: #9ca3af;
            font-weight: 500;
            flex-shrink: 0;
            align-self: center;
            transition: all 0.4s ease;
        }}
        
        body.light .tip-badge {{
            background: rgba(15, 23, 42, 0.04);
            border-color: rgba(15, 23, 42, 0.06);
            color: #475569;
        }}

        .tip-badge svg {{
            width: 16px;
            height: 16px;
            color: #818cf8;
            transition: color 0.4s ease;
        }}
        
        body.light .tip-badge svg {{
            color: #4f46e5;
        }}

        /* 主题切换圆钮 */
        .theme-toggle {{
            position: fixed;
            top: 24px;
            right: 24px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #f3f4f6;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 100;
            backdrop-filter: blur(8px);
        }}
        
        body.light .theme-toggle {{
            background: rgba(15, 23, 42, 0.04);
            border-color: rgba(15, 23, 42, 0.08);
            color: #0f172a;
        }}

        .theme-toggle:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: scale(1.05);
            border-color: rgba(255, 255, 255, 0.15);
        }}
        
        body.light .theme-toggle:hover {{
            background: rgba(15, 23, 42, 0.08);
            border-color: rgba(15, 23, 42, 0.12);
        }}

        .theme-toggle svg {{
            width: 20px;
            height: 20px;
        }}

        /* 控制太阳/月亮图标展示 */
        body.light .sun-icon {{
            display: block;
        }}
        body.light .moon-icon {{
            display: none;
        }}
        body:not(.light) .sun-icon {{
            display: none;
        }}
        body:not(.light) .moon-icon {{
            display: block;
        }}
    </style>
</head>
<body>
    <button id="theme-toggle" class="theme-toggle" aria-label="切换主题">
        <!-- 太阳图标 -->
        <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 9H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M14 12a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <!-- 月亮图标 -->
        <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
    </button>

    <div class="container">
        <h1>My Knowledge Graph</h1>
        <div class="chart-wrapper">
            {chart_html}
        </div>
        <div class="tip-badge">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
            <span>点击中心区域返回上一级 · 悬停查看占比</span>
        </div>
    </div>

    <script>
        const toggleBtn = document.getElementById('theme-toggle');
        const chartDiv = document.querySelector('.plotly-graph-div');
        
        toggleBtn.addEventListener('click', () => {{
            document.body.classList.toggle('light');
            const isLight = document.body.classList.contains('light');
            
            // 如果页面存在 Plotly，动态切换图表文本颜色以保障清晰度
            if (chartDiv && window.Plotly) {{
                const newFontColor = isLight ? '#0f172a' : '#f3f4f6';
                Plotly.relayout(chartDiv.id, {{
                    'font.color': newFontColor
                }});
            }}
        }});
    </script>
</body>
</html>
"""
            OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT_FILE.write_text(html_template, encoding="utf-8")
            print("✅ 网页生成完成！已启用轻量化在线 CDN 引用。")

            # 智能生图缓存与优化
            if GENERATE_PREVIEW:
                CACHE_FILE = OUTPUT_FILE.parent / ".tree_md5.cache"
                current_md5 = get_file_md5(INPUT_FILE)
                cached_md5 = ""
                
                if CACHE_FILE.exists():
                    cached_md5 = CACHE_FILE.read_text().strip()

                if cached_md5 == current_md5 and IMAGE_OUTPUT_FILE.exists():
                    print("ℹ️ 检测到 tree.md 未改变且预览图已存在，跳过生图流程。")
                else:
                    print(f"5. 正在导出预览图: {IMAGE_OUTPUT_FILE}...")
                    # 临时修改背景色，使生成的静态预览图包含指定的 #151b23 纯色背景
                    fig.update_layout(paper_bgcolor="#151b23")
                    fig.write_image(
                        str(IMAGE_OUTPUT_FILE),
                        width=IMAGE_WIDTH,
                        height=IMAGE_HEIGHT,
                        scale=IMAGE_SCALE,
                        engine="kaleido"
                    )
                    CACHE_FILE.write_text(current_md5, encoding="utf-8")
                    print("✅ 预览图成功更新！")
            else:
                print("ℹ️ 已配置跳过预览图生成。")

            print("✅ 全部工作顺利完成！")
    except Exception as e:
        print(f"❌ 生成失败: {e}")


if __name__ == "__main__":
    make_sunburst()
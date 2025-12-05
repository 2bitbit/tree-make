import re
import plotly.graph_objects as go
import os
from pathlib import Path
from LISTS import sensitive_words_included

# ================= 配置区域 =================
INPUT_FILE = Path(__file__).parent.parent / "outputs" / "tree.md"
OUTPUT_FILE = Path(__file__).parent.parent / "outputs" / "index.html"

ROOT_NAME = "My Knowledge Universe"
IMAGE_OUTPUT_FILE = Path(__file__).parent.parent / "outputs" / "preview.png"

# ===========================================


def is_sensitive(name: str) -> bool:
    """检查文件或目录名是否包含敏感词。"""
    lower_name = name.lower()
    sensitive_words = sensitive_words_included(lower_name)

    if sensitive_words:
        print(f"❌ sunburst 绘制中，过滤敏感词:{sensitive_words} (被包含在 {lower_name})")
        return True
    else:
        return False


def parse_tree_file(filepath):
    with open(filepath, "r",encoding='utf-8') as f:
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
        if not line or line.startswith("D:"):
            continue

        # 正则匹配缩进和节点名
        # 兼容 "│   " 和 "    " 等不同缩进风格
        match = re.search(r"([│\s]*)(├──|└──)\s+(.*)", line)
        if not match:
            continue

        prefix = match.group(1)
        name = match.group(3).strip()
        # 过滤敏感词
        if is_sensitive(name):
            continue

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
        if len(path_stack) > depth + 1:
            path_stack[-1] = (depth, current_id)
        else:
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
            maxdepth=3,  # 默认显示的层级深度
            insidetextorientation="radial",
            hoverinfo="label+percent parent",
            marker=dict(colorscale="Viridis", line=dict(color="white", width=0.5)),
        )
    )

    fig.update_layout(
        title_text="My Knowledge Graph",
        title_x=0.5,
        font_family="sans-serif",
        margin=dict(t=40, l=0, r=0, b=0),
        width=1000,
        height=1000,
    )

    return fig


def make_sunburst():
    print(f"1. 正在读取 {INPUT_FILE}...")
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到 {INPUT_FILE}，请确认文件在脚本同一目录下。")
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
            fig.write_html(OUTPUT_FILE)
            print(f"5. 正在导出预览图: {IMAGE_OUTPUT_FILE}...")
            # scale=2 表示 2倍分辨率 (Retina效果)，engine="kaleido" 使用 kaleido 引擎
            fig.write_image(str(IMAGE_OUTPUT_FILE), width=1000, height=1000, scale=2, engine="kaleido")
            print("✅ 完成！请双击 index.html 查看效果。")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        # 添加友好提示
        print("提示：如果 HTML 生成成功但图片失败，请检查是否安装了库: pip install kaleido")

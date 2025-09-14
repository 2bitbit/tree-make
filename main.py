from pathlib import Path
from config import TARGET_DIR, OUTPUT_DIR, OUTPUT_FILENAME, IGNORE_SET


def generate_tree(start_path: Path, prefix: str = "") -> list[str]:
    """递归生成目录树的可视化表示。
    Args:
        start_path: 要开始生成树的目录路径。
        prefix: 用于当前行缩进和连接线的字符串。

    Returns:
        一个字符串列表，每行代表树的一个部分。
    """
    tree_lines = []
    try:
        # 列表推导式一次性完成遍历和过滤
        contents = [p for p in start_path.iterdir() if p.name not in IGNORE_SET]
    except (FileNotFoundError, PermissionError) as e:
        # 增加健壮性，处理目录不存在或无权访问的情况
        return [f"{prefix}└── [错误: {e.strerror}]"]

    # 为了美观和一致性，将目录排在文件前面，然后统一按名称排序
    contents.sort(key=lambda p: (p.is_file(), p.name.lower()))

    # 巧妙地生成连接线：除了最后一个，其他都是 "├── "，最后一个是 "└── "
    pointers = ["├── "] * (len(contents) - 1) + ["└── "]

    for pointer, path in zip(pointers, contents):
        item = f"{prefix}{pointer}{path.name}"
        item += "/" if path.is_dir() else ""
        tree_lines.append(item)

        if path.is_dir():
            # 判断是否是最后一个条目，来决定下一层递归的前缀: 如果是最后一个，后续就不需要 "│" 连接线了
            extension = "│   " if pointer != "└── " else "    "
            tree_lines.extend(generate_tree(path, prefix + extension))

    return tree_lines


def main():
    """主函数，生成并保存目录树。"""
    print(f"\n开始扫描目录: {TARGET_DIR.resolve()}")

    # 生成树形结构
    tree_structure = [f"```text\n{TARGET_DIR.resolve()}"]
    tree_structure.extend(generate_tree(TARGET_DIR))
    tree_structure.append("```")

    # 输出到文件
    output_path = OUTPUT_DIR / OUTPUT_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(tree_structure), encoding="utf-8")

    print(f"目录树已成功生成到: {output_path.resolve()}")


if __name__ == "__main__":
    main()

import tomllib
from pathlib import Path

# 默认 config.toml 位于项目根目录
CONFIG_PATH = Path(__file__).parent.parent / "config.toml"

with CONFIG_PATH.open("rb") as f:
    _config = tomllib.load(f)

# 1. 解析路径配置
paths = _config.get("paths", {})
INPUT_DIR = Path(paths.get("input_dir", r"D:\Notes"))

def _resolve_relative_path(path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else Path(__file__).parent.parent / p

OUTPUT_TREE = _resolve_relative_path(paths.get("output_tree", "outputs/tree.md"))
OUTPUT_HTML = _resolve_relative_path(paths.get("output_html", "outputs/index.html"))
OUTPUT_PREVIEW = _resolve_relative_path(paths.get("output_preview", "outputs/preview.png"))

# 2. 解析 tree 配置
tree_conf = _config.get("tree", {})
IGNORE_SET = set(tree_conf.get("ignore_set", []))

# 3. 解析 sunburst 配置
sb_conf = _config.get("sunburst", {})
ROOT_NAME = sb_conf.get("root_name", "My Knowledge Universe")
MAX_DEPTH = sb_conf.get("max_depth", 3)
IMAGE_WIDTH = sb_conf.get("image_width", 1000)
IMAGE_HEIGHT = sb_conf.get("image_height", 1000)
IMAGE_SCALE = float(sb_conf.get("image_scale", 1.0))
GENERATE_PREVIEW = sb_conf.get("generate_preview", True)
PLOTLY_JS_MODE = sb_conf.get("plotly_js_mode", "cdn")

# 4. 解析安全配置并转换为小写，保留白名单精确、黑名单模糊包含的规则
security = _config.get("security", {})
BLACKLIST = {word.lower() for word in security.get("blacklist", [])}
WHITELIST = {word.lower() for word in security.get("whitelist", [])}

def sensitive_words_included(name: str) -> None | list:
    """按原规则校验敏感词（白名单完全精确匹配优先，黑名单子串模糊匹配居后）"""
    lower_name = name.lower()
    if lower_name in WHITELIST:
        return None
    words_in_blacklist = [word for word in BLACKLIST if word in lower_name]
    if words_in_blacklist:
        return words_in_blacklist
    return None

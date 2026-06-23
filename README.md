# tree_make: 目录树与旭日图生成器

一个用于扫描本地目录并生成 Markdown 树和交互式 HTML 旭日图的 Python 脚本。

---

## 功能特点

- **双重生成**：扫描目录并输出 Markdown 格式的物理树，同时生成用于层级缩放的交互式旭日图。
- **配置分离**：路径、忽略目录、图表参数、安全过滤列表统一写在 `config.toml` 中，修改无需改动代码。
- **体积轻量**：HTML 网页默认使用官方 CDN 引入 Plotly 引擎，生成的 `index.html` 体积约 8KB，交互无卡顿且不增加 Git 提交负担。
- **生图缓存**：引入 MD5 校验，当目录树未发生改变且已生成 `preview.png` 时，运行会自动跳过耗时的无头浏览器截图流程，实现秒级执行。
- **隐私拦截**：提供大小写不敏感的黑白名单过滤，用于在生成树时自动剔除真实姓名、就医历史、主机密钥、QQ 机器人配置等敏感路径。

---

## 配置文件说明 (`config.toml`)

```toml
[paths]
input_dir = "D:\\Notes"                      # 扫描的源目录
output_tree = "outputs/tree.md"              # 树结构 md 输出路径
output_html = "outputs/index.html"            # 旭日图 html 网页路径
output_preview = "outputs/preview.png"        # 静态预览图路径

[tree]
ignore_set = [".git", ".obsidian", ".smart-env", "Z_attachments"]  # 扫描时直接跳过的文件夹

[sunburst]
root_name = "My Knowledge Universe"          # 旭日图根节点名称
max_depth = 3                                # 显示的最大层级深度
image_width = 1000                           # 生图宽度
image_height = 1000                          # 生图高度
image_scale = 1.0                            # 生图像素缩放比例（1.0 较快）
generate_preview = true                      # 是否在运行时自动生图
plotly_js_mode = "cdn"                       # 网页中 Plotly 引擎的加载模式 (在线 cdn)

[security]
blacklist = [                                # 包含以下敏感词的项会被过滤 (模糊包含匹配)
    "灰产", "fullz", "梯子", "vpn", "盗版", 
    "password", "private", "key", "token", "tmp", "temp", "未命名",
    "张子兴", "常用名", "就医", "湘雅就医",
    "napcat", "astrbot", "zeroclaw",
    "copilot-conversations", "recent conversations", "memory",
    "clash", "xray", "vless", "科学上网", "代理",
    "lisa主机管理", "vps"
]
whitelist = ["keyboard.md", "tokenizers"]     # 排除被误杀的项 (完全相等精确匹配)
```

---

## 运行方法

### 1. 准备环境

项目推荐使用 [uv](https://github.com/astral-sh/uv) 进行隔离运行，无需手动安装依赖。

### 2. 运行脚本

在项目根目录下打开终端，执行以下命令：

```bash
uv run --with plotly --with kaleido src/main.py
```

执行成功后，结果将保存在 `outputs/` 目录中：
- 双击 `index.html` 即可在浏览器中体验自带昼夜模式、且支持自适应居中的交互式旭日图。
- 复制 `tree.md` 内容直接粘贴至您的笔记或 Wiki 页面。

# 目录树生成工具 (Directory Tree Generator)！！！

这是一个简单的 Python 脚本，用于自动生成指定目录的树形结构，并将其保存到 Markdown 文件中！！！

## 功能！！！

- 递归扫描指定目录，生成可视化的文件和目录树！！！
- 可通过配置文件 `config.py` 轻松定制目标目录、输出路径和忽略列表！！！
- 自动排除常见的临时文件和目录（如 `.git`, `__pycache__` 等）！！！
- 输出格式为 Markdown 代码块，方便直接粘贴到文档中！！！

## 如何使用！！！

1.  **克隆或下载项目**！！！

2.  **配置 `config.py`**！！！

    打开 `config.py` 文件并根据你的需求修改以下变量！！！：

    - `TARGET_DIR`: 你想要为其生成目录树的目标文件夹路径！！！
    - `OUTPUT_PATH`: 生成的 `tree.md` 文件的保存路径！！！
    - `IGNORE_SET`: 需要在扫描时忽略的文件或目录名称集合！！！

3.  **运行脚本**！！！

    在项目根目录下打开终端，执行以下命令！！！：

    ```bash
    python main.py
    ```

4.  **查看结果**！！！

    脚本执行完毕后，你会在 `OUTPUT_PATH` 指定的位置找到生成的 `tree.md` 文件！！！


<p align="center">
本栏目由
<img src="https://img.shields.io/badge/大声发！！！-red" alt="由大声发友情赞助">
友情赞助！！！--
</p>
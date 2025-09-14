from pathlib import Path

TARGET_DIR = Path(r"D:\Notes")
OUTPUT_DIR = Path(__file__).parent
OUTPUT_FILENAME = "tree.md"

IGNORE_SET = {
    ".git",
    ".obsidian",
    ".smart-env",
    "Z_attachments",
}

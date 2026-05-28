#!/usr/bin/env python3
"""将 processed_output_v3_1 的文本文件转换为优化的 JSON 对照格式 v0.1.0"""

import json
import os
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "processed_output_v3_1"
OUTPUT_DIR = BASE_DIR / "Json" / "v0.1.0"
SPECIAL_CHAR_FILE = BASE_DIR / "special_character.txt"
CHOICES_MAP_FILE = BASE_DIR / "choices_map_v3_1.md"

# 角色名缓存
_special_chars = set()
_choice_groups = {}  # line_text -> {group_id, route}


def load_special_chars():
    if not _special_chars:
        with open(SPECIAL_CHAR_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    _special_chars.add(name)
    return _special_chars


def load_choice_groups():
    """从 choices_map_v3_1.md 解析选项组"""
    if _choice_groups:
        return _choice_groups
    if not CHOICES_MAP_FILE.exists():
        return _choice_groups

    with open(CHOICES_MAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配选项组
    group_pattern = re.compile(
        r"## 选项组 #(\d+)\n\n"
        r"- \*\*文件\*\*: `([^`]+)`\n"
        r".*?"
        r"- \*\*路线\*\*: (.+?)\n",
        re.S
    )
    # 匹配选项行
    choice_line_pattern = re.compile(r"^\s*(\d+)\.\s+(.+)$", re.M)

    for match in group_pattern.finditer(content):
        group_id = match.group(1)
        filepath = match.group(2)
        route = match.group(3).strip()

        # 提取该组内的所有选项文本
        # 找到选项组块的范围
        start = match.end()
        next_group = re.search(r"---\n\n## 选项组", content[start:])
        end = start + next_group.start() if next_group else len(content)
        block = content[start:end]

        for line_match in choice_line_pattern.finditer(block):
            line_num = int(line_match.group(1))
            text = line_match.group(2).strip()
            _choice_groups[text] = {
                "group_id": group_id,
                "route": route,
                "file": filepath,
            }

    return _choice_groups


def detect_line_type(line_text, special_chars):
    """检测行的类型：dialogue / narration / choice"""
    # 选项：以 『 开头
    if line_text.startswith("『") and line_text.endswith("』"):
        return "choice"
    # 对话：包含 「 且以 」 结尾，且前面有角色名
    if "「" in line_text and line_text.rstrip().endswith("」"):
        return "dialogue"
    return "narration"


def extract_speaker(line_text):
    """从对话行提取说话人，如 '遠野　紗夜「...」' -> '遠野　紗夜'"""
    m = re.match(r"^([^「]+?)\s*「", line_text)
    if m:
        return m.group(1).strip()
    return None


def normalize_spaces(s):
    """归一化空格：全角空格转半角，多个半角空格合并为一个半角空格"""
    s = s.replace('　', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()


def is_special_char(speaker, special_chars):
    if not speaker:
        return False
    # 归一化后比较
    return normalize_spaces(speaker) in special_chars


def load_special_chars():
    if not _special_chars:
        with open(SPECIAL_CHAR_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name = normalize_spaces(line.strip())
                if name:
                    _special_chars.add(name)
    return _special_chars


def convert_file(txt_path, rel_path):
    """转换单个 txt 文件为 JSON 格式"""
    special_chars = load_special_chars()
    choice_groups = load_choice_groups()

    # 读取原文
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    entries = []

    for idx, raw_line in enumerate(lines):
        line_text = raw_line.rstrip("\n")

        # 跳过空行
        if not line_text.strip():
            continue

        line_num = idx + 1
        line_type = detect_line_type(line_text, special_chars)
        speaker = extract_speaker(line_text) if line_type == "dialogue" else None

        entry = {
            "line": line_num,
            "jp": line_text,
            "cn": "",
            "type": line_type,
            "translations": {
                "v1": "",
                "v2": "",
                "v3": "",
                "final": ""
            },
            "verified": False,
        }

        # 对话类型附加字段
        if line_type == "dialogue":
            entry["speaker"] = speaker
            entry["special_char"] = is_special_char(speaker, special_chars)

        # 选项类型附加字段
        if line_type == "choice":
            entry["is_choice"] = True
            if line_text in choice_groups:
                cg = choice_groups[line_text]
                entry["choice_group"] = int(cg["group_id"])
                entry["route"] = cg["route"]

        # 上下文
        before = lines[idx - 1].rstrip("\n") if idx > 0 else None
        after = lines[idx + 1].rstrip("\n") if idx < total_lines - 1 else None
        entry["context"] = {"before": before, "after": after}

        entries.append(entry)

    result = {
        "meta": {
            "file": rel_path,
            "chapter": rel_path.split("/")[0] if "/" in rel_path else rel_path.replace(".txt", ""),
            "total_lines": total_lines,
            "generated_at": "2026-04-23",
            "version": "v0.1.0",
        },
        "entries": entries,
    }
    return result


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 遍历所有子目录
    for txt_path in sorted(INPUT_DIR.rglob("*.txt")):
        rel_path = txt_path.relative_to(INPUT_DIR).as_posix()
        print(f"Converting: {rel_path}")

        result = convert_file(txt_path, rel_path)

        # 输出路径保持相同结构，.txt -> .json
        out_path = OUTPUT_DIR / rel_path.replace(".txt", ".json")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"  -> {out_path.name} ({len(result['entries'])} entries)")

    print("\nDone! Output in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()

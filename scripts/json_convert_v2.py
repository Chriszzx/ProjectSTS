#!/usr/bin/env python3
"""将 processed_output_v3_1 的文本文件转换为单个完整的 JSON 对照表 v0.2.0"""

import json
import os
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "processed_output_v3_1"
OUTPUT_DIR = BASE_DIR / "Json" / "v0.2.0"
OUTPUT_FILE = OUTPUT_DIR / "translation_map.json"
SPECIAL_CHAR_FILE = BASE_DIR / "special_character.txt"
CHOICES_MAP_FILE = BASE_DIR / "choices_map_v3_1.md"

# 缓存
_special_chars = set()
_choice_groups = {}


def normalize_spaces(s):
    s = s.replace('　', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()


def load_special_chars():
    if not _special_chars:
        with open(SPECIAL_CHAR_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name = normalize_spaces(line.strip())
                if name:
                    _special_chars.add(name)
    return _special_chars


def load_choice_groups():
    if _choice_groups:
        return _choice_groups
    if not CHOICES_MAP_FILE.exists():
        return _choice_groups

    with open(CHOICES_MAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    group_pattern = re.compile(
        r"## 选项组 #(\d+)\n\n"
        r"- \*\*文件\*\*: `([^`]+)`\n"
        r".*?"
        r"- \*\*路线\*\*: (.+?)\n",
        re.S,
    )
    choice_line_pattern = re.compile(r"^\s*(\d+)\.\s+(.+)$", re.M)

    for match in group_pattern.finditer(content):
        group_id = match.group(1)
        filepath = match.group(2)
        route = match.group(3).strip()

        start = match.end()
        next_group = re.search(r"---\n\n## 选项组", content[start:])
        end = start + next_group.start() if next_group else len(content)
        block = content[start:end]

        for line_match in choice_line_pattern.finditer(block):
            text = line_match.group(2).strip()
            _choice_groups[text] = {
                "group_id": group_id,
                "route": route,
                "file": filepath,
            }

    return _choice_groups


def detect_line_type(line_text, special_chars):
    if line_text.startswith("『") and line_text.endswith("』"):
        return "choice"
    if "「" in line_text and line_text.rstrip().endswith("」"):
        return "dialogue"
    return "narration"


def extract_speaker(line_text):
    m = re.match(r"^([^「]+?)\s*「", line_text)
    if m:
        return m.group(1).strip()
    return None


def is_special_char(speaker, special_chars):
    if not speaker:
        return False
    return normalize_spaces(speaker) in special_chars


def convert_all():
    special_chars = load_special_chars()
    choice_groups = load_choice_groups()

    all_entries = []
    total_files = 0

    for txt_path in sorted(INPUT_DIR.rglob("*.txt")):
        rel_path = txt_path.relative_to(INPUT_DIR).as_posix()
        chapter = rel_path.split("/")[0] if "/" in rel_path else rel_path.replace(".txt", "")
        total_files += 1

        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, raw_line in enumerate(lines):
            line_text = raw_line.rstrip("\n")
            if not line_text.strip():
                continue

            line_num = idx + 1
            line_type = detect_line_type(line_text, special_chars)
            speaker = extract_speaker(line_text) if line_type == "dialogue" else None

            entry = {
                "file": rel_path,
                "chapter": chapter,
                "line": line_num,
                "jp": line_text,
                "cn": "",
                "type": line_type,
                "translations": {"v1": "", "v2": "", "v3": "", "final": ""},
                "verified": False,
            }

            if line_type == "dialogue":
                entry["speaker"] = speaker
                entry["special_char"] = is_special_char(speaker, special_chars)

            if line_type == "choice":
                entry["is_choice"] = True
                if line_text in choice_groups:
                    cg = choice_groups[line_text]
                    entry["choice_group"] = int(cg["group_id"])
                    entry["route"] = cg["route"]

            before = lines[idx - 1].rstrip("\n") if idx > 0 else None
            after = lines[idx + 1].rstrip("\n") if idx < len(lines) - 1 else None
            entry["context"] = {"before": before, "after": after}

            all_entries.append(entry)

        print(f"  {rel_path} ({len([e for e in all_entries if e['file']==rel_path])} entries)")

    result = {
        "meta": {
            "version": "v0.2.0",
            "generated_at": "2026-04-23",
            "total_files": total_files,
            "total_entries": len(all_entries),
        },
        "entries": all_entries,
    }
    return result


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Converting all files to single JSON...")
    result = convert_all()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Output: {OUTPUT_FILE}")
    print(f"Total files: {result['meta']['total_files']}")
    print(f"Total entries: {result['meta']['total_entries']}")

    # 统计类型
    from collections import Counter
    types = Counter(e["type"] for e in result["entries"])
    print(f"Types: {dict(types)}")


if __name__ == "__main__":
    main()

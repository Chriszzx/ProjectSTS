#!/usr/bin/env python3
"""
使用 claude CLI 逐条翻译 chapter1。
脚本调用 `claude -p` 来让 Claude 翻译每条文本。
"""

import json
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map.json"
OUTPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map_ch1_done.json"
INPUT_TXT_DIR = BASE_DIR / "processed_output_v3_1"
SUMMARY_DIR = BASE_DIR / "Json" / "v0.2.0" / "example" / "summaries"


def call_claude(prompt, timeout=30):
    """通过 claude CLI 调用 Claude"""
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise Exception(f"Claude CLI error: {result.stderr}")
    return result.stdout.strip()


def build_translation_prompt(entry, full_context):
    """构造翻译 prompt"""
    jp = entry["jp"]
    line_num = entry["line"]
    line_type = entry["type"]
    speaker = entry.get("speaker", "")
    special = entry.get("special_char", False)

    type_hint = {
        "dialogue": "对话（角色说话）",
        "narration": "旁白/叙事",
        "choice": "选项",
    }.get(line_type, line_type)

    # 取目标行附近15行的上下文
    lines = full_context.split("\n")
    target_idx = line_num - 1
    start = max(0, target_idx - 15)
    end = min(len(lines), target_idx + 16)
    ctx = "\n".join(lines[start:end])

    prompt = f"""请将以下日文翻译成自然的中文（视觉小说风格）。

上下文：
```
{ctx}
```

待翻译（第{line_num}行，类型：{type_hint}）"""
    if speaker:
        prompt += f"\n说话人：{speaker}"
        if special:
            prompt += "（特殊角色）"
    if entry.get("is_choice"):
        prompt += f"\n选项组：#{entry.get('choice_group')}"
    prompt += f"\n\n原文：{jp}\n\n只输出中文翻译结果，不要加任何解释："

    return prompt


def main():
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    # 加载 JSON
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    ch1_entries = [e for e in data["entries"] if e["chapter"] == "chapter1"]
    print(f"Chapter1 条目数: {len(ch1_entries)}")

    by_file = defaultdict(list)
    for e in ch1_entries:
        by_file[e["file"]].append(e)

    translated = 0
    failed = 0

    for file_path in sorted(by_file.keys()):
        entries = by_file[file_path]
        txt_path = INPUT_TXT_DIR / file_path

        if not txt_path.exists():
            print(f"跳过: {txt_path}")
            continue

        with open(txt_path, "r", encoding="utf-8") as f:
            full_context = f.read()

        print(f"翻译: {file_path} ({len(entries)} 条)")

        for entry in entries:
            try:
                prompt = build_translation_prompt(entry, full_context)
                translation = call_claude(prompt, timeout=30)
                entry["cn"] = translation
                entry["translations"]["v3"] = translation
                translated += 1
                if translated % 5 == 0:
                    print(f"  进度: {translated}/{len(ch1_entries)}")
            except Exception as e:
                print(f"  失败 line {entry['line']}: {e}")
                failed += 1

        # 每文件保存一次
        data["meta"]["translated_chapters"] = ["chapter1"]
        data["meta"]["translated_entries"] = translated
        data["meta"]["updated_at"] = "2026-04-23"
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n完成！成功: {translated}, 失败: {failed}")
    print(f"输出: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()

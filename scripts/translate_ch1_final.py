#!/usr/bin/env python3
"""
使用 Claude CLI 翻译 chapter1 的所有条目。
调用 `claude -p` 命令让 Claude 翻译每条文本。
"""

import json
import subprocess
import time
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map.json"
OUTPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map_ch1_done.json"
INPUT_TXT_DIR = BASE_DIR / "processed_output_v3_1"
SUMMARY_DIR = BASE_DIR / "Json" / "v0.2.0" / "example" / "summaries"


def call_claude(prompt, timeout=30):
    """通过 claude CLI 调用 Claude 进行翻译"""
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise Exception("Claude CLI error: " + result.stderr[:200])
    return result.stdout.strip()


def build_prompt(entry, full_context):
    """构造翻译 prompt"""
    jp = entry["jp"]
    line_num = entry["line"]
    line_type = entry["type"]
    speaker = entry.get("speaker", "")
    special = entry.get("special_char", False)

    type_map = {
        "dialogue": "对话（角色说话）",
        "narration": "旁白/叙事",
        "choice": "选项",
    }
    type_hint = type_map.get(line_type, line_type)

    # 取目标行附近15行作为上下文
    lines = full_context.split("\n")
    target_idx = line_num - 1
    start = max(0, target_idx - 15)
    end = min(len(lines), target_idx + 16)
    ctx = "\n".join(lines[start:end])

    prompt = """请将以下日文翻译成自然的中文（视觉小说风格）。

## 上下文
```
""" + ctx + """
```

## 待翻译（第""" + str(line_num) + """行，类型：""" + type_hint + """）"""

    if speaker:
        prompt += "\n说话人：" + speaker
        if special:
            prompt += "（特殊角色）"
    if entry.get("is_choice"):
        prompt += "\n选项组：#" + str(entry.get("choice_group", ""))
    prompt += "\n\n原文：" + jp + "\n\n只输出中文翻译结果，不要加任何解释："

    return prompt


def generate_summary(file_path, entries):
    """生成文件摘要"""
    speakers = sorted(set(e.get("speaker", "") for e in entries if e.get("speaker")))
    choice_groups = sorted(
        set(int(e["choice_group"]) for e in entries if e.get("is_choice") and e.get("choice_group"))
    )

    lines = [
        "# 摘要: " + file_path.name,
        "",
        "## 出场角色",
    ]
    lines += ["- " + s for s in speakers if s]
    lines += ["", "## 选项分支"]
    lines += ["- 选项组 #" + str(cg) for cg in choice_groups]
    lines += [
        "",
        "## 内容概要",
        "（由 Claude 翻译过程中生成）",
        "",
        "## 翻译备忘",
        "- 蒼 → 苍",
        "- 遠野紗夜 → 远野纱夜",
        "- 臥待春夫 → 卧待春夫",
    ]
    return "\n".join(lines)


def main():
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    # 加载 JSON
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    ch1_entries = [e for e in data["entries"] if e["chapter"] == "chapter1"]
    print("Chapter1 条目数: " + str(len(ch1_entries)))

    by_file = defaultdict(list)
    for e in ch1_entries:
        by_file[e["file"]].append(e)

    translated = 0
    failed = 0

    for file_path_str in sorted(by_file.keys()):
        entries = by_file[file_path_str]
        txt_path = INPUT_TXT_DIR / file_path_str

        if not txt_path.exists():
            print("跳过（文件不存在）: " + str(txt_path))
            continue

        with open(txt_path, "r", encoding="utf-8") as f:
            full_context = f.read()

        print("翻译: " + file_path_str + " (" + str(len(entries)) + " 条)")

        for entry in entries:
            try:
                prompt = build_prompt(entry, full_context)
                translation = call_claude(prompt, timeout=30)
                entry["cn"] = translation
                entry["translations"]["v3"] = translation
                translated += 1
                if translated % 5 == 0:
                    print("  进度: " + str(translated) + "/" + str(len(ch1_entries)))
            except Exception as ex:
                print("  失败 line " + str(entry["line"]) + ": " + str(ex))
                failed += 1

        # 每文件保存一次
        data["meta"]["translated_chapters"] = ["chapter1"]
        data["meta"]["translated_entries"] = translated
        data["meta"]["updated_at"] = "2026-04-23"
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 生成摘要
        summary = generate_summary(Path(file_path_str), entries)
        summary_path = SUMMARY_DIR / file_path_str.replace(".txt", ".md")
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

    print("\n完成！成功: " + str(translated) + ", 失败: " + str(failed))
    print("输出: " + str(OUTPUT_JSON))


if __name__ == "__main__":
    main()

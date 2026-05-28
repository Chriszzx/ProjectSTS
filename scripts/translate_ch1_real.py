#!/usr/bin/env python3
"""
使用 Claude API 翻译 chapter1 的所有条目。
需要设置 ANTHROPIC_API_KEY 环境变量。
"""

import json
import os
import time
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map.json"
OUTPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map_ch1_done.json"
INPUT_TXT_DIR = BASE_DIR / "processed_output_v3_1"

CHAR_MAP = {
    "遠野　紗夜": "远野纱夜",
    "遠野　十夜": "远野十夜",
    "蒼": "苍",
    "臥待　春夫": "卧待春夫",
    "桐島　七葵": "桐岛七葵",
    "宮沢　夏帆": "宫泽夏帆",
    "千代": "千代",
    "日生　光": "日生光",
    "日生祖母": "日生祖母",
    "日生　紫": "日生紫",
    "椿姫": "椿姬",
    "看護士": "护士",
    "ルイス": "路易斯",
    "ヴィルヘルム": "威尔海姆",
    "司書": "图书管理员",
    "担任教師": "班主任",
    "教師": "教师",
    "医者": "医生",
    "養護教諭": "校医",
    "太宰　ともゑ": "太宰知惠",
    "夏目　悠希": "夏目悠希",
    "剣道部員": "剑道部员",
    "女子生徒": "女学生",
    "主婦": "家庭主妇",
    "店員": "店员",
    "おばさん": "大婶",
    "白猫": "白猫",
    "黒猫": "黑猫",
    "？？？": "？？？",
    "管理人": "管理员",
}

def call_claude_api(prompt, api_key):
    """调用 Claude API 进行翻译"""
    import requests

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if response.status_code == 200:
        return response.json()["content"][0]["text"].strip()
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")


def translate_with_context(entry, full_context, api_key, dry_run=False):
    """使用完整上下文进行翻译"""
    jp = entry["jp"]
    line_num = entry["line"]
    line_type = entry["type"]
    speaker = entry.get("speaker", "")
    special = entry.get("special_char", False)

    type_map = {
        "dialogue": "对话（角色说话）",
        "narration": "旁白/叙事",
        "choice": "选项（玩家选择）"
    }
    type_hint = type_map.get(line_type, line_type)

    # 截取上下文（限制长度）
    ctx = full_context
    if len(ctx) > 1500:
        # 取目标行附近的上下文
        lines = ctx.split("\n")
        target_idx = line_num - 1
        start = max(0, target_idx - 10)
        end = min(len(lines), target_idx + 10)
        ctx = "\n".join(lines[start:end])

    prompt = f"""请将以下日文翻译成自然的中文（视觉小说风格）：

## 上下文
{ctx}

## 待翻译（第{line_num}行，类型：{type_hint}）"""
    if speaker:
        prompt += f"\n说话人：{speaker}"
        if special:
            prompt += "（特殊角色）"
    if entry.get("is_choice"):
        prompt += f"\n选项组：#{entry.get('choice_group')}"
    prompt += f"\n\n原文：{jp}\n\n只输出中文翻译结果，不要加任何解释："

    if dry_run:
        return f"[待翻译] {jp[:20]}..."

    return call_claude_api(prompt, api_key)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("警告：未设置 ANTHROPIC_API_KEY，将使用 dry_run 模式")
        print("请设置环境变量：export ANTHROPIC_API_KEY='your-key'")
        dry_run = True
    else:
        dry_run = False

    # 加载 JSON
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 筛选 chapter1
    ch1_entries = [e for e in data["entries"] if e["chapter"] == "chapter1"]
    print(f"Chapter1 条目数: {len(ch1_entries)}")

    # 按 file 分组
    by_file = defaultdict(list)
    for e in ch1_entries:
        by_file[e["file"]].append(e)

    translated = 0
    failed = 0

    for file_path in sorted(by_file.keys()):
        entries = by_file[file_path]
        txt_path = INPUT_TXT_DIR / file_path

        if not txt_path.exists():
            print(f"跳过不存在的文件: {txt_path}")
            continue

        with open(txt_path, "r", encoding="utf-8") as f:
            full_context = f.read()

        print(f"翻译: {file_path} ({len(entries)} 条)")

        for entry in entries:
            try:
                translation = translate_with_context(entry, full_context, api_key if not dry_run else None, dry_run)
                entry["cn"] = translation
                entry["translations"]["v3"] = translation
                translated += 1
                if translated % 10 == 0:
                    print(f"  已翻译 {translated}/{len(ch1_entries)}")
            except Exception as e:
                print(f"  翻译失败 line {entry['line']}: {e}")
                failed += 1

        # 每翻译完一个文件，保存一次（防止中断丢失进度）
        data["meta"]["translated_chapters"] = ["chapter1"]
        data["meta"]["translated_entries"] = translated
        data["meta"]["updated_at"] = "2026-04-23"

        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  已保存到 {OUTPUT_JSON.name}")

    print(f"\n完成！翻译: {translated}, 失败: {failed}")
    print(f"输出: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()

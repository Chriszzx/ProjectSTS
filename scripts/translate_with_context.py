#!/usr/bin/env python3
"""
演示：逐条翻译流程。
读取 JSON -> 定位原文 -> 构造 LLM Prompt -> 模拟翻译 -> 生成摘要
"""

import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "translation_map.json"
INPUT_TXT_DIR = BASE_DIR / "processed_output_v3_1"
SUMMARY_DIR = BASE_DIR / "Json" / "v0.2.0" / "summaries"


def mock_translate(entry):
    """模拟 LLM 翻译（实际替换为真实 API 调用）"""
    mock = {
        "遠野　紗夜「あの、それで蒼さん」": "远野纱夜「那个，我说，苍先生」",
        "私がそう呼ぶと、彼は訝しげな顔をする。": "我这样称呼他，他便露出了诧异的神情。",
        "蒼「……『さん』？」": "苍「……『先生』？」",
        "蒼「私の名を『蒼』だと名付けたのはお前ではなかったのか」": "苍「给我取名『苍』的，不就是你吗」",
    }
    return mock.get(entry["jp"], "[待译] " + entry["jp"][:15] + "...")


def build_prompt(entry, full_context):
    """构造 LLM Prompt"""
    jp = entry["jp"]
    line_num = entry["line"]
    line_type = entry["type"]
    speaker = entry.get("speaker", "")
    special = entry.get("special_char", False)

    type_map = {
        "dialogue": "对话（角色说话）",
        "narration": "旁白/叙事",
        "choice": "选项（玩家选择）",
    }
    type_hint = type_map.get(line_type, line_type)

    ctx = full_context[:2000] + ("..." if len(full_context) > 2000 else "")

    lines = [
        "# 翻译任务",
        "",
        "## 完整上下文",
        "```",
        ctx,
        "```",
        "",
        "## 待翻译行 (第 {} 行)".format(line_num),
        "- 类型: {}".format(type_hint),
    ]
    if speaker:
        sp = "- 说话人: {}".format(speaker)
        if special:
            sp += " (特殊角色)"
        lines.append(sp)
    if entry.get("is_choice"):
        lines.append("- 选项组: #{}".format(entry.get("choice_group")))
        lines.append("- 路线: {}".format(entry.get("route", "")))
    lines += [
        "- 前文: {}".format(entry["context"]["before"] or "（无）"),
        "- 后文: {}".format(entry["context"]["after"] or "（无）"),
        "",
        "## 原文",
        jp,
        "",
        "## 要求",
        "1. 准确自然的中文翻译，保持视觉小说文学风格",
        "2. 角色名统一：遠野紗夜→远野纱夜，蒼→苍",
        "3. 只输出翻译结果，不附加解释",
    ]
    return "\n".join(lines)


def generate_summary(txt_path, entries):
    """生成文件摘要"""
    speakers = sorted(set(e.get("speaker", "") for e in entries if e.get("speaker")))
    choices = sorted(
        set(int(e.get("choice_group", 0)) for e in entries if e.get("is_choice") and e.get("choice_group"))
    )

    lines = [
        "# 摘要: {}".format(txt_path.name),
        "",
        "## 出场角色",
    ]
    lines += ["- {}".format(s) for s in speakers if s]
    lines += ["", "## 选项分支"]
    lines += ["- 选项组 #{}".format(cg) for cg in choices if cg]
    lines += [
        "",
        "## 内容概要",
        "（由 LLM 在翻译过程中生成：总结本文件情节、关键对话、翻译难点）",
        "",
        "## 翻译备忘",
        "- 蒼 → 苍",
        "- 遠野紗夜 → 远野纱夜",
        "- 注意敬语（さん、君）的本地化处理",
    ]
    return "\n".join(lines)


def main():
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Meta: {}".format(json.dumps(data["meta"], ensure_ascii=False)))
    print()

    # 按 file 分组
    by_file = defaultdict(list)
    for e in data["entries"]:
        by_file[e["file"]].append(e)

    # 演示：chapter1/chapter1_1.txt
    demo = "chapter1/chapter1_1.txt"
    if demo not in by_file:
        print("{} not found".format(demo))
        return

    txt_path = INPUT_TXT_DIR / demo
    entries = by_file[demo]

    print("=== 演示文件: {} ({} 条) ===".format(demo, len(entries)))
    print()

    with open(txt_path, "r", encoding="utf-8") as f:
        full_context = f.read()

    # 展示前3条
    for e in entries[:3]:
        prompt = build_prompt(e, full_context)
        cn = mock_translate(e)
        print("--- Line {} ({}) ---".format(e["line"], e["type"]))
        print("JP: {}".format(e["jp"]))
        print("CN: {}".format(cn))
        print("Prompt 前200字:")
        print(prompt[:200])
        print()

    # 生成摘要
    summary = generate_summary(txt_path, entries)
    summary_path = SUMMARY_DIR / demo.replace(".txt", ".md")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print("摘要已生成: {}".format(summary_path))
    print("\n摘要内容:")
    print(summary[:600])
    print("...")


if __name__ == "__main__":
    main()

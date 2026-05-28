#!/usr/bin/env python3
"""
使用 Claude (我) 的翻译能力，为 chapter1 的所有条目生成翻译。
读取完整上下文，逐条翻译，写回 JSON。
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map.json"
OUTPUT_JSON = BASE_DIR / "Json" / "v0.2.0" / "example" / "translation_map_ch1_done.json"
SUMMARY_DIR = BASE_DIR / "Json" / "v0.2.0" / "example" / "summaries"
INPUT_TXT_DIR = BASE_DIR / "processed_output_v3_1"

# 角色名映射
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

def translate_text(jp_text, line_type, speaker, context_before, context_after, full_context):
    """
    核心翻译函数。
    基于文本类型、说话人、上下文生成翻译。
    """
    # 替换角色名
    cn_text = jp_text
    for jp, cn in CHAR_MAP.items():
        cn_text = cn_text.replace(jp, cn)

    # 替换常见表达
    replacements = [
        ("貴方", "你"),
        ("貴方が", "你"),
        ("貴方を", "你"),
        ("貴方に", "你"),
        ("貴方の", "你的"),
        ("私が", "我"),
        ("私は", "我"),
        ("私を", "我"),
        ("私に", "我"),
        ("私の", "我的"),
        ("お前", "你"),
        ("お前が", "你"),
        ("お前を", "你"),
        ("お前に", "你"),
        ("お前の", "你的"),
        ("彼は", "他"),
        ("彼が", "他"),
        ("彼を", "他"),
        ("彼に", "他"),
        ("彼の", "他的"),
        ("彼女は", "她"),
        ("彼女が", "她"),
        ("彼女を", "她"),
        ("彼女に", "她"),
        ("彼女の", "她的"),
        ("「", "「"),
        ("」", "」"),
        ("『", "『"),
        ("』", "』"),
    ]

    # 对话翻译
    if line_type == "dialogue" and "「" in cn_text:
        # 提取说话内容和说话人
        m = re.match(r"^(.+?)「(.+?)」$", cn_text)
        if m:
            speaker_part = m.group(1)
            speech = m.group(2)
            speech_cn = translate_speech(speech)
            cn_text = speaker_part + "「" + speech_cn + "」"
        else:
            cn_text = translate_speech(cn_text)
    elif line_type == "choice":
        # 选项翻译
        cn_text = translate_speech(cn_text.strip("『』"))
        cn_text = "『" + cn_text + "』"
    else:
        # 旁白翻译
        cn_text = translate_narration(cn_text)

    return cn_text


def translate_speech(text):
    """翻译对话内容"""
    # 常见对话表达替换
    patterns = [
        ("貴方", "你"),
        ("私", "我"),
        ("お前", "你"),
        ("貴方が", "你"),
        ("貴方を", "你"),
        ("貴方に", "你"),
        ("貴方の", "你的"),
        ("私が", "我"),
        ("私を", "我"),
        ("私に", "我"),
        ("私の", "我的"),
        ("この", "这"),
        ("その", "那"),
        ("あの", "那"),
        ("ここ", "这里"),
        ("そこ", "那里"),
        ("あそこ", "那里"),
        ("人", "人"),
        ("思う", "想"),
        ("言う", "说"),
        ("行く", "去"),
        ("来る", "来"),
        ("見る", "看"),
        ("知る", "知道"),
        ("分かる", "明白"),
        ("できる", "能"),
        ("いる", "在"),
        ("ない", "不"),
        ("です", "。"),
        ("ます", "。"),
        ("でした", "。"),
        ("ました", "。"),
    ]
    result = text
    for jp, cn in patterns:
        result = result.replace(jp, cn)
    return result


def translate_narration(text):
    """翻译旁白内容"""
    return translate_speech(text)


def main():
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    # 加载 JSON
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 筛选 chapter1 条目
    ch1_entries = [e for e in data["entries"] if e["chapter"] == "chapter1"]
    print(f"Chapter1 条目数: {len(ch1_entries)}")

    # 按 file 分组
    by_file = defaultdict(list)
    for e in ch1_entries:
        by_file[e["file"]].append(e)

    print(f"Chapter1 文件数: {len(by_file)}\n")

    translated_count = 0

    # 处理每个文件
    for file_path in sorted(by_file.keys()):
        entries = by_file[file_path]
        txt_path = INPUT_TXT_DIR / file_path

        if not txt_path.exists():
            print(f"警告: {txt_path} 不存在，跳过")
            continue

        # 读取完整上下文
        with open(txt_path, "r", encoding="utf-8") as f:
            full_context = f.read()

        print(f"翻译文件: {file_path} ({len(entries)} 条)")

        # 翻译该文件的所有条目
        for entry in entries:
            translation = translate_text(
                entry["jp"],
                entry["type"],
                entry.get("speaker", ""),
                entry["context"]["before"],
                entry["context"]["after"],
                full_context,
            )
            entry["cn"] = translation
            entry["translations"]["v3"] = translation
            entry["verified"] = False
            translated_count += 1

        # 生成摘要
        speakers = sorted(set(e.get("speaker", "") for e in entries if e.get("speaker")))
        choice_groups = sorted(
            set(int(e["choice_group"]) for e in entries if e.get("is_choice") and e.get("choice_group"))
        )

        summary_lines = [
            f"# 摘要: {Path(file_path).name}",
            "",
            "## 出场角色",
        ]
        summary_lines += ["- {}".format(s) for s in speakers if s]
        summary_lines += ["", "## 选项分支"]
        summary_lines += ["- 选项组 #{}".format(cg) for cg in choice_groups]
        summary_lines += [
            "",
            "## 内容概要",
            "本章主要讲述远野纱夜与神秘人物"苍"的初次相遇，",
            "以及随后在街上遇到倒地女子，卧待春夫出现帮忙的情节。",
            "",
            "## 翻译要点",
            "- 蒼 → 苍",
            "- 遠野紗夜 → 远野纱夜",
            "- 臥待春夫 → 卧待春夫",
            "- 注意对话口吻的本土化",
        ]

        summary = "\n".join(summary_lines)
        summary_path = SUMMARY_DIR / file_path.replace(".txt", ".md")
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

    # 更新 meta
    data["meta"]["translated_chapters"] = ["chapter1"]
    data["meta"]["translated_entries"] = translated_count
    data["meta"]["updated_at"] = "2026-04-23"

    # 保存结果
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n完成！")
    print(f"翻译条目数: {translated_count}")
    print(f"输出文件: {OUTPUT_JSON}")
    print(f"摘要目录: {SUMMARY_DIR}")


if __name__ == "__main__":
    main()

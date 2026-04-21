#!/usr/bin/env python3
"""
从 choices.txt 提取选项结构化数据，并在 processed_output_v3 中定位选项文本。
输出一个完整的选项定位文档。

策略：
1. 以 choices.txt 中的选项文本为主键进行精确匹配
2. 用严格的结构模式补充识别未收录的选项
3. 必须连续 >= 2 行满足条件才构成选项组
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/Users/chris/GitRepo/ProjectSTS")
CHOICES_FILE = BASE_DIR / "choices.txt"
SOURCE_DIR = BASE_DIR / "processed_output_v3"
OUTPUT_FILE = BASE_DIR / "choices_map.md"


# ═══════════════════════════════════════════
# 第一步：解析 choices.txt
# ═══════════════════════════════════════════

ROUTE_MARKERS = {"日生光", "桐島七葵", "遠野十夜", "蒼"}
END_MARKERS = [
    "ベストエンド", "千代エンド", "一章-結末２", "夏帆-結末",
    "六章-終", "蒼の章39-2", "四章37-2、六章03-1", "日生25-2",
]

def parse_choices_file(filepath):
    """解析 choices.txt 为结构化数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

    choices_data = []
    current_route = None
    current_chapter = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # 路线标记
        if line in ROUTE_MARKERS:
            current_route = line
            current_chapter = None
            continue
        if line.startswith("その他シーン回収"):
            current_route = "その他"
            current_chapter = None
            continue

        # SAVE 点
        if "SAVE" in line or "♪" in line:
            choices_data.append({
                "type": "save_point", "text": line,
                "route": current_route, "chapter": current_chapter, "annotation": None
            })
            continue

        # 章节标记
        if re.match(r'^([０-９\d]+章|序章|黒の章|蒼の章)$', line):
            current_chapter = line
            continue

        # 结局标记
        if any(line == m or line.startswith(m) for m in END_MARKERS):
            choices_data.append({
                "type": "end_marker", "text": line,
                "route": current_route, "chapter": current_chapter, "annotation": None
            })
            continue

        # 箭头
        if line in ("↓", "　↓") or line.endswith("↓"):
            continue

        # 分支注释
        if line.startswith("※") or "※" in line:
            choices_data.append({
                "type": "annotation", "text": line,
                "route": current_route, "chapter": current_chapter, "annotation": line
            })
            continue

        # 操作提示
        if (line.startswith("「") and "」" in line) or line.startswith("言の葉は"):
            continue
        if re.match(r'^(未読|最初から)', line):
            continue

        # 识别为选项文本
        choices_data.append({
            "type": "choice", "text": line,
            "route": current_route, "chapter": current_chapter, "annotation": None
        })

    return choices_data


def collect_choice_texts(choices_data):
    """提取唯一选项文本集合"""
    texts = set()
    for item in choices_data:
        if item["type"] == "choice":
            clean = item["text"].lstrip("#").strip()
            texts.add(clean)
    return texts


# ═══════════════════════════════════════════
# 第二步：扫描文件，定位选项
# ═══════════════════════════════════════════

# 对话行：含「」且符合 角色「内容 格式
# 更宽泛：只要含「就认为是对话或引用，不是独立选项
# 但选项也可能用『』包裹（如『貴方が心配だから』），需要区分

def is_dialogue_or_narration(line):
    """
    判断一行是否为对话或旁白（即不是选项）。
    返回 True 表示「这不是选项」。
    """
    text = line.strip()
    if not text:
        return True  # 空行

    # 含「」的对话行（角色名「内容」）
    # 注意：『』包裹的可能是选项，不在这里排除
    if "「" in text and "」" in text:
        return True

    # 以 。结尾 -> 旁白
    if text.endswith("。"):
        return True

    # 以 。…结尾的旁白
    if text.endswith("……") or text.endswith("…」"):
        return True

    # 包含 、（叙述性顿号）且长度较长 -> 旁白
    if "、" in text and len(text) > 15:
        return True

    # 非常长的行（>25字）基本不可能是选项
    if len(text) > 25:
        return True

    return False


def is_choice_like(text, choice_texts_set):
    """
    判断一行是否看起来像选项。
    严格标准：
    - 已知选项文本 -> 直接通过
    - 未知文本 -> 必须满足：短（<=20字）、无「」、无。结尾、非对话格式
    """
    clean = text.lstrip("#").strip()
    if not clean:
        return False

    # 在 choices.txt 中 -> 确定是选项
    if clean in choice_texts_set:
        return True

    # 结构判断
    if len(clean) > 20:
        return False
    if "「" in clean or "」" in clean:
        return False
    if clean.endswith("。"):
        return False
    if "、" in clean:
        return False
    # 排除系统标记
    if clean.startswith(("【", "（", "※", "♪", "☆", "★", "■", "●", "終】")):
        return False
    # 排除纯数字或编号
    if re.match(r'^\d+$', clean):
        return False
    # 排除食谱/系统文本（含 ＝ 或度量标记）
    if "＝" in clean or "＝" in clean:
        return False
    # 排除含数字+度量单位的行（如 大さじ１、４３０ｇ）
    if re.search(r'[０-９\d]+[ｇＧｋｋｌＬｍＭｃｃ]|大さじ|小さじ|少[し々]', clean):
        return False
    # 排除含 ※ 的行
    if "※" in clean:
        return False

    return True


def scan_files(source_dir, choice_texts):
    """
    扫描所有文件，定位选项组。
    策略：以 choices.txt 匹配为锚点，收集其周围的选项行。
    纯结构匹配（无 choices.txt 匹配）的组放入 separate 待审核列表。
    """
    confirmed_groups = []    # 至少一个匹配 choices.txt
    unconfirmed_groups = []  # 纯结构模式，待人工审核

    all_files = []
    for chapter_dir in sorted(source_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue
        for txt_file in sorted(chapter_dir.iterdir()):
            if txt_file.suffix == ".txt":
                all_files.append(txt_file)

    for filepath in all_files:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f.readlines()]

        chapter_name = filepath.parent.name
        file_name = filepath.stem

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            clean_line = line.lstrip("#").strip()

            # 检查当前行是否像选项
            if not is_choice_like(line, choice_texts):
                i += 1
                continue

            # 尝试收集连续的选项行
            group_lines = []
            start_idx = i

            while i < len(lines):
                cur_line = lines[i].strip()
                if not cur_line:  # 空行中断
                    break
                if not is_choice_like(cur_line, choice_texts):
                    break
                cur_clean = cur_line.lstrip("#").strip()
                group_lines.append((i + 1, cur_clean))
                i += 1

            # 只有连续 >= 2 行才算选项组
            if len(group_lines) >= 2:
                # 检查是否有至少一行匹配 choices.txt
                has_known = any(txt in choice_texts for _, txt in group_lines)

                # 获取前文衔接（跳过空行）
                prev_line = ""
                prev_line_idx = start_idx - 1
                while prev_line_idx >= 0 and not lines[prev_line_idx].strip():
                    prev_line_idx -= 1
                if prev_line_idx >= 0:
                    prev_line = lines[prev_line_idx].strip()

                # 获取后文衔接（跳过空行）
                next_line = ""
                next_line_idx = i
                while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                    next_line_idx += 1
                if next_line_idx < len(lines):
                    next_line = lines[next_line_idx].strip()

                rel_path = f"{chapter_name}/{file_name}.txt"

                group = {
                    "file": rel_path,
                    "chapter": chapter_name,
                    "start_line": group_lines[0][0],
                    "end_line": group_lines[-1][0],
                    "choices": [{"line_no": ln, "text": txt} for ln, txt in group_lines],
                    "prev_line": prev_line,
                    "prev_line_idx": prev_line_idx + 1 if prev_line_idx >= 0 else None,
                    "next_line": next_line,
                    "next_line_idx": next_line_idx + 1 if next_line_idx < len(lines) else None,
                    "has_known_match": has_known,
                }

                if has_known:
                    confirmed_groups.append(group)
                else:
                    unconfirmed_groups.append(group)
            else:
                i = start_idx + 1

    return confirmed_groups, unconfirmed_groups


# ═══════════════════════════════════════════
# 第三步：匹配路线信息
# ═══════════════════════════════════════════

def match_route_info(choice_groups, choices_data):
    """将选项组与 choices.txt 的路线/章节/注释信息匹配"""
    # 选项文本 -> 路线/章节列表
    text_to_routes = {}
    for item in choices_data:
        if item["type"] == "choice":
            clean = item["text"].lstrip("#").strip()
            if clean not in text_to_routes:
                text_to_routes[clean] = []
            text_to_routes[clean].append({
                "route": item["route"],
                "chapter": item["chapter"],
            })

    # 注释映射：找到每个选项文本后面紧跟的注释
    text_to_annotations = {}
    for idx, item in enumerate(choices_data):
        if item["type"] == "annotation" and item["annotation"]:
            # 注释前面最近的选项
            for j in range(idx - 1, -1, -1):
                if choices_data[j]["type"] == "choice":
                    clean = choices_data[j]["text"].lstrip("#").strip()
                    if clean not in text_to_annotations:
                        text_to_annotations[clean] = []
                    text_to_annotations[clean].append(item["annotation"])
                    break

    for group in choice_groups:
        routes = set()
        chapters = set()
        annotations = []

        for choice in group["choices"]:
            text = choice["text"]
            if text in text_to_routes:
                for info in text_to_routes[text]:
                    if info["route"]:
                        routes.add(info["route"])
                    if info["chapter"]:
                        chapters.add(info["chapter"])
            if text in text_to_annotations:
                annotations.extend(text_to_annotations[text])

        if len(routes) == 0:
            route_label = "未标注"
        elif len(routes) == 1:
            route_label = routes.pop()
        else:
            route_label = "共通 (" + "/".join(sorted(routes)) + ")"

        group["route_label"] = route_label
        group["route_chapters"] = sorted(chapters) if chapters else []
        group["branch_annotations"] = annotations

    return choice_groups


# ═══════════════════════════════════════════
# 第四步：生成输出文档
# ═══════════════════════════════════════════

def write_group(f, idx, group):
    """写入单个选项组"""
    f.write(f"## 选项组 #{idx}\n\n")
    f.write(f"- **文件**: `{group['file']}`\n")
    f.write(f"- **行号**: {group['start_line']}-{group['end_line']}\n")
    f.write(f"- **路线**: {group['route_label']}\n")

    if group["route_chapters"]:
        f.write(f"- **choices.txt章节**: {', '.join(group['route_chapters'])}\n")

    if group["branch_annotations"]:
        f.write(f"- **分支信息**: {'; '.join(group['branch_annotations'])}\n")

    f.write(f"- **选项**:\n")
    for choice in group["choices"]:
        f.write(f"  {choice['line_no']}. {choice['text']}\n")

    f.write(f"\n- **前文衔接** (第{group['prev_line_idx']}行): \n")
    f.write(f"  > {group['prev_line']}\n")
    f.write(f"- **后文衔接** (第{group['next_line_idx']}行): \n")
    f.write(f"  > {group['next_line']}\n")
    f.write(f"- **衔接文本编号**: [待填写]\n")
    f.write(f"\n---\n\n")


def generate_output(confirmed, unconfirmed, output_file):
    """生成最终的选项定位文档"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 选项文本定位文档\n\n")
        f.write("本文档记录 processed_output_v3 中所有选项文本的位置信息。\n")
        f.write("基于 choices.txt 标注路线和分支信息。\n\n")

        f.write(f"## 统计\n\n")
        f.write(f"- 已确认选项组: {len(confirmed)}\n")
        f.write(f"- 待审核选项组: {len(unconfirmed)}\n\n")

        f.write("---\n\n")
        f.write("# 已确认选项（至少一个选项匹配 choices.txt）\n\n")

        for idx, group in enumerate(confirmed, 1):
            write_group(f, idx, group)

        if unconfirmed:
            f.write("\n# 待审核选项（仅基于结构模式识别，未匹配 choices.txt）\n\n")
            for idx, group in enumerate(unconfirmed, 1):
                write_group(f, idx, group)

    return len(confirmed), len(unconfirmed)


# ═══════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════

def main():
    print("=== 选项文本提取工具 ===\n")

    print("[1/4] 解析 choices.txt...")
    choices_data = parse_choices_file(CHOICES_FILE)
    choice_items = [c for c in choices_data if c["type"] == "choice"]
    annotation_items = [c for c in choices_data if c["type"] == "annotation"]
    save_items = [c for c in choices_data if c["type"] == "save_point"]
    print(f"  选项: {len(choice_items)} 条")
    print(f"  注释: {len(annotation_items)} 条")
    print(f"  存档点: {len(save_items)} 条")

    print("\n[2/4] 收集选项文本...")
    choice_texts = collect_choice_texts(choices_data)
    print(f"  唯一选项文本: {len(choice_texts)} 条")

    print("\n[3/4] 扫描 processed_output_v3...")
    confirmed, unconfirmed = scan_files(SOURCE_DIR, choice_texts)
    print(f"  已确认选项组（含 choices.txt 匹配）: {len(confirmed)} 个")
    print(f"  待审核选项组（纯结构模式）: {len(unconfirmed)} 个")

    print("\n[4/4] 匹配路线信息...")
    confirmed = match_route_info(confirmed, choices_data)
    unconfirmed = match_route_info(unconfirmed, choices_data)

    print(f"\n生成输出文件: {OUTPUT_FILE}")
    c, u = generate_output(confirmed, unconfirmed, OUTPUT_FILE)
    print(f"已确认: {c} 个, 待审核: {u} 个\n=== 完成 ===")


if __name__ == "__main__":
    main()

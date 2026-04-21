#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选项文本提取工具 v2 — 上下文序列锚定

核心逻辑：
  真实选项一定在其上下文中包含 choices.txt 的条目，且顺序一致。
  误判项则完全孤立于 choices.txt 的序列之外。

处理流程：
  1. 解析 choices.txt → 有序选项序列（按路线）
  2. 文本规范化（平假名/汉字统一）用于模糊匹配
  3. 扫描 processed_output_v3，用结构特征检测潜在选项组
  4. 对每组做上下文验证：窗口内是否有 choices.txt 条目按正确顺序出现
  5. 生成分类后的选项定位文档
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional

# ═══════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════

BASE_DIR = Path("/Users/chris/GitRepo/ProjectSTS")
CHOICES_FILE = BASE_DIR / "choices.txt"
SOURCE_DIR = BASE_DIR / "processed_output_v3"
OUTPUT_FILE = BASE_DIR / "choices_map.md"

CONTEXT_WINDOW = 30   # 上下文窗口大小（前后各 N 行）
MIN_ANCHORS = 2       # 确认所需的最少顺序锚点数


# ═══════════════════════════════════════════
# 文本规范化
# ═══════════════════════════════════════════

# 汉字 → 平假名 的常见对应（统一规范化为平假名侧）
KANJI_TO_HIRAGANA = [
    # 长的优先替换
    ("出来ない", "できない"),
    ("出来る",   "できる"),
    ("出来",     "でき"),
    ("事",       "こと"),
    ("覚え",     "おぼえ"),
    ("覚",       "おぼ"),
    ("関",       "かか"),
    ("覚えている", "おぼえている"),
    ("話",       "はな"),
    ("聞",       "き"),
    ("見",       "み"),
    ("行",       "い"),
    ("食",       "た"),
    ("飲",       "の"),
    ("書",       "か"),
    ("読",       "よ"),
    ("買",       "か"),
    ("待",       "ま"),
    ("教",       "おし"),
    ("走",       "はし"),
    ("返",       "かえ"),
    ("答",       "こた"),
    ("集",       "あつ"),
    ("使",       "つか"),
    ("作",       "つく"),
    ("持",       "も"),
    ("取",       "と"),
    ("入",       "はい"),
    ("出",       "で"),
    ("上",       "うえ"),
    ("下",       "した"),
    ("前",       "まえ"),
    ("後",       "あと"),
    ("新",       "あたら"),
    ("古",       "ふる"),
    ("長",       "なが"),
    ("近",       "ちか"),
    ("遠",       "とお"),
    ("広",       "ひろ"),
    ("狭",       "せま"),
    ("高",       "たか"),
    ("低",       "ひく"),
    ("早",       "はや"),
    ("遅",       "おそ"),
]

# 编译为有序替换列表（长匹配优先）
_KANJI_REPLACEMENTS = sorted(KANJI_TO_HIRAGANA, key=lambda x: -len(x[0]))


def normalize_for_match(text: str) -> str:
    """将汉字侧统一转换为平假名，用于模糊匹配。"""
    result = text.strip()
    for kanji, hira in _KANJI_REPLACEMENTS:
        result = result.replace(kanji, hira)
    return result


# ═══════════════════════════════════════════
# 第一步：解析 choices.txt
# ═══════════════════════════════════════════

ROUTE_MARKERS = {"日生光", "桐島七葵", "遠野十夜", "蒼"}

END_MARKERS = [
    "ベストエンド", "千代エンド", "一章-結末２", "夏帆-結末",
    "六章-終", "蒼の章39-2", "四章37-2、六章03-1", "日生25-2",
]

# 过于常见的短条目，用作上下文锚点时需谨慎
# 这些词在对话中频繁出现，单独一个不足以确认
COMMON_SHORT_ENTRIES = {"はい", "いいえ", "好き", "嫌い"}


def parse_choices_file(filepath: Path) -> dict:
    """
    解析 choices.txt 为结构化数据。

    返回:
      ordered: list[dict]  — 所有选项的有序列表
      choice_set_norm: set  — 规范化后的唯一选项文本集合
      choice_set_orig: set  — 原始唯一选项文本集合
      text_to_info: dict    — 规范化文本 → 路线/章节信息
      route_sequences: dict — 路线 → 规范化选项有序列表
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

    ordered = []
    current_route = None
    current_section = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # 路线标记
        if line in ROUTE_MARKERS:
            current_route = line
            current_section = None
            continue
        if line.startswith("その他シーン回収"):
            current_route = "その他"
            current_section = line
            continue

        # 跳过非选项行
        if "SAVE" in line or "♪" in line:
            continue
        if line in ("↓", "　↓") or line.endswith("↓"):
            continue
        if line.startswith("※") or "※" in line:
            # 注释行：提取被注释的选项（如 ※「嘘を吐かないで」→終１）
            m = re.search(r'[「『](.+?)[」』]', line)
            if m:
                annot_text = m.group(1)
                ordered.append({
                    "text": annot_text,
                    "normalized": normalize_for_match(annot_text),
                    "route": current_route,
                    "section": current_section,
                    "is_annotation": True,
                })
            continue
        if (line.startswith("「") and "」" in line) or line.startswith("言の葉は"):
            continue
        if re.match(r'^(未読|最初から)', line):
            continue

        # 章节标记
        if re.match(r'^([０-９\d]+章|序章|黒の章|蒼の章)$', line):
            current_section = line
            continue

        # 结局标记
        if any(line == m or line.startswith(m) for m in END_MARKERS):
            continue

        # 识别为选项文本
        ordered.append({
            "text": line,
            "normalized": normalize_for_match(line),
            "route": current_route,
            "section": current_section,
            "is_annotation": False,
        })

    # 构建查找集合
    choice_set_norm = set(c["normalized"] for c in ordered)
    choice_set_orig = set(c["text"] for c in ordered)

    # 规范化文本 → 路线信息
    text_to_info = defaultdict(list)
    for c in ordered:
        text_to_info[c["normalized"]].append({
            "route": c["route"],
            "section": c["section"],
            "text": c["text"],
        })

    # 按路线构建有序序列
    route_sequences = defaultdict(list)
    for c in ordered:
        if c["route"]:
            route_sequences[c["route"]].append(c["normalized"])

    return {
        "ordered": ordered,
        "choice_set_norm": choice_set_norm,
        "choice_set_orig": choice_set_orig,
        "text_to_info": dict(text_to_info),
        "route_sequences": dict(route_sequences),
    }


# ═══════════════════════════════════════════
# 第二步：结构检测（潜在选项组）
# ═══════════════════════════════════════════

def is_dialogue_or_narration(line: str) -> bool:
    """判断一行是否为对话或旁白（不是选项）。"""
    text = line.strip()
    if not text:
        return True
    if "「" in text and "」" in text:
        return True
    if text.endswith("。"):
        return True
    if text.endswith("……") or text.endswith("…」"):
        return True
    if "、" in text and len(text) > 15:
        return True
    if len(text) > 25:
        return True
    return False


def is_choice_like(text: str, choice_set_orig: set, choice_set_norm: set) -> bool:
    """
    判断一行是否看起来像选项。
    已知选项（精确或规范化匹配）直接通过。
    未知文本须满足结构条件。
    """
    clean = text.lstrip("#").strip()
    if not clean:
        return False

    # 已知选项
    if clean in choice_set_orig:
        return True
    if normalize_for_match(clean) in choice_set_norm:
        return True

    # 结构过滤
    if len(clean) > 20:
        return False
    if "「" in clean or "」" in clean:
        return False
    if clean.endswith("。"):
        return False
    if "、" in clean:
        return False
    if clean.startswith(("【", "（", "※", "♪", "☆", "★", "■", "●", "終】")):
        return False
    if re.match(r'^\d+$', clean):
        return False
    if "＝" in clean:
        return False
    if re.search(r'[０-９\d]+[ｇＧｋｋｌＬｍＭｃｃ]|大さじ|小さじ|少[し々]', clean):
        return False
    if "※" in clean:
        return False

    return True


def detect_groups(filepath: Path, choice_data: dict) -> list:
    """
    扫描单个文件，检测所有潜在选项组。
    返回 list[dict]，每个 dict 描述一个选项组。
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

    choice_set_orig = choice_data["choice_set_orig"]
    choice_set_norm = choice_data["choice_set_norm"]

    groups = []
    chapter_name = filepath.parent.name
    file_name = filepath.stem
    rel_path = f"{chapter_name}/{file_name}.txt"

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not is_choice_like(line, choice_set_orig, choice_set_norm):
            i += 1
            continue

        # 收集连续的选项行
        group_lines = []
        start_idx = i
        while i < len(lines):
            cur_line = lines[i].strip()
            if not cur_line:
                break
            if not is_choice_like(cur_line, choice_set_orig, choice_set_norm):
                break
            cur_clean = cur_line.lstrip("#").strip()
            group_lines.append((i + 1, cur_clean))  # 1-indexed
            i += 1

        if len(group_lines) >= 2:
            # 前文衔接
            prev_line = ""
            prev_idx = start_idx - 1
            while prev_idx >= 0 and not lines[prev_idx].strip():
                prev_idx -= 1
            if prev_idx >= 0:
                prev_line = lines[prev_idx].strip()

            # 后文衔接
            next_line = ""
            next_idx = i
            while next_idx < len(lines) and not lines[next_idx].strip():
                next_idx += 1
            if next_idx < len(lines):
                next_line = lines[next_idx].strip()

            group = {
                "file": rel_path,
                "chapter": chapter_name,
                "start_line": group_lines[0][0],
                "end_line": group_lines[-1][0],
                "choices": [{"line_no": ln, "text": txt} for ln, txt in group_lines],
                "prev_line": prev_line,
                "prev_line_idx": prev_idx + 1 if prev_idx >= 0 else None,
                "next_line": next_line,
                "next_line_idx": next_idx + 1 if next_idx < len(lines) else None,
            }
            groups.append(group)
        else:
            i = start_idx + 1

    return groups


# ═══════════════════════════════════════════
# 第三步：上下文序列锚定验证
# ═══════════════════════════════════════════

def find_anchors_in_context(
    file_lines: list,
    ctx_start: int,
    ctx_end: int,
    choice_data: dict,
) -> list:
    """
    在上下文窗口内寻找 choices.txt 锚点。

    锚点条件：
      - 该行不是对话（不含「」配对，不以。结尾）
      - 该行文本（规范化后）匹配 choices.txt 条目

    返回: [(line_idx_0based, normalized_text), ...]
    """
    anchors = []
    choice_set_norm = choice_data["choice_set_norm"]

    for i in range(ctx_start, ctx_end):
        if i < 0 or i >= len(file_lines):
            continue
        line = file_lines[i].strip()
        clean = line.lstrip("#").strip()
        if not clean:
            continue

        # 排除对话行和旁白行
        if "「" in clean and "」" in clean:
            continue
        if clean.endswith("。"):
            continue
        # 排除含角色名标记的行（如 "遠野　紗夜「..."）
        if re.match(r'^[^\s「」『』]+\s*[「『]', clean):
            continue

        norm = normalize_for_match(clean)
        if norm in choice_set_norm:
            anchors.append((i, norm, clean))

    return anchors


def check_sequential_order(
    anchors: list,
    route_sequences: dict,
) -> Tuple[bool, Optional[str], list]:
    """
    检查锚点是否在某条路线的序列中按正确顺序出现。

    参数:
      anchors: [(line_idx, norm_text, orig_text), ...]
      route_sequences: {route_name: [norm_text, ...], ...}

    返回: (is_confirmed, best_route, route_anchors)
      route_anchors: 匹配到的锚点子集，按文件行序排列
    """
    if not anchors:
        return False, None, []

    best_route = None
    best_anchors = []
    best_match_count = 0

    for route, seq in route_sequences.items():
        # 为每个锚点找到在路线序列中的所有位置
        positions = []  # [(line_idx, seq_pos)]
        for line_idx, norm, orig in anchors:
            for pos, s in enumerate(seq):
                if s == norm:
                    positions.append((line_idx, pos))

        if len(positions) < MIN_ANCHORS:
            continue

        # 按文件行序排列
        positions.sort(key=lambda x: x[0])

        # 检查是否存在长度 ≥ MIN_ANCHORS 的非递减子序列
        # 使用简化的最长非递减子序列算法
        seq_positions = [p[1] for p in positions]
        lis = _longest_non_decreasing_subseq_len(seq_positions)

        if lis >= MIN_ANCHORS and lis > best_match_count:
            best_match_count = lis
            best_route = route
            best_anchors = anchors  # 保留全部锚点供参考

    if best_route:
        return True, best_route, best_anchors
    return False, None, []


def _longest_non_decreasing_subseq_len(arr: list) -> int:
    """计算最长非递减子序列长度（允许相等）。"""
    if not arr:
        return 0
    n = len(arr)
    if n == 1:
        return 1

    # 简单 O(n²) 实现，n 通常很小（<50）
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[j] <= arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def verify_group(
    group: dict,
    file_lines: list,
    choice_data: dict,
) -> dict:
    """
    对单个潜在选项组做上下文序列锚定验证。

    判定优先级：
      1. 组内有直接匹配（精确或规范化） → 确认（不必再验序列）
      2. 上下文序列验证通过            → 确认
      3. 上下文无锚点                  → 排除
      4. 有锚点但序列不通              → 排除

    返回:
      category: 'confirmed' | 'rejected'
      reason: str
      route: str|None
      anchors: list
    """
    start = group["start_line"] - 1  # 转为 0-indexed
    end = group["end_line"]          # exclusive

    ctx_start = max(0, start - CONTEXT_WINDOW)
    ctx_end = min(len(file_lines), end + CONTEXT_WINDOW)

    # ── 优先级 1：组内直接匹配 → 直接确认 ──
    matched_texts = []
    for choice in group["choices"]:
        norm = normalize_for_match(choice["text"])
        if norm in choice_data["choice_set_norm"]:
            matched_texts.append(choice["text"])

    if matched_texts:
        # 尝试匹配路线
        best_route = _infer_route_from_group(group, choice_data)
        return {
            "category": "confirmed",
            "reason": f"组内直接匹配: {', '.join(matched_texts[:3])}",
            "route": best_route,
            "anchors": [],
        }

    # ── 优先级 2 & 3：上下文序列锚定 ──
    anchors = find_anchors_in_context(
        file_lines, ctx_start, ctx_end, choice_data
    )

    if not anchors:
        return {
            "category": "rejected",
            "reason": "上下文中无 choices.txt 条目（孤立区域）",
            "route": None,
            "anchors": [],
        }

    # 检查顺序一致性
    is_confirmed, route, route_anchors = check_sequential_order(
        anchors, choice_data["route_sequences"]
    )

    if is_confirmed:
        return {
            "category": "confirmed",
            "reason": f"上下文序列一致，路线: {route}，锚点数: {len(route_anchors)}",
            "route": route,
            "anchors": route_anchors,
        }

    # ── 优先级 4：有锚点但序列不通过 → 排除 ──
    return {
        "category": "rejected",
        "reason": f"上下文有 {len(anchors)} 个锚点但顺序不一致",
        "route": None,
        "anchors": anchors,
    }


def _infer_route_from_group(group: dict, choice_data: dict) -> Optional[str]:
    """从组内匹配的选项文本推断最可能的路线。"""
    text_to_info = choice_data["text_to_info"]
    route_counts = defaultdict(int)
    for choice in group["choices"]:
        norm = normalize_for_match(choice["text"])
        if norm in text_to_info:
            for info in text_to_info[norm]:
                if info["route"]:
                    route_counts[info["route"]] += 1
    if route_counts:
        return max(route_counts, key=route_counts.get)
    return None


# ═══════════════════════════════════════════
# 第四步：路线信息匹配
# ═══════════════════════════════════════════

def match_route_info(groups: list, choice_data: dict) -> list:
    """为选项组匹配路线和章节信息。"""
    text_to_info = choice_data["text_to_info"]

    for group in groups:
        routes = set()
        chapters = set()
        annotations = []

        for choice in group["choices"]:
            norm = normalize_for_match(choice["text"])
            if norm in text_to_info:
                for info in text_to_info[norm]:
                    if info["route"]:
                        routes.add(info["route"])
                    if info["section"]:
                        chapters.add(info["section"])

        if group.get("route") and group["route"] not in routes:
            routes.add(group["route"])

        if len(routes) == 0:
            group["route_label"] = "未标注"
        elif len(routes) == 1:
            group["route_label"] = routes.pop()
        else:
            group["route_label"] = "共通 (" + "/".join(sorted(routes)) + ")"

        group["route_chapters"] = sorted(chapters) if chapters else []
        group["branch_annotations"] = annotations

    return groups


# ═══════════════════════════════════════════
# 第五步：生成输出文档
# ═══════════════════════════════════════════

def write_group(f, idx: int, group: dict):
    """写入单个选项组。"""
    f.write(f"## 选项组 #{idx}\n\n")
    f.write(f"- **文件**: `{group['file']}`\n")
    f.write(f"- **行号**: {group['start_line']}-{group['end_line']}\n")
    f.write(f"- **路线**: {group.get('route_label', '未标注')}\n")

    if group.get("route_chapters"):
        f.write(f"- **choices.txt章节**: {', '.join(group['route_chapters'])}\n")

    if group.get("branch_annotations"):
        f.write(f"- **分支信息**: {'; '.join(group['branch_annotations'])}\n")

    # 验证信息
    ver = group.get("verification", {})
    f.write(f"- **验证**: {ver.get('reason', 'N/A')}")
    if ver.get("route"):
        f.write(f" (路线: {ver['route']})")
    f.write("\n")

    f.write(f"- **选项**:\n")
    for choice in group["choices"]:
        f.write(f"  {choice['line_no']}. {choice['text']}\n")

    f.write(f"\n- **前文衔接** (第{group['prev_line_idx']}行): \n")
    f.write(f"  > {group['prev_line']}\n")
    f.write(f"- **后文衔接** (第{group['next_line_idx']}行): \n")
    f.write(f"  > {group['next_line']}\n")

    # 显示上下文锚点
    anchors = ver.get("anchors", [])
    if anchors:
        f.write(f"- **上下文锚点** (窗口 ±{CONTEXT_WINDOW}行):\n")
        for line_idx, norm, orig in anchors[:10]:  # 最多显示 10 个
            f.write(f"  - L{line_idx+1}: `{orig}`\n")
        if len(anchors) > 10:
            f.write(f"  - ... 共 {len(anchors)} 个\n")

    f.write(f"\n---\n\n")


def generate_output(
    confirmed: list,
    rejected: list,
    output_file: Path,
):
    """生成最终的选项定位文档。"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 选项文本定位文档\n\n")
        f.write(
            "本文档记录 processed_output_v3 中所有选项文本的位置信息。\n"
            "基于 choices.txt 标注路线和分支信息。\n"
            "v2: 使用上下文序列锚定验证，过滤结构匹配误判。\n\n"
        )

        f.write("## 统计\n\n")
        f.write(f"- 已确认选项组: {len(confirmed)}\n\n")
        f.write("---\n\n")

        f.write("# 已确认选项\n\n")
        for idx, group in enumerate(confirmed, 1):
            write_group(f, idx, group)


# ═══════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════

def main():
    print("=== 选项文本提取工具 v2（上下文序列锚定）===\n")

    # 1. 解析 choices.txt
    print("[1/5] 解析 choices.txt...")
    choice_data = parse_choices_file(CHOICES_FILE)
    print(f"  选项条目: {len(choice_data['ordered'])} 条")
    print(f"  唯一文本: {len(choice_data['choice_set_norm'])} 条 (规范化)")
    print(f"  路线: {list(choice_data['route_sequences'].keys())}")

    # 2. 收集所有文件
    print("\n[2/5] 收集文件...")
    all_files = []
    for chapter_dir in sorted(SOURCE_DIR.iterdir()):
        if not chapter_dir.is_dir():
            continue
        for txt_file in sorted(chapter_dir.iterdir()):
            if txt_file.suffix == ".txt":
                all_files.append(txt_file)
    print(f"  共 {len(all_files)} 个文件")

    # 3. 检测潜在选项组
    print("\n[3/5] 检测潜在选项组...")
    all_groups = []
    for filepath in all_files:
        groups = detect_groups(filepath, choice_data)
        all_groups.extend(groups)
    print(f"  潜在选项组: {len(all_groups)} 个")

    # 4. 上下文验证
    print("\n[4/5] 上下文序列锚定验证...")

    # 缓存文件内容
    file_cache = {}
    confirmed = []
    rejected = []

    for group in all_groups:
        file_path = SOURCE_DIR / group["file"]

        if group["file"] not in file_cache:
            with open(file_path, "r", encoding="utf-8") as f:
                file_cache[group["file"]] = [l.rstrip("\n") for l in f.readlines()]

        file_lines = file_cache[group["file"]]
        result = verify_group(group, file_lines, choice_data)
        group["verification"] = result

        if result["category"] == "confirmed":
            confirmed.append(group)
        else:
            rejected.append(group)

    # 5. 匹配路线信息
    print("\n[5/5] 匹配路线信息...")
    confirmed = match_route_info(confirmed, choice_data)
    rejected = match_route_info(rejected, choice_data)

    # 生成输出
    print(f"\n生成输出: {OUTPUT_FILE}")
    generate_output(confirmed, rejected, OUTPUT_FILE)

    print(f"\n=== 完成 ===")
    print(f"  已确认: {len(confirmed)} 个")
    print(f"  已排除: {len(rejected)} 个")


if __name__ == "__main__":
    main()

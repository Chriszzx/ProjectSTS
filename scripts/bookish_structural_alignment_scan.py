#!/usr/bin/env python3
"""Scan zh-CN bookish text against processed_output_v3_1 source scenes."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from branch_explore_arc import parse_arc as arc  # noqa: E402


DEFAULT_ROUND_ID = "structural_alignment_round_001"
DEFAULT_OUT_DIR = ROOT / "_audit" / "translation_experiment" / "corrections"
PROCESSED_DIR = ROOT / "processed_output_v3_1"
ZH_DIR = ROOT / "bookish_zhcn"
SCENE_ANNOTATIONS_PATH = ROOT / "branch_explore_arc" / "scene_annotations.json"
CHOICES_MAP_PATH = ROOT / "choices_map_v3_1.md"

CJK_RE = re.compile(r"[\u3400-\u9fff]")
JA_KANA_RE = re.compile(r"[ぁ-んァ-ン]")
ZH_SPEAKER_RE = re.compile(r"^([^:：]{1,28})[:：]\s*(.*)$")
JA_SPEAKER_RE = re.compile(r"^([^「『]{1,32})「(.*)$")
ZH_MIXED_QUOTE_RE = re.compile(r"[“”‘’\"]|(?<=[\u3400-\u9fff])'|'(?=[\u3400-\u9fff])")
INLINE_ASCII_SINGLE_RE = re.compile(r"(?<=[\u3400-\u9fff])'[^'\n]+'(?=[\u3400-\u9fff]|[，。！？、；：,.!?;:]|$)")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]+\]\([^) \n]+\)")
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
APPENDIX_SCENE_HEADING_RE = re.compile(r"^(\d{3}|\d+)\.\s+(.+)$")

ZH_CHAPTER_BY_READING_FILE = {
    "reading_order/00_hajimari.md": "はじまり",
    "reading_order/01_prologue.md": "序章",
    "reading_order/02_chapter1.md": "一章",
    "reading_order/03_chapter2.md": "二章",
    "reading_order/04_chapter3.md": "三章",
    "reading_order/05_natsuko.md": "夏帆",
    "reading_order/06_chapter4_to_hinase_branch.md": "四章",
    "reading_order/07_hinase_chapter4_branch.md": "日生",
    "reading_order/08_hinase.md": "日生",
    "reading_order/09_chapter4_after_hinase_branch.md": "四章",
    "reading_order/10_chapter5_to_kirichiyo_branch.md": "五章",
    "reading_order/11_kirishima_chapter5_branch.md": "桐島",
    "reading_order/12_kirishima.md": "桐島",
    "reading_order/13_chiyo_chapter5_branch.md": "千代",
    "reading_order/14_chiyo_kirishima_branch.md": "千代",
    "reading_order/15_chiyo.md": "千代",
    "reading_order/16_chapter5_after_kirichiyo_branch.md": "五章",
    "reading_order/17_chapter6.md": "六章",
    "reading_order/18_kuro.md": "黒の章",
    "reading_order/19_ao.md": "蒼の章",
    "reading_order/20_atogaki.md": "あとがき",
}

CHAPTER_NAME_ALIASES = {
    "はじまり": "はじまり",
    "开端": "はじまり",
    "序章": "序章",
    "一章": "一章",
    "二章": "二章",
    "三章": "三章",
    "夏帆": "夏帆",
    "四章": "四章",
    "日生": "日生",
    "日生光": "日生",
    "日生光线": "日生",
    "五章": "五章",
    "桐島": "桐島",
    "桐岛": "桐島",
    "桐岛七葵": "桐島",
    "千代": "千代",
    "六章": "六章",
    "黒の章": "黒の章",
    "黑之章": "黒の章",
    "黑的章": "黒の章",
    "蒼の章": "蒼の章",
    "苍之章": "蒼の章",
    "苍的章": "蒼の章",
    "あとがき": "あとがき",
    "后记": "あとがき",
}

TERM_NORMALIZATION = {
    "結末": "结末",
    "結": "结",
    "終": "终",
    "黒": "黑",
    "蒼": "苍",
    "桐島": "桐岛",
    "あとがき": "后记",
    "はじまり": "开端",
    "の章": "之章",
}


@dataclass(frozen=True)
class LineInfo:
    file: str
    line: int
    text: str
    kind: str
    speaker: str | None
    body: str


@dataclass(frozen=True)
class SceneRef:
    scene_index: int
    chapter: str
    title: str
    source_file: str
    local_marker: str
    full_marker: str


@dataclass(frozen=True)
class ZhBlock:
    file: str
    heading: str
    heading_line: int
    source: SceneRef
    lines: list[LineInfo]


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    file: str
    line: int | None
    source_file: str | None
    source_line: int | None
    zh: str
    source: str
    note: str
    suggestion: str
    confidence: str
    scene: str | None = None
    status: str = "pending"

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "source_file": self.source_file,
            "source_line": self.source_line,
            "zh": self.zh,
            "source": self.source,
            "scene": self.scene,
            "note": self.note,
            "suggestion": self.suggestion,
            "confidence": self.confidence,
            "status": self.status,
        }


def compact(text: str, limit: int = 240) -> str:
    cleaned = " ".join(text.strip().split())
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 1] + "..."


def normalize_speaker(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = value.strip().replace("\u3000", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    compacted = cleaned.replace(" ", "")
    for source, target in arc.BOOKISH_ZHCN_SPEAKER_MAP.items():
        source_clean = source.replace("\u3000", " ")
        source_compact = source_clean.replace(" ", "")
        if cleaned == source_clean or compacted == source_compact:
            return target
    return cleaned


def normalize_marker(value: str) -> str:
    marker = value.strip()
    marker = re.sub(r"^シナリオタイトル【(.+)】$", r"\1", marker)
    marker = marker.replace("（不能约定）", "")
    for source, target in TERM_NORMALIZATION.items():
        marker = marker.replace(source, target)
    marker = marker.replace(" ", "").replace("　", "")
    marker = marker.replace("２", "2").replace("１", "1")
    marker = marker.replace("－", "-").replace("ー", "-")

    def normalize_number(match: re.Match[str]) -> str:
        return str(int(match.group(0)))

    marker = re.sub(r"\d+", normalize_number, marker)
    return marker


def canonical_chapter(value: str) -> str | None:
    cleaned = value.strip().replace(" ", "")
    return CHAPTER_NAME_ALIASES.get(cleaned)


def split_scene_title(title: str) -> tuple[str, str]:
    marker = re.sub(r"^シナリオタイトル【(.+)】$", r"\1", title).strip()
    if "-" not in marker:
        return marker, marker
    chapter, local = marker.split("-", 1)
    return marker, local


def scene_label(scene: SceneRef) -> str:
    if scene.scene_index <= 0:
        return f"{scene.full_marker} ({scene.source_file})"
    return f"{scene.scene_index:03d}. {scene.full_marker} ({scene.source_file})"


def classify_zh_line(file: str, line_no: int, line: str) -> LineInfo:
    stripped = line.strip()
    if not stripped:
        return LineInfo(file, line_no, line, "blank", None, "")
    if stripped == "---":
        return LineInfo(file, line_no, line, "hr", None, "")
    if stripped.startswith("<!-- anchor:"):
        return LineInfo(file, line_no, line, "anchor", None, "")
    if re.match(r"^#{1,6}\s+", stripped):
        return LineInfo(file, line_no, line, "heading", None, stripped)
    if stripped.startswith("> 选择：") or stripped.startswith("> 選択："):
        return LineInfo(file, line_no, line, "choice", None, stripped)
    if stripped.startswith("> "):
        return LineInfo(file, line_no, line, "note", None, stripped)
    if stripped.startswith(("- ", "* ")):
        return LineInfo(file, line_no, line, "list", None, stripped)

    match = ZH_SPEAKER_RE.match(stripped)
    if match:
        speaker, body = match.groups()
        if "「" in body or "『" in body:
            return LineInfo(file, line_no, line, "speaker_dialogue", speaker.strip(), body)
        return LineInfo(file, line_no, line, "speaker_narration", speaker.strip(), body)

    if stripped.startswith(("「", "『")):
        return LineInfo(file, line_no, line, "bare_dialogue", None, stripped)
    return LineInfo(file, line_no, line, "narration", None, stripped)


def load_choice_line_refs() -> set[tuple[str, int]]:
    if not CHOICES_MAP_PATH.exists():
        return set()
    refs: set[tuple[str, int]] = set()
    current_file: str | None = None
    for line in CHOICES_MAP_PATH.read_text(encoding="utf-8").splitlines():
        file_match = re.search(r"- \*\*文件\*\*: `([^`]+)`", line)
        if file_match:
            current_file = file_match.group(1)
            continue
        choice_match = re.match(r"\s*(\d+)\.\s+(.+)$", line)
        if current_file and choice_match:
            refs.add((current_file, int(choice_match.group(1))))
    return refs


def classify_processed_line(
    file: str,
    line_no: int,
    line: str,
    choice_line_refs: set[tuple[str, int]],
    open_quote_depth: int,
) -> tuple[LineInfo, int]:
    stripped = line.strip()
    visible = stripped.lstrip("#").strip()
    if not visible:
        info = LineInfo(file, line_no, line, "blank", None, "")
    elif (file, line_no) in choice_line_refs:
        info = LineInfo(file, line_no, line, "choice", None, visible)
    else:
        match = JA_SPEAKER_RE.match(visible)
        if match:
            speaker, body = match.groups()
            info = LineInfo(file, line_no, line, "speaker_dialogue", speaker.strip(), body)
        elif open_quote_depth > 0 or visible.startswith(("「", "『")):
            info = LineInfo(file, line_no, line, "bare_dialogue", None, visible)
        else:
            info = LineInfo(file, line_no, line, "narration", None, visible)

    depth = open_quote_depth + visible.count("「") + visible.count("『") - visible.count("」") - visible.count("』")
    return info, max(depth, 0)


def read_processed_infos(rel: str, choice_line_refs: set[tuple[str, int]]) -> list[LineInfo]:
    path = PROCESSED_DIR / rel
    depth = 0
    infos: list[LineInfo] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        info, depth = classify_processed_line(rel, index, line, choice_line_refs, depth)
        infos.append(info)
    return infos


def source_files_from_manifest() -> list[str]:
    manifest = json.loads((ZH_DIR / "manifest.json").read_text(encoding="utf-8"))
    ignored = set(manifest["epub"].get("frontmatter_files", []))
    files = []
    for source_file in manifest["epub"]["source_files"]:
        if source_file in ignored or source_file.startswith("dividers/"):
            continue
        files.append(source_file)
    return files


def load_scene_refs() -> tuple[dict[int, SceneRef], dict[tuple[str, str], SceneRef], dict[str, SceneRef]]:
    scenes = json.loads(SCENE_ANNOTATIONS_PATH.read_text(encoding="utf-8"))
    source_files = arc.build_bookish_scene_source_files({"scene_annotations": scenes})
    by_index: dict[int, SceneRef] = {}
    by_chapter_marker: dict[tuple[str, str], SceneRef] = {}
    by_full_marker: dict[str, SceneRef] = {}

    for scene in scenes:
        scene_index = int(scene["scene_index"])
        source_file = source_files.get(scene_index)
        if not source_file:
            continue
        full_marker, local_marker = split_scene_title(scene["title"])
        ref = SceneRef(
            scene_index=scene_index,
            chapter=scene["chapter"],
            title=scene["title"],
            source_file=source_file,
            local_marker=local_marker,
            full_marker=full_marker,
        )
        by_index[scene_index] = ref
        by_chapter_marker[(scene["chapter"], normalize_marker(local_marker))] = ref
        by_full_marker[normalize_marker(full_marker)] = ref

    return by_index, by_chapter_marker, by_full_marker


def resolve_scene_heading(
    rel: str,
    heading: str,
    by_index: dict[int, SceneRef],
    by_chapter_marker: dict[tuple[str, str], SceneRef],
    by_full_marker: dict[str, SceneRef],
) -> SceneRef | None:
    heading = heading.strip()
    appendix_match = APPENDIX_SCENE_HEADING_RE.match(heading)
    if appendix_match:
        scene = by_index.get(int(appendix_match.group(1)))
        if scene:
            return scene

    normalized = normalize_marker(heading)
    if normalized in by_full_marker:
        return by_full_marker[normalized]

    chapter = ZH_CHAPTER_BY_READING_FILE.get(rel)
    if chapter:
        scene = by_chapter_marker.get((chapter, normalized))
        if scene:
            return scene

    if "-" in normalized:
        prefix, local = normalized.split("-", 1)
        canonical = canonical_chapter(prefix)
        if canonical:
            return by_chapter_marker.get((canonical, local))

    return None


def parse_zh_blocks(
    rel: str,
    by_index: dict[int, SceneRef],
    by_chapter_marker: dict[tuple[str, str], SceneRef],
    by_full_marker: dict[str, SceneRef],
) -> tuple[list[ZhBlock], list[LineInfo], list[tuple[int, str]]]:
    path = ZH_DIR / rel
    infos = [classify_zh_line(rel, index, line) for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)]
    blocks: list[ZhBlock] = []
    unmatched_headings: list[tuple[int, str]] = []
    current_heading: str | None = None
    current_heading_line: int | None = None
    current_source: SceneRef | None = None
    current_lines: list[LineInfo] = []

    def flush() -> None:
        if current_heading and current_source:
            blocks.append(
                ZhBlock(
                    file=rel,
                    heading=current_heading,
                    heading_line=current_heading_line or 0,
                    source=current_source,
                    lines=list(current_lines),
                )
            )

    for info in infos:
        stripped = info.text.strip()
        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            heading = heading_match.group(2)
            scene = resolve_scene_heading(rel, heading, by_index, by_chapter_marker, by_full_marker)
            if scene:
                flush()
                current_heading = heading
                current_heading_line = info.line
                current_source = scene
                current_lines = []
                continue
            if stripped.startswith(("## ", "### ")) and not heading.startswith(("注", "进入条件")):
                unmatched_headings.append((info.line, heading))

        if current_source:
            current_lines.append(info)

    flush()
    return blocks, infos, unmatched_headings


def add_finding(
    findings: list[Finding],
    rule_id: str,
    severity: str,
    file: str,
    zh: LineInfo | None,
    source: LineInfo | None,
    note: str,
    suggestion: str,
    confidence: str = "medium",
    scene: SceneRef | None = None,
) -> None:
    findings.append(
        Finding(
            rule_id=rule_id,
            severity=severity,
            file=file,
            line=zh.line if zh else None,
            source_file=source.file if source else (scene.source_file if scene else None),
            source_line=source.line if source else None,
            zh=compact(zh.text) if zh else "",
            source=compact(source.text) if source else "",
            note=note,
            suggestion=suggestion,
            confidence=confidence,
            scene=scene_label(scene) if scene else None,
        )
    )


def is_translatable_kind(kind: str) -> bool:
    return kind in {"speaker_dialogue", "speaker_narration", "bare_dialogue", "narration"}


def quote_counts(text: str) -> dict[str, int]:
    return {
        "「": text.count("「"),
        "」": text.count("」"),
        "『": text.count("『"),
        "』": text.count("』"),
        "“": text.count("“"),
        "”": text.count("”"),
        "‘": text.count("‘"),
        "’": text.count("’"),
        '"': text.count('"'),
    }


def scan_quote_issues(file: str, zh_infos: list[LineInfo], findings: list[Finding]) -> None:
    for info in zh_infos:
        stripped = info.text.strip()
        if not stripped or info.kind in {"heading", "anchor"}:
            continue
        no_links = MARKDOWN_LINK_RE.sub("", stripped)
        counts = quote_counts(no_links)

        if ZH_MIXED_QUOTE_RE.search(no_links) or INLINE_ASCII_SINGLE_RE.search(no_links):
            add_finding(
                findings,
                "mixed_quote_style",
                "medium",
                file,
                info,
                None,
                "中文正文存在非目标引号字符，可能需要统一为 `「」` / `『』`。",
                "人工确认该处是否是引用、书名外的引语或普通撇号；确认后改为日文引号层级。",
                confidence="high",
            )

        if counts["「"] != counts["」"] or counts["『"] != counts["』"]:
            add_finding(
                findings,
                "unbalanced_japanese_quotes",
                "high",
                file,
                info,
                None,
                f"日文式引号数量不平衡：{counts}",
                "优先人工审核，避免把跨行引用或脚本文本误合并。",
                confidence="high",
            )

        if counts["“"] != counts["”"] or counts["‘"] != counts["’"]:
            add_finding(
                findings,
                "unbalanced_curly_quotes",
                "medium",
                file,
                info,
                None,
                f"中文/弯引号数量不平衡：{counts}",
                "若确认为引语，统一改为 `「」` / `『』`。",
                confidence="high",
            )

        if re.search(r"「[^」]*。」", stripped):
            add_finding(
                findings,
                "dialogue_terminal_period_left",
                "medium",
                file,
                info,
                None,
                "对话引号内部仍有末尾句号。",
                "按当前规则删除 `。」` 中的句号。",
                confidence="high",
            )


def alignment_token(info: LineInfo) -> str:
    if info.kind in {"blank", "hr", "anchor"}:
        return info.kind
    if info.kind in {"heading", "choice", "note", "list"}:
        return info.kind
    if info.kind in {"speaker_dialogue", "speaker_narration"}:
        return f"speaker:{normalize_speaker(info.speaker) or '?'}"
    return info.kind


def compare_aligned_pair(
    file: str,
    source: LineInfo,
    zh: LineInfo,
    findings: list[Finding],
    scene: SceneRef,
    confidence: str,
) -> None:
    severity = "high" if confidence != "low" else "medium"

    if source.kind in {"heading", "hr", "anchor", "choice", "note", "list", "blank"} or zh.kind in {
        "heading",
        "hr",
        "anchor",
        "choice",
        "note",
        "list",
        "blank",
    }:
        return

    if source.kind in {"narration", "bare_dialogue"} and zh.kind == "speaker_dialogue":
        source_shape = "旁白" if source.kind == "narration" else "无角色名前缀的引语/台词"
        add_finding(
            findings,
            "source_unspeakered_text_wrapped_as_dialogue",
            severity,
            file,
            zh,
            source,
            f"v3-1 原文是{source_shape}，中文被归入带角色名的对话。",
            "优先人工审核；若确认沿用原文形态，去掉中文角色名前缀。若原文是纯旁白，同时去掉外层对话引号；若原文是内层引语，只保留 `「」` / `『』`。",
            confidence=confidence,
            scene=scene,
        )
    elif source.kind == "narration" and zh.kind == "bare_dialogue":
        add_finding(
            findings,
            "source_narration_wrapped_in_quotes",
            severity,
            file,
            zh,
            source,
            "v3-1 原文是旁白，中文被包进引号。",
            "优先人工审核；若确认是旁白，去掉外层引号。",
            confidence=confidence,
            scene=scene,
        )
    elif source.kind == "speaker_dialogue" and zh.kind == "narration":
        add_finding(
            findings,
            "source_dialogue_rendered_as_narration",
            severity,
            file,
            zh,
            source,
            "v3-1 原文是带说话人的对话，中文变成旁白形态。",
            "检查是否丢失角色名前缀或对话引号。",
            confidence=confidence,
            scene=scene,
        )

    if source.kind == "speaker_dialogue" and zh.kind == "speaker_dialogue":
        source_speaker = normalize_speaker(source.speaker)
        zh_speaker = normalize_speaker(zh.speaker)
        if source_speaker and zh_speaker and source_speaker != zh_speaker:
            add_finding(
                findings,
                "speaker_name_mismatch",
                severity,
                file,
                zh,
                source,
                f"说话人不一致：v3-1={source_speaker} / ZH={zh_speaker}。",
                "优先对照原文确认是否翻译错位或说话人误归属。",
                confidence=confidence,
                scene=scene,
            )

    if is_translatable_kind(zh.kind) and JA_KANA_RE.search(zh.text):
        add_finding(
            findings,
            "japanese_kana_in_zh",
            "medium",
            file,
            zh,
            source,
            "中文行中仍含假名。",
            "确认是否为保留标题/专名；否则应翻译或替换。",
            confidence="high",
            scene=scene,
        )


def translatable_lines(lines: list[LineInfo]) -> list[LineInfo]:
    return [line for line in lines if is_translatable_kind(line.kind)]


def compare_scene_block(
    block: ZhBlock,
    source_infos: list[LineInfo],
    findings: list[Finding],
) -> None:
    source_lines = translatable_lines(source_infos)
    zh_lines = translatable_lines(block.lines)
    if not source_lines or not zh_lines:
        return

    max_len = max(len(source_lines), len(zh_lines))
    diff_ratio = abs(len(source_lines) - len(zh_lines)) / max_len
    confidence = "high" if diff_ratio <= 0.18 else "medium" if diff_ratio <= 0.35 else "low"
    if diff_ratio > 0.18:
        add_finding(
            findings,
            "source_block_line_count_mismatch",
            "medium",
            block.file,
            LineInfo(block.file, block.heading_line, f"## {block.heading}", "heading", None, block.heading),
            None,
            f"场景块可翻译行数差异较大：v3-1={len(source_lines)} / ZH={len(zh_lines)}。",
            "该块内部逐行错位候选的置信度会降低；优先确认是否有路线分支、删减或合并。",
            confidence=confidence,
            scene=block.source,
        )

    compare_anchor_bounded_spans(block, source_lines, zh_lines, findings)

    source_tokens = [alignment_token(line) for line in source_lines]
    zh_tokens = [alignment_token(line) for line in zh_lines]
    matcher = difflib.SequenceMatcher(None, source_tokens, zh_tokens, autojunk=False)
    for tag, source_start, source_end, zh_start, zh_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        source_block = source_lines[source_start:source_end]
        zh_block = zh_lines[zh_start:zh_end]
        if tag in {"replace", "delete", "insert"} and max(len(source_block), len(zh_block)) >= 12:
            add_finding(
                findings,
                "source_shape_alignment_gap",
                "medium",
                block.file,
                zh_block[0] if zh_block else None,
                source_block[0] if source_block else None,
                f"场景内行形态 token 对齐出现 {tag} 区块：v3-1 {source_start + 1}-{source_end} / ZH {zh_start + 1}-{zh_end}。",
                "该区块可能存在路线删减、翻译合并、说话人归属变化或结构错位；先进入人工抽查。",
                confidence=confidence,
                scene=block.source,
            )


def speaker_anchor(info: LineInfo) -> str | None:
    if info.kind != "speaker_dialogue":
        return None
    return normalize_speaker(info.speaker)


def matched_speaker_anchor_pairs(
    source_lines: list[LineInfo],
    zh_lines: list[LineInfo],
) -> list[tuple[int, int]]:
    source_anchors = [
        (index, speaker)
        for index, line in enumerate(source_lines)
        if (speaker := speaker_anchor(line))
    ]
    zh_anchors = [
        (index, speaker)
        for index, line in enumerate(zh_lines)
        if (speaker := speaker_anchor(line))
    ]
    if not source_anchors or not zh_anchors:
        return [(-1, -1), (len(source_lines), len(zh_lines))]

    source_speakers = [speaker for _, speaker in source_anchors]
    zh_speakers = [speaker for _, speaker in zh_anchors]
    matcher = difflib.SequenceMatcher(None, source_speakers, zh_speakers, autojunk=False)
    pairs: list[tuple[int, int]] = [(-1, -1)]
    for tag, source_start, source_end, zh_start, zh_end in matcher.get_opcodes():
        if tag != "equal":
            continue
        for source_anchor, zh_anchor in zip(source_anchors[source_start:source_end], zh_anchors[zh_start:zh_end]):
            pairs.append((source_anchor[0], zh_anchor[0]))
    pairs.append((len(source_lines), len(zh_lines)))
    return pairs


def compare_anchor_bounded_spans(
    block: ZhBlock,
    source_lines: list[LineInfo],
    zh_lines: list[LineInfo],
    findings: list[Finding],
) -> None:
    pairs = matched_speaker_anchor_pairs(source_lines, zh_lines)
    for (prev_source, prev_zh), (next_source, next_zh) in zip(pairs, pairs[1:]):
        source_span = source_lines[prev_source + 1 : next_source]
        zh_span = zh_lines[prev_zh + 1 : next_zh]
        if not source_span or not zh_span:
            continue

        source_unspeakered = [line for line in source_span if line.kind in {"narration", "bare_dialogue"}]
        zh_speakered = [line for line in zh_span if line.kind == "speaker_dialogue"]
        if len(source_unspeakered) < 2 or len(zh_speakered) < 2:
            continue

        source_ratio = len(source_unspeakered) / len(source_span)
        zh_ratio = len(zh_speakered) / len(zh_span)
        if source_ratio < 0.8 or zh_ratio < 0.7:
            continue

        max_len = max(len(source_unspeakered), len(zh_speakered))
        span_diff = abs(len(source_unspeakered) - len(zh_speakered)) / max_len
        bounded_by_real_anchors = prev_source >= 0 and prev_zh >= 0 and next_source < len(source_lines) and next_zh < len(zh_lines)
        confidence = "high" if bounded_by_real_anchors and span_diff <= 0.25 else "medium" if span_diff <= 0.45 else "low"
        if confidence == "low":
            continue

        for source, zh in zip(source_unspeakered, zh_speakered):
            compare_aligned_pair(block.file, source, zh, findings, block.source, confidence)


def write_jsonl(path: Path, findings: Iterable[Finding]) -> None:
    path.write_text(
        "".join(json.dumps(item.to_dict(), ensure_ascii=False) + "\n" for item in findings),
        encoding="utf-8",
    )


def write_markdown(
    path: Path,
    findings: list[Finding],
    files: list[str],
    round_id: str,
    matched_blocks: int,
    unmatched_headings: dict[str, list[tuple[int, str]]],
) -> None:
    counts = Counter(item.rule_id for item in findings)
    severity_counts = Counter(item.severity for item in findings)
    confidence_counts = Counter(item.confidence for item in findings)
    lines = [
        f"# 结构/错位/引号扫描：{round_id}",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> 范围：`bookish_zhcn` 对照 `processed_output_v3_1`，{len(files)} 个正文/附录源文件",
        f"> 场景映射：{matched_blocks} 个中文场景块成功绑定到 v3-1 原始 txt",
        "",
        "## 摘要",
        "",
        f"- 总候选：{len(findings)}",
        f"- 高优先级：{severity_counts.get('high', 0)}",
        f"- 中优先级：{severity_counts.get('medium', 0)}",
        f"- 低优先级：{severity_counts.get('low', 0)}",
        f"- 高置信：{confidence_counts.get('high', 0)}",
        f"- 中置信：{confidence_counts.get('medium', 0)}",
        f"- 低置信：{confidence_counts.get('low', 0)}",
        "",
        "## 分类计数",
        "",
        "| Rule | Count |",
        "|---|---:|",
    ]
    for rule_id, count in counts.most_common():
        lines.append(f"| `{rule_id}` | {count} |")

    priority_rules = [
        "source_unspeakered_text_wrapped_as_dialogue",
        "source_narration_wrapped_in_quotes",
        "source_dialogue_rendered_as_narration",
        "speaker_name_mismatch",
        "unbalanced_japanese_quotes",
        "mixed_quote_style",
        "source_block_line_count_mismatch",
        "source_shape_alignment_gap",
    ]
    lines.extend(["", "## 高价值样例", ""])
    for rule_id in priority_rules:
        subset = [item for item in findings if item.rule_id == rule_id]
        if not subset:
            continue
        lines.append(f"### `{rule_id}` ({len(subset)})")
        lines.append("")
        for item in subset[:30]:
            source_ref = f" / v3-1 `{item.source_file}:{item.source_line}`" if item.source_file and item.source_line else ""
            zh_ref = f"{item.file}:{item.line}" if item.line else item.file
            confidence = f" / confidence={item.confidence}"
            lines.append(f"- `{zh_ref}`{source_ref}{confidence}")
            if item.scene:
                lines.append(f"  - 场景：{item.scene}")
            if item.zh:
                lines.append(f"  - ZH: {item.zh}")
            if item.source:
                lines.append(f"  - v3-1: {item.source}")
            lines.append(f"  - 判断：{item.note}")
            lines.append(f"  - 建议：{item.suggestion}")
        lines.append("")

    if unmatched_headings:
        lines.extend(["## 未绑定标题", ""])
        for rel, headings in sorted(unmatched_headings.items()):
            shown = ", ".join(f"{line}:{heading}" for line, heading in headings[:20])
            suffix = " ..." if len(headings) > 20 else ""
            lines.append(f"- `{rel}`: {shown}{suffix}")
        lines.append("")

    lines.extend(
        [
            "## 使用说明",
            "",
            "- `*.findings.jsonl` 是完整候选队列，供后续自动/半自动修正脚本读取。",
            "- 本轮日文对照源是 `processed_output_v3_1` 的原始 scene txt；没有读取日文 `bookish/` 作为判断依据。",
            "- `source_unspeakered_text_wrapped_as_dialogue` 直接对应“原文无角色名前缀，中文却变成角色对话”的问题。",
            "- 低置信候选通常出现在路线分支较多、原始 txt 与当前中文读本删减/合并较多的场景；先抽样，不建议直接自动改。",
            "- `mixed_quote_style` 命中会很多，后续需要按上下文把中文/ASCII 引号分批改成 `「」` / `『』`。",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def run(round_id: str, out_dir: Path) -> tuple[Path, Path, list[Finding]]:
    by_index, by_chapter_marker, by_full_marker = load_scene_refs()
    scene_refs_by_chapter: dict[str, list[SceneRef]] = defaultdict(list)
    for scene in by_index.values():
        scene_refs_by_chapter[scene.chapter].append(scene)
    for refs in scene_refs_by_chapter.values():
        refs.sort(key=lambda item: item.scene_index)

    choice_line_refs = load_choice_line_refs()
    processed_cache: dict[str, list[LineInfo]] = {}
    files = source_files_from_manifest()
    findings: list[Finding] = []
    unmatched_headings: dict[str, list[tuple[int, str]]] = defaultdict(list)
    matched_blocks = 0

    for rel in files:
        zh_path = ZH_DIR / rel
        if not zh_path.exists():
            add_finding(
                findings,
                "missing_zh_file",
                "high",
                rel,
                None,
                None,
                "缺少中文 bookish 文件。",
                "先恢复同构文件结构后再继续扫描。",
                confidence="high",
            )
            continue

        blocks, zh_infos, file_unmatched = parse_zh_blocks(rel, by_index, by_chapter_marker, by_full_marker)
        if file_unmatched:
            unmatched_headings[rel].extend(file_unmatched)
        scan_quote_issues(rel, zh_infos, findings)

        if not blocks and (chapter := ZH_CHAPTER_BY_READING_FILE.get(rel)):
            source_infos: list[LineInfo] = []
            for scene in scene_refs_by_chapter.get(chapter, []):
                source_file = scene.source_file
                if source_file not in processed_cache:
                    source_path = PROCESSED_DIR / source_file
                    if source_path.exists():
                        processed_cache[source_file] = read_processed_infos(source_file, choice_line_refs)
                source_infos.extend(processed_cache.get(source_file, []))
            if source_infos:
                matched_blocks += 1
                aggregate_scene = SceneRef(
                    scene_index=0,
                    chapter=chapter,
                    title=chapter,
                    source_file=f"{chapter} aggregate from processed_output_v3_1",
                    local_marker=chapter,
                    full_marker=chapter,
                )
                aggregate_block = ZhBlock(rel, chapter, 1, aggregate_scene, zh_infos)
                compare_scene_block(aggregate_block, source_infos, findings)
            continue

        for block in blocks:
            source_file = block.source.source_file
            if source_file not in processed_cache:
                source_path = PROCESSED_DIR / source_file
                if not source_path.exists():
                    add_finding(
                        findings,
                        "missing_processed_source",
                        "high",
                        rel,
                        LineInfo(rel, block.heading_line, block.heading, "heading", None, block.heading),
                        None,
                        f"缺少 v3-1 对照文件：{source_file}",
                        "先确认 processed_output_v3_1 是否完整。",
                        confidence="high",
                        scene=block.source,
                    )
                    continue
                processed_cache[source_file] = read_processed_infos(source_file, choice_line_refs)
            matched_blocks += 1
            compare_scene_block(block, processed_cache[source_file], findings)

    def finding_sort_key(item: Finding) -> tuple[object, ...]:
        file_group = 0 if item.file.startswith("reading_order/") else 1 if item.file.startswith("appendix/") else 2
        return (item.severity != "high", file_group, item.file, item.line or 0, item.rule_id)

    findings.sort(key=finding_sort_key)
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = out_dir / f"{round_id}.findings.jsonl"
    md_path = out_dir / f"{round_id}.md"
    write_jsonl(jsonl_path, findings)
    write_markdown(md_path, findings, files, round_id, matched_blocks, unmatched_headings)
    return jsonl_path, md_path, findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round-id", default=DEFAULT_ROUND_ID)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    jsonl_path, md_path, findings = run(args.round_id, args.out_dir)
    counts = Counter(item.rule_id for item in findings)
    print(f"findings: {len(findings)}")
    for rule_id, count in counts.most_common():
        print(f"{rule_id}: {count}")
    print(f"jsonl: {jsonl_path.relative_to(ROOT)}")
    print(f"report: {md_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

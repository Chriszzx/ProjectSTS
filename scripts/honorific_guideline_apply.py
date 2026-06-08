#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply audited honorific corrections from the project guideline table."""

from __future__ import annotations

import argparse
import json
from bisect import bisect_right
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JA_DIR = ROOT / "bookish" / "reading_order"
DEFAULT_ZH_DIR = ROOT / "bookish_zhcn" / "reading_order"
DEFAULT_OUT_DIR = ROOT / "_audit" / "translation_experiment" / "corrections"
DEFAULT_ROUND_ID = "honorific_guideline_round_001"


@dataclass(frozen=True)
class LineRecord:
    number: int
    index: int
    text: str


@dataclass(frozen=True)
class Change:
    rule_id: str
    title: str
    file: str
    zh_line: int
    ja_line: int
    ja_text: str
    before: str
    after: str
    llm_judgment: str
    human_status: str = "applied-auto"

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "file": self.file,
            "zh_line": self.zh_line,
            "ja_line": self.ja_line,
            "ja_text": self.ja_text,
            "before": self.before,
            "after": self.after,
            "llm_judgment": self.llm_judgment,
            "human_status": self.human_status,
        }


@dataclass(frozen=True)
class AlignmentWarning:
    file: str
    ja_nonempty_lines: int
    zh_nonempty_lines: int

    def to_dict(self) -> dict[str, object]:
        return {
            "file": self.file,
            "ja_nonempty_lines": self.ja_nonempty_lines,
            "zh_nonempty_lines": self.zh_nonempty_lines,
        }


@dataclass(frozen=True)
class DialogueAlignment:
    zh_to_ja: dict[int, LineRecord]
    pairs: list[tuple[int, int]]


Predicate = Callable[[str], bool]
Replacement = Callable[[str], str]
ContextPredicate = Callable[[LineRecord, list[str], str], bool]


@dataclass(frozen=True)
class HonorificRule:
    rule_id: str
    title: str
    zh_needles: tuple[str, ...]
    predicate: Predicate
    replace: Replacement
    llm_judgment: str
    context_predicate: ContextPredicate | None = None
    allow_ratio_fallback: bool = False

    def is_candidate(self, zh_line: str) -> bool:
        return has_any(zh_line, self.zh_needles)

    def apply(self, ja_line: str, zh_line: str) -> str:
        if not self.predicate(ja_line):
            return zh_line
        return self.replace(zh_line)

    def allows_context(self, ja_record: LineRecord, ja_lines: list[str], zh_line: str) -> bool:
        if self.context_predicate is None:
            return True
        return self.context_predicate(ja_record, ja_lines, zh_line)


def has_any(text: str, needles: Iterable[str]) -> bool:
    return any(needle in text for needle in needles)


def is_sayo_or_narration(ja_line: str) -> bool:
    if ja_line.startswith("遠野　紗夜:") or ja_line.startswith("遠野 紗夜:") or ja_line.startswith("遠野紗夜:"):
        return True
    return ":" not in ja_line.split("「", 1)[0]


def replace_terms(text: str, pairs: Iterable[tuple[str, str]]) -> str:
    updated = text
    for before, after in pairs:
        updated = updated.replace(before, after)
    return updated


def normalize_chiyo_topic_phrasing(text: str) -> str:
    return replace_terms(
        text,
        [
            ("千代，您要不要来我这边？", "千代，愿意到我这里来吗？"),
            ("千代，您……", "千代，你……"),
            ("千代，您怎么会在这里？", "千代，怎么会在这里？"),
            ("……但是，千代，您却又希望我察觉到什么，我完全搞不懂……", "……可是千代却希望我察觉到什么，我完全搞不懂……"),
            ("请您来家里这点小事根本不算什么。尤其是千代，您", "请您来家里这点小事根本不算什么。尤其是千代"),
            ("比起我，千代，您要温柔得多了", "比起我，千代要温柔得多了"),
            ("千代，您很优秀呢", "千代真是很棒呢"),
            ("千代，您是不愿意和我一起去图书馆吗？", "千代，是不愿意和我一起去图书馆吗？"),
            ("千代你来学校需要许可吗？", "千代来学校需要许可吗？"),
            ("千代你听课会觉得无聊吗？", "千代听课会觉得无聊吗？"),
            ("千代你能感知到桐岛前辈在哪里对吧？", "千代能感知到桐岛前辈在哪里对吧？"),
            ("像千代你们那样", "像千代他们那样"),
            ("千代你也说过吧", "千代也说过吧"),
            ("千代你呢", "千代呢"),
        ],
    )


JA_SPEAKERS = {
    "遠野　紗夜": "sayo",
    "遠野 紗夜": "sayo",
    "遠野紗夜": "sayo",
    "日生 光": "hikari",
    "日生光": "hikari",
    "千代": "chiyo",
    "宮沢 夏帆": "kaho",
    "宮沢夏帆": "kaho",
    "臥待 春夫": "gashomachi",
    "臥待春夫": "gashomachi",
    "桐島 七葵": "kirishima",
    "桐島七葵": "kirishima",
    "蒼": "ao",
    "遠野 十夜": "toya",
    "遠野十夜": "toya",
    "男子生徒Ａ": "male_student_a",
    "男子生徒Ｂ": "male_student_b",
    "男子生徒": "male_student",
    "女子生徒Ａ": "female_student_a",
    "女子生徒Ｂ": "female_student_b",
    "女子生徒": "female_student",
}

ZH_SPEAKERS = {
    "远野纱夜": "sayo",
    "日生光": "hikari",
    "千代": "chiyo",
    "宫泽夏帆": "kaho",
    "卧待春夫": "gashomachi",
    "桐岛七葵": "kirishima",
    "苍": "ao",
    "远野十夜": "toya",
    "男学生A": "male_student_a",
    "男学生B": "male_student_b",
    "男学生": "male_student",
    "女学生A": "female_student_a",
    "女学生B": "female_student_b",
    "女学生": "female_student",
}


def speaker_prefix(line: str) -> str | None:
    before_quote = line.split("「", 1)[0]
    if ":" not in before_quote:
        return None
    return before_quote.split(":", 1)[0].strip()


def has_dialogue_marker(line: str) -> bool:
    return speaker_prefix(line) is not None


def speaker_id(line: str, mapping: dict[str, str]) -> str | None:
    prefix = speaker_prefix(line)
    if prefix is None:
        return None
    return mapping.get(prefix)


def dialogue_records(lines: list[str], mapping: dict[str, str]) -> list[tuple[LineRecord, str]]:
    records: list[tuple[LineRecord, str]] = []
    for record in nonempty_records(lines):
        sid = speaker_id(record.text, mapping)
        if sid is not None:
            records.append((record, sid))
    return records


def build_dialogue_alignment(ja_lines: list[str], zh_lines: list[str]) -> DialogueAlignment:
    ja_dialogue = dialogue_records(ja_lines, JA_SPEAKERS)
    zh_dialogue = dialogue_records(zh_lines, ZH_SPEAKERS)
    ja_sequence = [sid for _, sid in ja_dialogue]
    zh_sequence = [sid for _, sid in zh_dialogue]
    matcher = SequenceMatcher(a=ja_sequence, b=zh_sequence, autojunk=False)
    zh_to_ja: dict[int, LineRecord] = {}
    pairs: list[tuple[int, int]] = []
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            ja_record, ja_sid = ja_dialogue[block.a + offset]
            zh_record, zh_sid = zh_dialogue[block.b + offset]
            if ja_sid != zh_sid:
                continue
            zh_to_ja[zh_record.index] = ja_record
            pairs.append((zh_record.index, ja_record.index))
    pairs.sort()
    return DialogueAlignment(zh_to_ja=zh_to_ja, pairs=pairs)


def nearest_unique(records: list[LineRecord], predicted_index: int) -> LineRecord | None:
    if not records:
        return None
    distances = sorted((abs(record.index - predicted_index), record.index, record) for record in records)
    if len(distances) > 1 and distances[0][0] == distances[1][0]:
        return None
    return distances[0][2]


def collect_candidates(
    rule: HonorificRule,
    ja_lines: list[str],
    start: int,
    end: int,
    zh_sid: str | None,
) -> list[LineRecord]:
    candidates: list[LineRecord] = []
    for index in range(start, end):
        ja_line = ja_lines[index]
        if not rule.predicate(ja_line):
            continue
        if zh_sid is not None:
            ja_sid = speaker_id(ja_line, JA_SPEAKERS)
            if ja_sid != zh_sid:
                continue
        candidates.append(LineRecord(number=index + 1, index=index, text=ja_line))
    return candidates


def hikari_private_context(ja_record: LineRecord, ja_lines: list[str], zh_line: str) -> bool:
    meta_terms = (
        "不是光先生",
        "光先生没有说过",
        "光先生、光先生",
        "日生光先生",
        "味觉障碍者",
        "自称真正者",
    )
    if has_any(zh_line, meta_terms):
        return False
    formal_line_terms = ("お祖母様", "祖母", "紫", "両親", "母", "父", "縁談", "婚約", "結婚", "本物", "偽物")
    if has_any(ja_record.text, formal_line_terms):
        return False
    if "お初にお目にかかります" in ja_record.text:
        return False
    start = max(0, ja_record.index - 12)
    end = min(len(ja_lines), ja_record.index + 13)
    local_context = "\n".join(ja_lines[start:end])
    formal_context_terms = ("日生祖母", "日生紫", "日生 紫", "奥様")
    return not has_any(local_context, formal_context_terms)


def find_contextual_ja_record(
    rule: HonorificRule,
    zh_record: LineRecord,
    ja_lines: list[str],
    zh_lines: list[str],
    alignment: DialogueAlignment,
) -> LineRecord | None:
    exact = alignment.zh_to_ja.get(zh_record.index)
    if exact is not None:
        if rule.predicate(exact.text) and rule.allows_context(exact, ja_lines, zh_record.text):
            return exact
        return None

    # Unknown dialogue speakers are not safe to rewrite by narration heuristics.
    zh_sid = speaker_id(zh_record.text, ZH_SPEAKERS)
    if has_dialogue_marker(zh_record.text) and zh_sid is None:
        return None

    zh_indices = [zh for zh, _ in alignment.pairs]
    position = bisect_right(zh_indices, zh_record.index)
    previous_pair = alignment.pairs[position - 1] if position > 0 else None
    next_pair = alignment.pairs[position] if position < len(alignment.pairs) else None

    search_start = 0
    search_end = len(ja_lines)
    if previous_pair is not None and next_pair is not None:
        previous_zh, previous_ja = previous_pair
        next_zh, next_ja = next_pair
        if previous_ja < next_ja:
            zh_span = max(next_zh - previous_zh, 1)
            ja_span = max(next_ja - previous_ja, 1)
            predicted = previous_ja + round((zh_record.index - previous_zh) * ja_span / zh_span)
            search_start = previous_ja + 1
            search_end = next_ja
        else:
            predicted = round(zh_record.index * max(len(ja_lines) - 1, 0) / max(len(zh_lines) - 1, 1))
    else:
        predicted = round(zh_record.index * max(len(ja_lines) - 1, 0) / max(len(zh_lines) - 1, 1))
        search_start = max(0, predicted - 48)
        search_end = min(len(ja_lines), predicted + 49)

    candidates = collect_candidates(rule, ja_lines, search_start, search_end, zh_sid)
    if not candidates and rule.allow_ratio_fallback:
        ratio_predicted = round(zh_record.index * max(len(ja_lines) - 1, 0) / max(len(zh_lines) - 1, 1))
        candidates = collect_candidates(
            rule,
            ja_lines,
            max(0, ratio_predicted - 240),
            min(len(ja_lines), ratio_predicted + 241),
            zh_sid,
        )
        predicted = ratio_predicted
    candidate = nearest_unique(candidates, predicted)
    if candidate is None:
        return None
    if not rule.allows_context(candidate, ja_lines, zh_record.text):
        return None
    return candidate


RULES: list[HonorificRule] = [
    HonorificRule(
        rule_id="hikari-senpai",
        title="纱夜 → 光先輩：光前辈",
        zh_needles=("光先生",),
        predicate=lambda ja: "光先輩" in ja and "光さん" not in ja,
        replace=lambda zh: replace_terms(zh, [("光先生", "光前辈")]),
        llm_judgment="`光先輩` 仍是前后辈称呼，不应译成“先生”；保留名呼作“光前辈”。",
    ),
    HonorificRule(
        rule_id="hinase-senpai",
        title="纱夜 → 日生：日生先輩 = 日生前辈",
        zh_needles=("日生学长",),
        predicate=lambda ja: "日生先輩" in ja,
        replace=lambda zh: replace_terms(zh, [("日生学长", "日生前辈")]),
        llm_judgment="策略表规定 `日生先輩` 统一译为“日生前辈”，避免“学长/前辈”摇摆。",
    ),
    HonorificRule(
        rule_id="kirishima-senpai",
        title="纱夜 → 桐岛：桐島先輩 = 桐岛前辈",
        zh_needles=("桐岛学长",),
        predicate=lambda ja: "桐島先輩" in ja,
        replace=lambda zh: replace_terms(zh, [("桐岛学长", "桐岛前辈")]),
        llm_judgment="策略表规定 `桐島先輩` 统一译为“桐岛前辈”。",
    ),
    HonorificRule(
        rule_id="hikari-san-private",
        title="纱夜/叙述 → 光：光さん = 光",
        zh_needles=("光先生",),
        predicate=lambda ja: "光さん" in ja and is_sayo_or_narration(ja),
        replace=lambda zh: replace_terms(zh, [("光先生您", "光，你"), ("光先生", "光")]),
        llm_judgment="策略表规定恋人后私下 `光さん` 译为“光”，正式场合才可用“光先生”。",
        context_predicate=hikari_private_context,
    ),
    HonorificRule(
        rule_id="hikari-ojo",
        title="光 → 纱夜：お嬢 = 小姐",
        zh_needles=("大小姐",),
        predicate=lambda ja: "お嬢" in ja and "お嬢様" not in ja and "お嬢さん" not in ja,
        replace=lambda zh: replace_terms(zh, [("大小姐", "小姐")]),
        llm_judgment="策略表规定 `お嬢` 译为“小姐”，`お嬢様` 才译“大小姐”。",
    ),
    HonorificRule(
        rule_id="chiyo-ojousan",
        title="千代 → 纱夜：お嬢さん = 小姐",
        zh_needles=("大小姐", "大、小姐"),
        predicate=lambda ja: "お嬢さん" in ja,
        replace=lambda zh: replace_terms(zh, [("大、大小姐", "小、小姐"), ("大、小姐", "小、小姐"), ("大小姐", "小姐")]),
        llm_judgment="策略表规定千代的 `お嬢さん` 译为“小姐”，不译“大小姐”。",
        allow_ratio_fallback=True,
    ),
    HonorificRule(
        rule_id="sayo-to-chiyo-san",
        title="纱夜/叙述 → 千代：千代さん = 千代",
        zh_needles=("千代先生", "千代小姐", "千代女士", "千代同学", "千代桑", "千代君", "千代酱", "千代大人", "千代您"),
        predicate=lambda ja: "千代さん" in ja,
        replace=lambda zh: replace_terms(
            zh,
            [
                ("千代您", "千代，您"),
                ("千代先生您", "千代，您"),
                ("千代小姐您", "千代，您"),
                ("千代先生", "千代"),
                ("千代小姐", "千代"),
                ("千代女士", "千代"),
                ("千代同学", "千代"),
                ("千代桑", "千代"),
                ("千代君", "千代"),
                ("千代酱", "千代"),
                ("千代大人", "千代"),
            ],
        ),
        llm_judgment="策略表规定 `千代さん` 默认译“千代”，不显性化为先生/小姐/女士/同学/桑；距离感由句式承担。",
        allow_ratio_fallback=True,
    ),
    HonorificRule(
        rule_id="sayo-to-chiyo-san-truncation",
        title="纱夜 → 千代：千代さ…… = 千代……",
        zh_needles=("千代小……", "千代小...", "千代小…"),
        predicate=lambda ja: "千代さ" in ja,
        replace=lambda zh: replace_terms(zh, [("千代小……", "千代……"), ("千代小...", "千代..."), ("千代小…", "千代…")]),
        llm_judgment="`千代さ……` 是 `千代さん` 的被打断呼唤；中文按本轮策略保留“千代……”，不残留“千代小”。",
        allow_ratio_fallback=True,
    ),
    HonorificRule(
        rule_id="sayo-to-chiyo-topic-naturalization",
        title="纱夜 → 千代：千代さん 的中文话题句自然化",
        zh_needles=("千代，您", "千代你", "千代你们"),
        predicate=lambda ja: "千代さん" in ja,
        replace=normalize_chiyo_topic_phrasing,
        llm_judgment="`千代さん` 后缀不在中文中硬贴成身份或机械二人称；保留“千代”话题感，并按语境使用“你/您/省略”。",
        allow_ratio_fallback=True,
    ),
    HonorificRule(
        rule_id="chiyo-address-residual-exact",
        title="千代称呼残留：精确上下文修正",
        zh_needles=("千代同学的手",),
        predicate=lambda ja: True,
        replace=lambda zh: replace_terms(zh, [("千代同学的手", "千代的手")]),
        llm_judgment="旧译把转述中的千代继续显性化为“同学”；该处上下文是千代本人回忆与桐岛牵手，按准则改为“千代”。",
    ),
    HonorificRule(
        rule_id="chiyo-sayo-san",
        title="千代 → 纱夜：紗夜さん = 纱夜",
        zh_needles=("纱夜小姐", "纱夜、小姐"),
        predicate=lambda ja: "紗夜さん" in ja or "紗夜、さん" in ja,
        replace=lambda zh: replace_terms(zh, [("纱夜、小姐", "纱夜"), ("纱夜小姐", "纱夜")]),
        llm_judgment="策略表规定千代关键转换 `紗夜さん` 译为“纱夜”，保留从“小姐”到名字的转换。",
    ),
    HonorificRule(
        rule_id="gashomachi-to-sayo-chan",
        title="卧待 → 纱夜：紗夜ちゃん = 小纱夜",
        zh_needles=("纱夜酱",),
        predicate=lambda ja: ja.startswith("臥待 春夫:") and "紗夜ちゃん" in ja,
        replace=lambda zh: replace_terms(zh, [("纱夜酱", "小纱夜")]),
        llm_judgment="用户修正策略表：卧待对纱夜的 `紗夜ちゃん` 固定译“小纱夜”，与夏帆的“纱夜酱”分开。",
    ),
]


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def clean_dialogue_terminal_periods(text: str) -> str:
    return text.replace("。」", "」")


def nonempty_records(lines: list[str]) -> list[LineRecord]:
    return [LineRecord(number=i + 1, index=i, text=line) for i, line in enumerate(lines) if line.strip()]


def apply_honorific_guidelines(
    ja_files: Iterable[Path] | None = None,
    *,
    zh_dir: Path = DEFAULT_ZH_DIR,
    root: Path = ROOT,
) -> list[Change]:
    files = sorted(ja_files) if ja_files is not None else sorted(DEFAULT_JA_DIR.glob("*.md"))
    changes: list[Change] = []
    for ja_path in files:
        zh_path = zh_dir / ja_path.name
        if not zh_path.exists():
            continue
        ja_lines = ja_path.read_text(encoding="utf-8").splitlines()
        zh_lines = zh_path.read_text(encoding="utf-8").splitlines()
        alignment = build_dialogue_alignment(ja_lines, zh_lines)
        zh_records = nonempty_records(zh_lines)

        for zh_record in zh_records:
            current = zh_lines[zh_record.index]
            for rule in RULES:
                if not rule.is_candidate(current):
                    continue
                ja_record = find_contextual_ja_record(rule, zh_record, ja_lines, zh_lines, alignment)
                if ja_record is None:
                    continue
                updated = rule.apply(ja_record.text, current)
                if updated == current:
                    continue
                changes.append(
                    Change(
                        rule_id=rule.rule_id,
                        title=rule.title,
                        file=relative_path(zh_path, root),
                        zh_line=zh_record.number,
                        ja_line=ja_record.number,
                        ja_text=ja_record.text,
                        before=current,
                        after=updated,
                        llm_judgment=rule.llm_judgment,
                    )
                )
                current = updated
            zh_lines[zh_record.index] = clean_dialogue_terminal_periods(current)
        zh_path.write_text("\n".join(zh_lines) + "\n", encoding="utf-8")
    changes.sort(key=lambda item: (item.file, item.zh_line, item.rule_id))
    return changes


def scan_alignment_warnings(
    ja_files: Iterable[Path] | None = None,
    *,
    zh_dir: Path = DEFAULT_ZH_DIR,
    root: Path = ROOT,
) -> list[AlignmentWarning]:
    files = sorted(ja_files) if ja_files is not None else sorted(DEFAULT_JA_DIR.glob("*.md"))
    warnings: list[AlignmentWarning] = []
    for ja_path in files:
        zh_path = zh_dir / ja_path.name
        if not zh_path.exists():
            continue
        ja_count = len(nonempty_records(ja_path.read_text(encoding="utf-8").splitlines()))
        zh_count = len(nonempty_records(zh_path.read_text(encoding="utf-8").splitlines()))
        if ja_count != zh_count:
            warnings.append(
                AlignmentWarning(
                    file=relative_path(zh_path, root),
                    ja_nonempty_lines=ja_count,
                    zh_nonempty_lines=zh_count,
                )
            )
    return warnings


def write_jsonl(path: Path, items: Iterable[Change | AlignmentWarning]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")


def count_by_rule(changes: Iterable[Change]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for change in changes:
        counts[change.rule_id] = counts.get(change.rule_id, 0) + 1
    return dict(sorted(counts.items()))


def render_report(round_id: str, changes: list[Change], warnings: list[AlignmentWarning]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    counts = count_by_rule(changes)
    lines = [
        f"# 敬语称呼准则回填记录：{round_id}",
        "",
        f"> 生成时间：{now}",
        "> 范围：`bookish/reading_order/*.md` 与 `bookish_zhcn/reading_order/*.md`",
        "> 原则：按敬语准则策略表回填；只在日文对应行证明称呼关系时自动改；每条操作保留日文依据。",
        "",
        "## 本轮状态",
        "",
        f"- 自动回填：{len(changes)}",
        f"- 非空行数量不一致的文件：{len(warnings)}",
        "",
        "## 规则统计",
        "",
    ]
    for rule in RULES:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- 说明：{rule.title}",
                f"- LLM 初判：{rule.llm_judgment}",
                f"- 本轮应用：{counts.get(rule.rule_id, 0)}",
                "",
            ]
        )

    lines.extend(["## 自动回填明细", ""])
    if changes:
        for change in changes:
            lines.extend(
                [
                    f"- `{change.file}:{change.zh_line}` `{change.rule_id}`",
                    f"  - ja `{change.ja_line}`: {change.ja_text}",
                    f"  - before: {change.before}",
                    f"  - after: {change.after}",
                ]
            )
    else:
        lines.append("- 本轮没有自动回填。")

    lines.extend(["", "## 对齐警告", ""])
    if warnings:
        for warning in warnings:
            lines.append(
                f"- `{warning.file}` ja_nonempty={warning.ja_nonempty_lines}, zh_nonempty={warning.zh_nonempty_lines}"
            )
    else:
        lines.append("- 未发现非空行数量不一致。")

    lines.extend(["", "## 人工审核说明", ""])
    lines.append("- `*.operations.jsonl` 是全量操作记录，可按 `human_status` 做二次人工验收。")
    lines.append("- `*.alignment_warnings.jsonl` 记录非空行数不一致文件；本轮不使用非空行 zip，而是使用说话人锚点与局部日文触发语确认。")
    lines.append("")
    return "\n".join(lines)


def write_outputs(round_id: str, changes: list[Change], warnings: list[AlignmentWarning], out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / f"{round_id}.md"
    operations = out_dir / f"{round_id}.operations.jsonl"
    alignment = out_dir / f"{round_id}.alignment_warnings.jsonl"
    report.write_text(render_report(round_id, changes, warnings), encoding="utf-8")
    write_jsonl(operations, changes)
    write_jsonl(alignment, warnings)
    return {"report": report, "operations": operations, "alignment": alignment}


def command_apply(args: argparse.Namespace) -> int:
    root = Path(args.root)
    ja_dir = Path(args.ja_dir)
    zh_dir = Path(args.zh_dir)
    ja_files = sorted(ja_dir.glob("*.md"))
    changes = apply_honorific_guidelines(ja_files, zh_dir=zh_dir, root=root)
    warnings = scan_alignment_warnings(ja_files, zh_dir=zh_dir, root=root)
    outputs = write_outputs(args.round_id, changes, warnings, Path(args.out_dir))
    print(f"honorific changes: {len(changes)}")
    print(f"alignment warnings: {len(warnings)}")
    print(f"report: {outputs['report']}")
    print(f"operations: {outputs['operations']}")
    print(f"alignment: {outputs['alignment']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--ja-dir", default=str(DEFAULT_JA_DIR))
    parser.add_argument("--zh-dir", default=str(DEFAULT_ZH_DIR))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--round-id", default=DEFAULT_ROUND_ID)
    subparsers = parser.add_subparsers(dest="command", required=True)
    apply = subparsers.add_parser("apply", help="Apply honorific guideline corrections.")
    apply.set_defaults(func=command_apply)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

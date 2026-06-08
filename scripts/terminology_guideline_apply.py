#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply deterministic terminology corrections and report review candidates."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZH_DIR = ROOT / "bookish_zhcn" / "reading_order"
DEFAULT_OUT_DIR = ROOT / "_audit" / "translation_experiment" / "corrections"
DEFAULT_ROUND_ID = "terminology_round_001"


@dataclass(frozen=True)
class TermRule:
    rule_id: str
    title: str
    replacements: tuple[tuple[str, str], ...]
    judgment: str

    def apply(self, text: str) -> str:
        updated = text
        for before, after in self.replacements:
            updated = updated.replace(before, after)
        return updated

    def matches(self, text: str) -> bool:
        return any(before in text for before, _ in self.replacements)


@dataclass(frozen=True)
class Change:
    rule_id: str
    title: str
    file: str
    line: int
    before: str
    after: str
    llm_judgment: str
    human_status: str = "applied-auto"

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "file": self.file,
            "line": self.line,
            "before": self.before,
            "after": self.after,
            "llm_judgment": self.llm_judgment,
            "human_status": self.human_status,
        }


@dataclass(frozen=True)
class ReviewFinding:
    rule_id: str
    title: str
    file: str
    line: int
    line_text: str
    llm_judgment: str
    human_status: str = "pending"

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "file": self.file,
            "line": self.line,
            "line_text": self.line_text,
            "llm_judgment": self.llm_judgment,
            "human_status": self.human_status,
        }


RULES: list[TermRule] = [
    TermRule(
        rule_id="clock-tower",
        title="時計塔：时钟塔",
        replacements=(
            ("时钟塔", "__CLOCK_TOWER__"),
            ("时计塔", "__CLOCK_TOWER__"),
            ("钟塔", "__CLOCK_TOWER__"),
            ("钟楼", "__CLOCK_TOWER__"),
            ("__CLOCK_TOWER__", "时钟塔"),
        ),
        judgment="用户确认 `時計塔` 统一译为“时钟塔”。",
    ),
    TermRule(
        rule_id="librarian",
        title="司書：图书管理员",
        replacements=(("司书", "图书管理员"),),
        judgment="用户确认 `司書` 固定译为“图书管理员”，不混用“司书”。",
    ),
    TermRule(
        rule_id="fantasy-monogatari",
        title="幻想物語：幻想物语",
        replacements=(
            ("幻想故事", "幻想物语"),
            ("幻想物語", "幻想物语"),
        ),
        judgment="按用户确认的字面策略，`物語` 在术语性表达中保留“物语”。",
    ),
    TermRule(
        rule_id="kago-no-tori-title",
        title="籠の鳥：笼中鸟",
        replacements=(
            ("《笼里的鸟》", "《笼中鸟》"),
            ("『笼里的鸟』", "『笼中鸟』"),
            ("「笼里的鸟」", "「笼中鸟」"),
            ("《笼中之鸟》", "《笼中鸟》"),
            ("『笼中之鸟』", "『笼中鸟』"),
            ("「笼中之鸟」", "「笼中鸟」"),
        ),
        judgment="用户确认只固定 `籠の鳥` 标题为《笼中鸟》。",
    ),
    TermRule(
        rule_id="chiyo-flower-terms",
        title="秋桜/コスモス/桜：秋樱/波斯菊/樱花",
        replacements=(
            ("大波斯菊", "波斯菊"),
            ("樱花花", "樱花"),
            ("秋樱花", "秋樱"),
        ),
        judgment="用户确认按揭示层级处理：`コスモス` 为“波斯菊”，`秋桜` 为“秋樱”，`桜` 为“樱花”。",
    ),
]


REVIEW_PATTERNS: tuple[tuple[str, str, re.Pattern[str], str], ...] = (
    (
        "monogatari-review",
        "物語：故事/物语人工判断",
        re.compile(r"故事"),
        "剩余“故事”需对照原文判断：`物語` 术语性用“物语”，普通 `話/お話` 可保留“故事/话”。",
    ),
    (
        "kotoba-language-review",
        "言葉：语言/言语人工判断",
        re.compile(r"语言|言语|话语"),
        "`言葉` 暂不自动回填；需区分主题词、普通话语、单个词、语言系统、花语和故事台词。",
    ),
    (
        "ao-color-review",
        "蒼色/青：苍色母题人工判断",
        re.compile(r"青色|蓝色|苍色|青黑色|青白|薄青"),
        "`蒼色/青` 需结合苍、天空、眼睛、书脊、夜色母题检查，不自动替换。",
    ),
    (
        "honmono-review",
        "本物/偽物：真假身份轴人工判断",
        re.compile(r"真正的|真的|假的|虚假的|不是真的|不是真正|本尊|正主|真品|赝品"),
        "`本物/偽物` 暂不自动回填；需区分修饰语、独立名词、谓语和童话/亲缘语境。",
    ),
)


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def clean_dialogue_terminal_periods(text: str) -> str:
    return text.replace("。」", "」")


def apply_terminology(
    files: Iterable[Path] | None = None,
    *,
    zh_dir: Path = DEFAULT_ZH_DIR,
    root: Path = ROOT,
) -> list[Change]:
    paths = sorted(files) if files is not None else sorted(zh_dir.glob("*.md"))
    changes: list[Change] = []
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            current = line
            for rule in RULES:
                if not rule.matches(current):
                    continue
                updated = rule.apply(current)
                if updated == current:
                    continue
                changes.append(
                    Change(
                        rule_id=rule.rule_id,
                        title=rule.title,
                        file=relative_path(path, root),
                        line=index + 1,
                        before=current,
                        after=updated,
                        llm_judgment=rule.judgment,
                    )
                )
                current = updated
            lines[index] = clean_dialogue_terminal_periods(current)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    changes.sort(key=lambda item: (item.file, item.line, item.rule_id))
    return changes


def collect_review_findings(
    files: Iterable[Path] | None = None,
    *,
    zh_dir: Path = DEFAULT_ZH_DIR,
    root: Path = ROOT,
    limit_per_rule: int = 200,
) -> list[ReviewFinding]:
    paths = sorted(files) if files is not None else sorted(zh_dir.glob("*.md"))
    findings: list[ReviewFinding] = []
    counts: dict[str, int] = {}
    for path in paths:
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            for rule_id, title, pattern, judgment in REVIEW_PATTERNS:
                if counts.get(rule_id, 0) >= limit_per_rule:
                    continue
                if not pattern.search(line):
                    continue
                findings.append(
                    ReviewFinding(
                        rule_id=rule_id,
                        title=title,
                        file=relative_path(path, root),
                        line=index + 1,
                        line_text=line,
                        llm_judgment=judgment,
                    )
                )
                counts[rule_id] = counts.get(rule_id, 0) + 1
    findings.sort(key=lambda item: (item.rule_id, item.file, item.line))
    return findings


def write_jsonl(path: Path, items: Iterable[Change | ReviewFinding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")


def count_changes(changes: Iterable[Change]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for change in changes:
        counts[change.rule_id] = counts.get(change.rule_id, 0) + 1
    return dict(sorted(counts.items()))


def count_findings(findings: Iterable[ReviewFinding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.rule_id] = counts.get(finding.rule_id, 0) + 1
    return dict(sorted(counts.items()))


def render_report(round_id: str, changes: list[Change], findings: list[ReviewFinding]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_counts = count_changes(changes)
    finding_counts = count_findings(findings)
    lines = [
        f"# 术语准则回填记录：{round_id}",
        "",
        f"> 生成时间：{now}",
        "> 范围：`bookish_zhcn/reading_order/*.md`",
        "> 原则：只自动回填用户已确认且无需上下文判断的术语；语义敏感项仅列入人工候选。",
        "",
        "## 本轮状态",
        "",
        f"- 自动回填：{len(changes)}",
        f"- 人工候选：{len(findings)}",
        "",
        "## 自动规则统计",
        "",
    ]
    for rule in RULES:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- 说明：{rule.title}",
                f"- 初判：{rule.judgment}",
                f"- 本轮应用：{change_counts.get(rule.rule_id, 0)}",
                "",
            ]
        )

    lines.extend(["## 人工候选统计", ""])
    for rule_id, title, _, judgment in REVIEW_PATTERNS:
        lines.extend(
            [
                f"### {rule_id}",
                "",
                f"- 说明：{title}",
                f"- 初判：{judgment}",
                f"- 本轮候选：{finding_counts.get(rule_id, 0)}",
                "",
            ]
        )

    lines.extend(["## 自动回填明细", ""])
    if changes:
        for change in changes:
            lines.extend(
                [
                    f"- `{change.file}:{change.line}` `{change.rule_id}`",
                    f"  - before: {change.before}",
                    f"  - after: {change.after}",
                ]
            )
    else:
        lines.append("- 本轮没有自动回填。")

    lines.extend(["", "## 人工候选样例", ""])
    if findings:
        for finding in findings[:160]:
            lines.extend(
                [
                    f"- `{finding.file}:{finding.line}` `{finding.rule_id}`",
                    f"  - text: {finding.line_text}",
                ]
            )
        if len(findings) > 160:
            lines.append(f"- 其余 {len(findings) - 160} 条见 `*.review.jsonl`。")
    else:
        lines.append("- 本轮没有人工候选。")

    lines.extend(["", "## 人工审核说明", ""])
    lines.append("- `*.operations.jsonl` 是自动回填记录。")
    lines.append("- `*.review.jsonl` 是需要人工或 LLM 精判的候选项，特别是“物语/故事”“语言/言语”“苍色/青色”“正牌/冒牌”。")
    lines.append("")
    return "\n".join(lines)


def write_outputs(
    round_id: str,
    changes: list[Change],
    findings: list[ReviewFinding],
    out_dir: Path,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / f"{round_id}.md"
    operations = out_dir / f"{round_id}.operations.jsonl"
    review = out_dir / f"{round_id}.review.jsonl"
    report.write_text(render_report(round_id, changes, findings), encoding="utf-8")
    write_jsonl(operations, changes)
    write_jsonl(review, findings)
    return {"report": report, "operations": operations, "review": review}


def command_apply(args: argparse.Namespace) -> int:
    root = Path(args.root)
    zh_dir = Path(args.zh_dir)
    files = sorted(zh_dir.glob("*.md"))
    changes = apply_terminology(files, zh_dir=zh_dir, root=root)
    findings = collect_review_findings(files, zh_dir=zh_dir, root=root, limit_per_rule=args.review_limit)
    outputs = write_outputs(args.round_id, changes, findings, Path(args.out_dir))
    print(f"terminology changes: {len(changes)}")
    print(f"review findings: {len(findings)}")
    print(f"report: {outputs['report']}")
    print(f"operations: {outputs['operations']}")
    print(f"review: {outputs['review']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--zh-dir", default=str(DEFAULT_ZH_DIR))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--round-id", default=DEFAULT_ROUND_ID)
    parser.add_argument("--review-limit", type=int, default=200)
    subparsers = parser.add_subparsers(dest="command", required=True)
    apply = subparsers.add_parser("apply", help="Apply deterministic terminology corrections.")
    apply.set_defaults(func=command_apply)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

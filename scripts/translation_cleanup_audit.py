#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan and conservatively fix obvious zh-CN translation cleanup issues.

This tool is intentionally audit-first. It applies only high-confidence
literal corrections and records everything else for human review.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_READING_ORDER = ROOT / "bookish_zhcn" / "reading_order"
DEFAULT_CORRECTION_DIR = ROOT / "_audit" / "translation_experiment" / "corrections"
DEFAULT_ROUND_ID = "zhcn_cleanup_round_001"


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    mode: str
    severity: str
    pattern: re.Pattern[str]
    replacement: str | None
    llm_judgment: str
    human_status: str = "pending"

    def replacement_for(self, match: re.Match[str]) -> str | None:
        if self.replacement is None:
            return None
        return match.expand(self.replacement)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    mode: str
    severity: str
    file: str
    line: int
    before: str
    line_text: str
    after: str | None
    llm_judgment: str
    human_status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "mode": self.mode,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "before": self.before,
            "line_text": self.line_text,
            "after": self.after,
            "llm_judgment": self.llm_judgment,
            "human_status": self.human_status,
        }


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


RULES: list[Rule] = [
    Rule(
        rule_id="hard-misread-naniga",
        title="明显误读：何が？",
        mode="auto",
        severity="high",
        pattern=re.compile(r"日生光: 「什么够不够？」"),
        replacement="日生光: 「什么？」",
        llm_judgment="日文 `何が？` 是追问对象的 '什么？/你指什么？'，现译 '什么够不够？' 属明显误读。",
    ),
    Rule(
        rule_id="hard-translator-note-shingai",
        title="译者犹豫痕迹：心外だという顔",
        mode="auto",
        severity="high",
        pattern=re.compile(r"面对我的问题，他露出一副意外（或不以为然）的表情。"),
        replacement="面对我的问题，他露出一副不服气的表情。",
        llm_judgment="括号内容是译者不确定痕迹；`心外だという顔` 可确定为不服气/受冤枉的神情。",
    ),
    Rule(
        rule_id="hard-prologue-duplicate-sashiagemashou",
        title="脚本换行误合并：差しあげましょう",
        mode="auto",
        severity="high",
        pattern=re.compile(
            r"远野十夜: 「如果您想离开笼子，我就帮您实现这个愿望，」\n"
            r"远野十夜: 「帮您实现。」"
        ),
        replacement="远野十夜: 「如果您想离开笼子，我就帮您实现这个愿望」",
        llm_judgment="日文 `差しあげましょう` 被脚本断行，中文不应重复成两个 '实现'。",
    ),
    Rule(
        rule_id="hard-prologue-stray-inner-quote",
        title="内嵌引用缺开引号：笼中鸟口头禅",
        mode="auto",
        severity="high",
        pattern=re.compile(r"远野十夜: 「我想出笼去』——这是笼中鸟的口头禅。」"),
        replacement="远野十夜: 「『我想出笼去』——这是笼中鸟的口头禅」",
        llm_judgment="内层 `我想出笼去` 只有闭引号，缺开引号，属于排版/引用错误。",
    ),
    Rule(
        rule_id="term-clocktower-variant",
        title="术语混用：時計塔",
        mode="review",
        severity="medium",
        pattern=re.compile(r"时计塔|钟塔|钟楼|时钟塔"),
        replacement=None,
        llm_judgment="`時計塔` 当前存在多译名；需要人工确认项目术语后统一，不在本轮自动替换。",
    ),
    Rule(
        rule_id="honorific-hikari-sensei",
        title="称呼疑点：光先生",
        mode="review",
        severity="medium",
        pattern=re.compile(r"光先生"),
        replacement=None,
        llm_judgment="可能误把 `光先輩` 或恋人后的 `光さん` 处理为 '先生'；需对照日文判断。",
    ),
    Rule(
        rule_id="honorific-hinase-senpai-mix",
        title="称呼混用：日生学长/光前辈",
        mode="review",
        severity="medium",
        pattern=re.compile(r"日生学长|光前辈"),
        replacement=None,
        llm_judgment="`日生先輩/光先輩` 与当前 '前辈/学长' 混用相关；需按关系阶段统一。",
    ),
    Rule(
        rule_id="honorific-chiyo-title-mix",
        title="称呼混用：千代先生/千代小姐/纱夜小姐",
        mode="review",
        severity="medium",
        pattern=re.compile(r"千代先生|千代小姐|纱夜小姐"),
        replacement=None,
        llm_judgment="`千代さん` 与 `紗夜さん` 的中文称呼需要按关系转换判断；本轮只记录。",
    ),
    Rule(
        rule_id="honorific-ojousama-risk",
        title="称呼疑点：大小姐",
        mode="review",
        severity="medium",
        pattern=re.compile(r"大小姐"),
        replacement=None,
        llm_judgment="可能来自 `お嬢様`，也可能误译 `お嬢/お嬢さん`；需对照日文。",
    ),
    Rule(
        rule_id="suspicious-plural-thanks",
        title="复数疑点：谢谢你们",
        mode="review",
        severity="low",
        pattern=re.compile(r"谢谢你们"),
        replacement=None,
        llm_judgment="`ありがとうございます` 很多场景只面对单人；'你们' 需按对象数量人工确认。",
    ),
    Rule(
        rule_id="translator-trace-generic",
        title="译者痕迹疑点",
        mode="review",
        severity="high",
        pattern=re.compile(r"（或|暂译|TODO|FIXME|待定"),
        replacement=None,
        llm_judgment="正文中不应保留译者犹豫或 TODO 痕迹；除已知 auto 规则外先记录审核。",
    ),
]


def iter_markdown_files(paths: Iterable[Path] | None = None, root: Path = ROOT) -> list[Path]:
    if paths is not None:
        return [Path(path) for path in paths]
    return sorted((root / "bookish_zhcn" / "reading_order").glob("*.md"))


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def source_line(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    return text[start:end]


def compact_snippet(text: str) -> str:
    return " ".join(text.split())


def scan_text(text: str, path: Path, root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative_path(path, root)
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            after = rule.replacement_for(match)
            findings.append(
                Finding(
                    rule_id=rule.rule_id,
                    title=rule.title,
                    mode=rule.mode,
                    severity=rule.severity,
                    file=rel,
                    line=line_number(text, match.start()),
                    before=compact_snippet(match.group(0)),
                    line_text=compact_snippet(source_line(text, match.start())),
                    after=after,
                    llm_judgment=rule.llm_judgment,
                    human_status=rule.human_status,
                )
            )
    findings.sort(key=lambda item: (item.file, item.line, item.rule_id))
    return findings


def scan_paths(paths: Iterable[Path] | None = None, root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_markdown_files(paths, root=root):
        findings.extend(scan_text(path.read_text(encoding="utf-8"), path, root=root))
    findings.sort(key=lambda item: (item.file, item.line, item.rule_id))
    return findings


def apply_auto_corrections(paths: Iterable[Path] | None = None, root: Path = ROOT) -> list[Change]:
    changes: list[Change] = []
    auto_rules = [rule for rule in RULES if rule.mode == "auto"]
    for path in iter_markdown_files(paths, root=root):
        text = path.read_text(encoding="utf-8")
        updated = text
        file_changes: list[Change] = []
        for rule in auto_rules:
            matches = list(rule.pattern.finditer(updated))
            for match in matches:
                replacement = rule.replacement_for(match)
                if replacement is None:
                    continue
                file_changes.append(
                    Change(
                        rule_id=rule.rule_id,
                        title=rule.title,
                        file=relative_path(path, root),
                        line=line_number(updated, match.start()),
                        before=compact_snippet(match.group(0)),
                        after=replacement,
                        llm_judgment=rule.llm_judgment,
                    )
                )
            updated = rule.pattern.sub(lambda match: rule.replacement_for(match) or match.group(0), updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
        changes.extend(file_changes)
    changes.sort(key=lambda item: (item.file, item.line, item.rule_id))
    return changes


def count_by_rule(items: Iterable[Finding | Change]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.rule_id] = counts.get(item.rule_id, 0) + 1
    return dict(sorted(counts.items()))


def write_jsonl(path: Path, items: Iterable[Finding | Change]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")


def read_changes_jsonl(path: Path) -> list[Change]:
    if not path.exists():
        return []
    changes: list[Change] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            data = json.loads(line)
            changes.append(
                Change(
                    rule_id=data["rule_id"],
                    title=data["title"],
                    file=data["file"],
                    line=int(data["line"]),
                    before=data["before"],
                    after=data["after"],
                    llm_judgment=data["llm_judgment"],
                    human_status=data.get("human_status", "applied-auto"),
                )
            )
    return changes


def render_markdown(round_id: str, findings: list[Finding], changes: list[Change]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    finding_counts = count_by_rule(findings)
    change_counts = count_by_rule(changes)
    review_findings = [item for item in findings if item.mode == "review"]

    lines = [
        f"# 中文译文显然错误修正记录：{round_id}",
        "",
        f"> 生成时间：{now}",
        "> 范围：`bookish_zhcn/reading_order/*.md`",
        "> 原则：先记录，后修正；只自动应用高置信硬错误；称呼、术语、语体进入人工审核。",
        "",
        "## 本轮状态",
        "",
        f"- 扫描命中：{len(findings)}",
        f"- 自动修正：{len(changes)}",
        f"- 待人工审核：{len(review_findings)}",
        "",
        "## 自动修正规则",
        "",
    ]

    auto_rules = [rule for rule in RULES if rule.mode == "auto"]
    for rule in auto_rules:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- 说明：{rule.title}",
                f"- 严重度：{rule.severity}",
                f"- LLM 初判：{rule.llm_judgment}",
                f"- 本轮应用：{change_counts.get(rule.rule_id, 0)}",
                "",
            ]
        )

    lines.extend(["## 待人工审核规则", ""])
    for rule in [rule for rule in RULES if rule.mode == "review"]:
        lines.extend(
            [
                f"### {rule.rule_id}",
                "",
                f"- 说明：{rule.title}",
                f"- 严重度：{rule.severity}",
                f"- LLM 初判：{rule.llm_judgment}",
                f"- 本轮命中：{finding_counts.get(rule.rule_id, 0)}",
                "- 人工状态：pending",
                "",
            ]
        )

    lines.extend(["## 自动修正明细", ""])
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
        lines.append("- 本轮没有自动修正。")

    lines.extend(["", "## 待审核样例", ""])
    if review_findings:
        for finding in review_findings[:200]:
            lines.extend(
                [
                    f"- `{finding.file}:{finding.line}` `{finding.rule_id}`",
                    f"  - match: {finding.before}",
                    f"  - line: {finding.line_text}",
                    f"  - judgment: {finding.llm_judgment}",
                ]
            )
        if len(review_findings) > 200:
            lines.append(f"- 其余 {len(review_findings) - 200} 条见 JSONL 全量记录。")
    else:
        lines.append("- 没有待审核项。")

    lines.extend(
        [
            "",
            "## 人工审核说明",
            "",
            "- `*.findings.jsonl`：扫描全量记录。",
            "- `*.operations.jsonl`：已自动应用的修正记录。",
            "- 审核时建议逐条标注 `accepted/rejected/needs-context`，再进入下一轮自动回填。",
            "",
        ]
    )

    return "\n".join(lines)


def write_report(round_id: str, findings: list[Finding], changes: list[Change], out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / f"{round_id}.md"
    findings_path = out_dir / f"{round_id}.findings.jsonl"
    operations_path = out_dir / f"{round_id}.operations.jsonl"
    report.write_text(render_markdown(round_id, findings, changes), encoding="utf-8")
    write_jsonl(findings_path, findings)
    write_jsonl(operations_path, changes)
    return {"report": report, "findings": findings_path, "operations": operations_path}


def command_scan(args: argparse.Namespace) -> int:
    root = Path(args.root)
    findings = scan_paths(root=root)
    outputs = write_report(args.round_id, findings, [], Path(args.out_dir))
    print(f"scan findings: {len(findings)}")
    print(f"report: {outputs['report']}")
    print(f"findings: {outputs['findings']}")
    return 0


def command_apply(args: argparse.Namespace) -> int:
    root = Path(args.root)
    findings_before = scan_paths(root=root)
    changes = apply_auto_corrections(root=root)
    findings_after = scan_paths(root=root)
    outputs = write_report(args.round_id, findings_after, changes, Path(args.out_dir))
    print(f"findings before: {len(findings_before)}")
    print(f"auto changes: {len(changes)}")
    print(f"findings after: {len(findings_after)}")
    print(f"report: {outputs['report']}")
    print(f"findings: {outputs['findings']}")
    print(f"operations: {outputs['operations']}")
    return 0


def command_report(args: argparse.Namespace) -> int:
    root = Path(args.root)
    operations_path = Path(args.operations_jsonl)
    findings = scan_paths(root=root)
    changes = read_changes_jsonl(operations_path)
    outputs = write_report(args.round_id, findings, changes, Path(args.out_dir))
    print(f"scan findings: {len(findings)}")
    print(f"loaded operations: {len(changes)}")
    print(f"report: {outputs['report']}")
    print(f"findings: {outputs['findings']}")
    print(f"operations: {outputs['operations']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT), help="Project root.")
    parser.add_argument("--out-dir", default=str(DEFAULT_CORRECTION_DIR), help="Audit output directory.")
    parser.add_argument("--round-id", default=DEFAULT_ROUND_ID, help="Correction round id.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan and write audit report without modifying files.")
    scan.set_defaults(func=command_scan)

    apply = subparsers.add_parser("apply", help="Apply auto rules and write audit report.")
    apply.set_defaults(func=command_apply)

    report = subparsers.add_parser("report", help="Rebuild report without modifying translation files.")
    report.add_argument(
        "--operations-jsonl",
        default=str(DEFAULT_CORRECTION_DIR / f"{DEFAULT_ROUND_ID}.operations.jsonl"),
        help="Existing operations JSONL to preserve in the rebuilt report.",
    )
    report.set_defaults(func=command_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

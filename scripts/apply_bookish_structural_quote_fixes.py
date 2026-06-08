#!/usr/bin/env python3
"""Apply conservative structural and quote fixes to bookish_zhcn.

This pass intentionally fixes only high-confidence cases:
- source narration that was wrapped as one-line dialogue in Chinese, based on
  reviewed processed_output_v3_1 alignment candidates;
- paired single quotes inside fully closed dialogue lines, normalized to 『』.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKISH_ZHCN = ROOT / "bookish_zhcn"
FINDINGS_JSONL = (
    ROOT
    / "_audit/translation_experiment/corrections/structural_alignment_round_001.findings.jsonl"
)
OUT_DIR = ROOT / "_audit/translation_experiment/corrections"
OUT_JSONL = OUT_DIR / "structural_quote_fixes_round_001.jsonl"
OUT_MD = OUT_DIR / "structural_quote_fixes_round_001.md"


@dataclass(frozen=True)
class LineTarget:
    relative_path: str
    start: int
    end: int

    def contains(self, relative_path: str, line_no: int) -> bool:
        return (
            self.relative_path == relative_path
            and self.start <= line_no <= self.end
        )


SOURCE_UNSPEAKERED_TARGETS = [
    LineTarget("reading_order/01_prologue.md", 1146, 1154),
    LineTarget("appendix/endings_and_recovery.md", 990, 998),
    LineTarget("reading_order/03_chapter2.md", 1121, 1132),
    LineTarget("reading_order/03_chapter2.md", 4265, 4298),
    LineTarget("reading_order/03_chapter2.md", 4301, 4302),
    LineTarget("reading_order/03_chapter2.md", 4781, 4786),
    LineTarget("reading_order/04_chapter3.md", 3443, 3445),
    LineTarget("reading_order/04_chapter3.md", 5158, 5164),
    LineTarget("reading_order/08_hinase.md", 3146, 3157),
    LineTarget("reading_order/16_chapter5_after_kirichiyo_branch.md", 3956, 3959),
    LineTarget("reading_order/16_chapter5_after_kirichiyo_branch.md", 3964, 3971),
    LineTarget("reading_order/17_chapter6.md", 553, 556),
    LineTarget("reading_order/17_chapter6.md", 883, 891),
]

MANUAL_SOURCE_UNSPEAKERED_HINTS = {
    ("reading_order/03_chapter2.md", 4301): {
        "source_file": "chapter2/chapter2_24.txt",
        "source_line": 324,
    },
    ("reading_order/03_chapter2.md", 4302): {
        "source_file": "chapter2/chapter2_24.txt",
        "source_line": 325,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3956): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 75,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3957): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 76,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3958): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 77,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3959): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 78,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3964): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 83,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3965): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 84,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3966): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 85,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3967): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 86,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3968): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 87,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3969): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 88,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3970): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 89,
    },
    ("reading_order/16_chapter5_after_kirichiyo_branch.md", 3971): {
        "source_file": "chapter5/chapter5_48.txt",
        "source_line": 90,
    },
}


DIALOGUE_LINE_RE = re.compile(r"^(?P<prefix>(?:[^:：\n]{1,40}[:：]\s*)?)「(?P<body>.*)」$")
WRAPPED_DIALOGUE_RE = re.compile(r"^(?P<speaker>[^:：\n]{1,40})[:：]\s*「(?P<body>.*)」$")
PAIR_CURLY_SINGLE_RE = re.compile(r"‘([^‘’\n]+)’")
PAIR_ASCII_SINGLE_RE = re.compile(r"(?<![A-Za-z])'([^'\n]+)'(?![A-Za-z])")


def load_source_unspeakered_findings() -> dict[tuple[str, int], dict]:
    findings: dict[tuple[str, int], dict] = {}
    if not FINDINGS_JSONL.exists():
        raise FileNotFoundError(FINDINGS_JSONL)
    with FINDINGS_JSONL.open("r", encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            row = json.loads(raw)
            if row.get("rule_id") != "source_unspeakered_text_wrapped_as_dialogue":
                continue
            key = (row["file"], int(row["line"]))
            findings[key] = row
    return findings


def is_targeted_source_unspeakered(relative_path: str, line_no: int) -> bool:
    return any(target.contains(relative_path, line_no) for target in SOURCE_UNSPEAKERED_TARGETS)


def source_unspeakered_hint(
    relative_path: str,
    line_no: int,
    unspeakered_findings: dict[tuple[str, int], dict],
) -> dict | None:
    key = (relative_path, line_no)
    if key in MANUAL_SOURCE_UNSPEAKERED_HINTS:
        return MANUAL_SOURCE_UNSPEAKERED_HINTS[key]
    if key in unspeakered_findings and is_targeted_source_unspeakered(relative_path, line_no):
        return unspeakered_findings[key]
    if is_targeted_source_unspeakered(relative_path, line_no):
        return {"source_file": None, "source_line": None}
    return None


def strip_dialogue_wrapper(line: str) -> str | None:
    match = WRAPPED_DIALOGUE_RE.match(line)
    if not match:
        return None
    return match.group("body")


def normalize_inner_single_quotes(line: str) -> str | None:
    match = DIALOGUE_LINE_RE.match(line)
    if not match:
        return None
    if line.count("「") != line.count("」"):
        return None

    body = match.group("body")
    normalized = PAIR_CURLY_SINGLE_RE.sub(r"『\1』", body)
    normalized = PAIR_ASCII_SINGLE_RE.sub(r"『\1』", normalized)
    if normalized == body:
        return None
    return f"{match.group('prefix')}「{normalized}」"


def iter_bookish_markdown_files() -> list[Path]:
    files = list((BOOKISH_ZHCN / "reading_order").glob("*.md"))
    files.extend((BOOKISH_ZHCN / "appendix").glob("*.md"))
    return sorted(files)


def read_git_head_lines(path: Path) -> list[str] | None:
    repo_relative = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "show", f"HEAD:{repo_relative}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8").splitlines()


def collect_current_diff_records(
    files: list[Path], unspeakered_findings: dict[tuple[str, int], dict]
) -> list[dict]:
    records: list[dict] = []
    for path in files:
        relative_path = path.relative_to(BOOKISH_ZHCN).as_posix()
        base_lines = read_git_head_lines(path)
        if base_lines is None:
            continue
        current_lines = path.read_text(encoding="utf-8").splitlines()
        max_len = max(len(base_lines), len(current_lines))
        for index in range(max_len):
            before = base_lines[index] if index < len(base_lines) else ""
            after = current_lines[index] if index < len(current_lines) else ""
            if before == after:
                continue
            line_no = index + 1
            key = (relative_path, line_no)

            hint = source_unspeakered_hint(relative_path, line_no, unspeakered_findings)
            if hint and strip_dialogue_wrapper(before) == after:
                records.append(
                    {
                        "kind": "source_unspeakered_dialogue_wrapper_removed",
                        "file": relative_path,
                        "line": line_no,
                        "before": before,
                        "after": after,
                        "source_file": hint.get("source_file"),
                        "source_line": hint.get("source_line"),
                    }
                )
                continue

            if normalize_inner_single_quotes(before) == after:
                records.append(
                    {
                        "kind": "dialogue_inner_single_quotes_to_kakko",
                        "file": relative_path,
                        "line": line_no,
                        "before": before,
                        "after": after,
                    }
                )
                continue

            records.append(
                {
                    "kind": "unclassified_existing_diff",
                    "file": relative_path,
                    "line": line_no,
                    "before": before,
                    "after": after,
                }
            )
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def write_markdown(path: Path, records: list[dict]) -> None:
    counts = Counter(record["kind"] for record in records)
    by_file: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        by_file[record["file"]][record["kind"]] += 1

    lines = [
        "# Structural and quote fixes round 001",
        "",
        "Scope:",
        "- Removed dialogue wrappers only for reviewed high-confidence source narration lines.",
        "- Replaced paired single quotes inside fully closed dialogue lines with 『』.",
        "- Left mixed, unclosed, or source-shape-ambiguous quote cases for manual review.",
        "",
        "Summary:",
    ]
    for kind, count in sorted(counts.items()):
        lines.append(f"- {kind}: {count}")

    lines.extend(["", "By file:"])
    for relative_path in sorted(by_file):
        rendered = ", ".join(
            f"{kind}={count}" for kind, count in sorted(by_file[relative_path].items())
        )
        lines.append(f"- `{relative_path}`: {rendered}")

    lines.extend(["", "Applied changes:", ""])
    for record in records:
        lines.append(f"## {record['kind']} — `{record['file']}:{record['line']}`")
        if record.get("source_file"):
            lines.append(f"- source: `{record['source_file']}:{record['source_line']}`")
        lines.append(f"- before: {record['before']}")
        lines.append(f"- after: {record['after']}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    unspeakered_findings = load_source_unspeakered_findings()
    files = iter_bookish_markdown_files()

    for path in files:
        relative_path = str(path.relative_to(BOOKISH_ZHCN))
        original_lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = list(original_lines)

        for index, line in enumerate(original_lines):
            line_no = index + 1
            if source_unspeakered_hint(relative_path, line_no, unspeakered_findings):
                stripped = strip_dialogue_wrapper(new_lines[index])
                if stripped is not None:
                    new_lines[index] = stripped

        for index, line in enumerate(new_lines):
            normalized = normalize_inner_single_quotes(line)
            if normalized is None:
                continue
            new_lines[index] = normalized

        if new_lines != original_lines:
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    records = collect_current_diff_records(files, unspeakered_findings)
    write_jsonl(OUT_JSONL, records)
    write_markdown(OUT_MD, records)
    print(f"applied records: {len(records)}")
    print(f"jsonl: {OUT_JSONL}")
    print(f"markdown: {OUT_MD}")


if __name__ == "__main__":
    main()

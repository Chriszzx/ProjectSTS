#!/usr/bin/env python3
"""Fix half-open/half-close Japanese quote marks in bookish_zhcn.

The pass is intentionally scoped to bookish_zhcn/reading_order and appendix.
It fixes line-local inner quote damage and a few source-confirmed multi-line
quote shapes, without regenerating complete_epub.md.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKISH = ROOT / "bookish_zhcn"
OUT_DIR = ROOT / "_audit/translation_experiment/corrections"
OUT_JSONL = OUT_DIR / "half_quote_fixes_round_001.jsonl"
OUT_MD = OUT_DIR / "half_quote_fixes_round_001.md"

OUTER_DIALOGUE_RE = re.compile(r"^(?P<prefix>.*?「)(?P<body>.*)(?P<suffix>」.*?)$")
TITLE_WITH_STRAY_CLOSE_RE = re.compile(r"《([^》]+)》』")


PROLOGUE_INNER_QUOTE_LINES = {
    "reading_order/01_prologue.md": {
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        63,
        67,
    },
    "appendix/endings_and_recovery.md": {
        390,
        391,
        392,
        393,
        394,
        395,
        396,
        397,
        398,
        399,
        401,
        402,
        403,
        404,
        405,
        406,
        407,
        408,
        410,
        414,
    },
}

MANUAL_LINE_REPLACEMENTS = {
    (
        "appendix/internal_stories.md",
        226,
    ): "因为两者如果没有现实这个『世界』就无法存在」",
    (
        "appendix/internal_stories.md",
        662,
    ): "你是你的一句话。』",
    (
        "reading_order/02_chapter1.md",
        1823,
    ): "『他』注意到我们后，表情一下子放松了。",
    (
        "reading_order/19_ao.md",
        4689,
    ): "「『那是你也知道的东西。",
    (
        "reading_order/19_ao.md",
        4691,
    ): "那就是我找到的、抵达的答案。』」",
}


def markdown_files() -> list[Path]:
    files = list((BOOKISH / "reading_order").glob("*.md"))
    files.extend((BOOKISH / "appendix").glob("*.md"))
    return sorted(files)


def has_half_quote_shape(line: str) -> bool:
    if line.count("『") != line.count("』"):
        return True
    if line.count("‘") != line.count("’"):
        return True
    return bool(re.search(r"「[^「」『』]*』|『[^「」『』]*」", line))


def rebalance_outer_dialogue(line: str) -> str:
    updated = line
    if "「" in updated or updated.startswith("『"):
        updated = updated.replace("‘", "『").replace("’", "』")
    updated = TITLE_WITH_STRAY_CLOSE_RE.sub(r"『\1』", updated)

    match = OUTER_DIALOGUE_RE.match(updated)
    if not match:
        return updated

    prefix = match.group("prefix")
    body = match.group("body")
    suffix = match.group("suffix")

    first_open = body.find("『")
    first_close = body.find("』")
    if first_close != -1 and (first_open == -1 or first_close < first_open):
        body = "『" + body

    opens = body.count("『")
    closes = body.count("』")
    if opens > closes:
        body += "』" * (opens - closes)
    elif closes > opens:
        body = ("『" * (closes - opens)) + body

    return f"{prefix}{body}{suffix}"


def wrap_outer_body_with_inner_quote(line: str) -> str:
    match = OUTER_DIALOGUE_RE.match(line)
    if not match:
        return line

    prefix = match.group("prefix")
    body = match.group("body")
    suffix = match.group("suffix")
    if body.startswith("『") and body.endswith("』"):
        return line
    return f"{prefix}『{body}』{suffix}"


def fix_line(relative_path: str, line_no: int, line: str) -> tuple[str, str | None]:
    manual = MANUAL_LINE_REPLACEMENTS.get((relative_path, line_no))
    if manual is not None and line != manual:
        return manual, "source_confirmed_multiline_quote"

    if line_no in PROLOGUE_INNER_QUOTE_LINES.get(relative_path, set()):
        updated = rebalance_outer_dialogue(line)
        updated = wrap_outer_body_with_inner_quote(updated)
        if updated != line:
            return updated, "source_confirmed_prologue_inner_quote"
        return line, None

    if not has_half_quote_shape(line):
        return line, None

    updated = rebalance_outer_dialogue(line)
    if updated != line:
        return updated, "line_local_half_quote_rebalanced"
    return line, None


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
        "# Half quote fixes round 001",
        "",
        "Scope:",
        "- `bookish_zhcn/reading_order/*.md`",
        "- `bookish_zhcn/appendix/*.md`",
        "",
        "Policy:",
        "- Outer dialogue remains `「」`.",
        "- Source-confirmed inner quotes use `『』`.",
        "- Multi-line `『...』` blocks without local damage are left untouched.",
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
        lines.append(f"- before: {record['before']}")
        lines.append(f"- after: {record['after']}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


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


def collect_current_diff_records(files: list[Path]) -> list[dict]:
    records: list[dict] = []
    for path in files:
        relative_path = path.relative_to(BOOKISH).as_posix()
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
            fixed, kind = fix_line(relative_path, index + 1, before)
            if kind and fixed == after:
                records.append(
                    {
                        "kind": kind,
                        "file": relative_path,
                        "line": index + 1,
                        "before": before,
                        "after": after,
                    }
                )
    return records


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = markdown_files()

    for path in files:
        relative_path = path.relative_to(BOOKISH).as_posix()
        old_lines = path.read_text(encoding="utf-8").splitlines()
        new_lines: list[str] = []
        for line_no, line in enumerate(old_lines, 1):
            fixed, kind = fix_line(relative_path, line_no, line)
            new_lines.append(fixed)

        if new_lines != old_lines:
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    records = collect_current_diff_records(files)
    write_jsonl(OUT_JSONL, records)
    write_markdown(OUT_MD, records)
    print(f"applied records: {len(records)}")
    print(f"jsonl: {OUT_JSONL}")
    print(f"markdown: {OUT_MD}")


if __name__ == "__main__":
    main()

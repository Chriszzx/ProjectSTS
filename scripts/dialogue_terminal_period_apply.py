#!/usr/bin/env python3
"""Remove final Chinese full stops inside dialogue corner quotes."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKISH = ROOT / "bookish_zhcn"

ANOMALY_REPLACEMENTS = {
    "我撅起嘴，心想「你明明知道」。」": "我撅起嘴，心想「你明明知道」",
    "仿佛在说「今天我就陪你任性一整天」。」": "仿佛在说「今天我就陪你任性一整天」",
}


def target_files() -> list[Path]:
    files: set[Path] = set()
    files.update(BOOKISH.glob("*.md"))
    files.update((BOOKISH / "reading_order").glob("*.md"))
    files.update((BOOKISH / "appendix").glob("*.md"))
    files.discard(BOOKISH / "complete_epub.md")
    return sorted(files)


def clean_text(text: str) -> tuple[str, int]:
    count = text.count("。」")
    for before, after in ANOMALY_REPLACEMENTS.items():
        text = text.replace(before, after)
    text = text.replace("。」", "」")
    return text, count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    total = 0
    changed: list[tuple[Path, int]] = []
    for path in target_files():
        original = path.read_text(encoding="utf-8")
        cleaned, count = clean_text(original)
        if cleaned == original:
            continue
        total += count
        changed.append((path, count))
        if not args.dry_run:
            path.write_text(cleaned.rstrip() + "\n", encoding="utf-8")

    for path, count in changed:
        print(f"{path.relative_to(ROOT)}\t{count}")
    print(f"total\t{total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Normalize bookish zh-CN route headings to source scene markers."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from branch_explore_arc import parse_arc as arc  # noqa: E402


DATA_DIR = ROOT / "branch_explore_arc"
BOOKISH_ZHCN_DIR = ROOT / "bookish_zhcn"


ROOT_CHAPTER_SPECS: list[tuple[str, str]] = [
    ("02_chapter1.md", "一章"),
    ("03_chapter2.md", "二章"),
    ("04_chapter3.md", "三章"),
    ("06_chapter4.md", "四章"),
    ("08_chapter5.md", "五章"),
    ("11_chapter6.md", "六章"),
]


READING_ORDER_SPECS: list[tuple[str, str, dict[str, Any]]] = [
    ("02_chapter1.md", "一章", {}),
    ("03_chapter2.md", "二章", {}),
    ("04_chapter3.md", "三章", {}),
    ("06_chapter4_to_hinase_branch.md", "四章", {"scene_max": 131}),
    (
        "07_hinase_chapter4_branch.md",
        "四章",
        {"scene_min": 132, "scene_max": 142, "active_route_keys": ["hinase"]},
    ),
    (
        "09_chapter4_after_hinase_branch.md",
        "四章",
        {"scene_min": 132, "active_route_keys": ["kirishima", "chiyo", "toya", "ao"]},
    ),
    ("10_chapter5_to_kirichiyo_branch.md", "五章", {"scene_max": 231}),
    (
        "11_kirishima_chapter5_branch.md",
        "五章",
        {"scene_min": 232, "scene_max": 235, "active_route_keys": ["kirishima"]},
    ),
    (
        "13_chiyo_chapter5_branch.md",
        "五章",
        {"scene_min": 232, "scene_max": 235, "active_route_keys": ["chiyo"]},
    ),
    (
        "16_chapter5_after_kirichiyo_branch.md",
        "五章",
        {"scene_min": 232, "active_route_keys": ["toya", "ao"]},
    ),
    ("17_chapter6.md", "六章", {}),
]


def load_data() -> tuple[dict[str, Any], dict[str, Any], dict[int, dict[str, Any]]]:
    scenes = json.loads((DATA_DIR / "scene_annotations.json").read_text(encoding="utf-8"))
    disasm = json.loads((DATA_DIR / "disasm.json").read_text(encoding="utf-8"))
    route_plan = json.loads((BOOKISH_ZHCN_DIR / "route_plan.json").read_text(encoding="utf-8"))
    data = {"scene_annotations": scenes, "full_disasm": disasm}
    return data, route_plan, {scene["scene_index"]: scene for scene in scenes}


def marker_for_scene(scene: dict[str, Any]) -> str:
    raw_title = arc.bookish_display_scene_title(scene)
    translated_title = arc.translate_bookish_heading(raw_title)
    translated_chapter = arc.translate_bookish_heading(scene.get("chapter") or "")
    marker = translated_title
    prefix = f"{translated_chapter}-"
    if marker.startswith(prefix):
        marker = marker[len(prefix) :]
    marker = marker.replace("結末", "结末").replace("終", "终")
    return marker


def chapter_blocks(data: dict[str, Any], route_plan: dict[str, Any], chapter: str) -> list[dict[str, Any]]:
    route_keys = arc.BOOKISH_CHAPTER_ROUTE_KEYS.get(chapter, arc.BOOKISH_PRIMARY_ROUTE_KEYS)
    return arc.build_bookish_chapter_section_blocks(data, route_plan, chapter, route_keys)


def filtered_blocks(
    data: dict[str, Any],
    route_plan: dict[str, Any],
    chapter: str,
    filters: dict[str, Any],
) -> list[dict[str, Any]]:
    return arc.filtered_bookish_blocks(chapter_blocks(data, route_plan, chapter), **filters)


def replace_or_insert_heading(segment: list[str], marker: str) -> bool:
    new_heading = f"## {marker}"
    for index, line in enumerate(segment):
        if line.startswith("## "):
            if line == new_heading:
                return False
            segment[index] = new_heading
            return True

    insert_at = 0
    if segment and segment[0].startswith("# "):
        insert_at = 1

    while insert_at < len(segment):
        line = segment[insert_at]
        if not line.strip() or line.startswith("<!-- anchor:"):
            insert_at += 1
            continue
        break

    insertion = [new_heading, ""]
    if insert_at > 0 and segment[insert_at - 1].strip():
        insertion.insert(0, "")
    segment[insert_at:insert_at] = insertion
    return True


def write_segments(path: Path, segments: list[list[str]]) -> None:
    output: list[str] = []
    for index, segment in enumerate(segments):
        if index:
            while output and not output[-1].strip():
                output.pop()
            output.extend(["", "---", ""])
        output.extend(segment)
    path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def normalize_file(
    path: Path,
    blocks: list[dict[str, Any]],
    scenes_by_index: dict[int, dict[str, Any]],
    *,
    dry_run: bool,
) -> int:
    if not path.exists():
        return 0

    original = path.read_text(encoding="utf-8")
    segments = arc.split_markdown_segments(original.splitlines())
    changed = 0

    for index, block in enumerate(blocks):
        if index >= len(segments):
            break
        scene = scenes_by_index.get(block["scene_index"])
        if not scene:
            continue
        if replace_or_insert_heading(segments[index], marker_for_scene(scene)):
            changed += 1

    if changed and not dry_run:
        write_segments(path, segments)
    return changed


def refresh_complete_markdown() -> None:
    manifest = json.loads((BOOKISH_ZHCN_DIR / "manifest.json").read_text(encoding="utf-8"))
    frontmatter = manifest["epub"].get("frontmatter_files", [])
    source_files = [item for item in manifest["epub"]["source_files"] if item not in frontmatter]
    arc.write_bookish_complete_markdown(
        BOOKISH_ZHCN_DIR,
        [*frontmatter, *source_files],
        BOOKISH_ZHCN_DIR / "complete_epub.md",
        arc.BOOKISH_ZHCN_EPUB_TITLE,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-refresh-complete", action="store_true")
    args = parser.parse_args()

    data, route_plan, scenes_by_index = load_data()
    changed_by_file: dict[str, int] = {}

    for filename, chapter in ROOT_CHAPTER_SPECS:
        changed = normalize_file(
            BOOKISH_ZHCN_DIR / filename,
            chapter_blocks(data, route_plan, chapter),
            scenes_by_index,
            dry_run=args.dry_run,
        )
        if changed:
            changed_by_file[filename] = changed

    reading_order_dir = BOOKISH_ZHCN_DIR / arc.BOOKISH_READING_ORDER_DIRNAME
    for filename, chapter, filters in READING_ORDER_SPECS:
        changed = normalize_file(
            reading_order_dir / filename,
            filtered_blocks(data, route_plan, chapter, filters),
            scenes_by_index,
            dry_run=args.dry_run,
        )
        if changed:
            changed_by_file[f"{arc.BOOKISH_READING_ORDER_DIRNAME}/{filename}"] = changed

    if changed_by_file and not args.dry_run and not args.no_refresh_complete:
        refresh_complete_markdown()

    for filename, count in changed_by_file.items():
        print(f"{filename}: {count}")
    if not changed_by_file:
        print("No scene heading changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

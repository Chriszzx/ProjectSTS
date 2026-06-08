#!/usr/bin/env python3
"""Sync the ignored Japanese bookish tree to the reviewed zh-CN structure."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from branch_explore_arc import parse_arc as arc  # noqa: E402


BOOKISH = ROOT / "bookish"
READING = BOOKISH / arc.BOOKISH_READING_ORDER_DIRNAME
APPENDIX = BOOKISH / "appendix" / "endings_and_recovery.md"
STRUCTURE_DOC = "_audit/translation_experiment/bookish_structure_constraints.md"

JA_TITLE = "死神と少女 完全脚本"
JA_AUTHOR = "藤文/takuyo"
FRONTMATTER = ["book_toc.md", "reader_manual.md"]

JA_DIVIDER_SPECS = [
    {"file": "dividers/00_story.md", "title": "本文", "before": "reading_order/00_name.md"},
    {"file": "dividers/01_prologue.md", "title": "序章", "before": "reading_order/01_prologue.md"},
    {"file": "dividers/02_chapter1.md", "title": "一章", "before": "reading_order/02_chapter1.md"},
    {"file": "dividers/03_chapter2.md", "title": "二章", "before": "reading_order/03_chapter2.md"},
    {"file": "dividers/04_chapter3.md", "title": "三章", "before": "reading_order/04_chapter3.md"},
    {"file": "dividers/05_natsuko.md", "title": "夏帆", "before": "reading_order/05_natsuko.md"},
    {"file": "dividers/06_chapter4.md", "title": "四章", "before": "reading_order/06_chapter4_to_hinase_branch.md"},
    {"file": "dividers/07_hinase.md", "title": "日生光ルート", "before": "reading_order/07_hinase_chapter4_branch.md"},
    {"file": "dividers/08_chapter5.md", "title": "五章", "before": "reading_order/10_chapter5_to_kirichiyo_branch.md"},
    {"file": "dividers/09_kirishima.md", "title": "桐島七葵ルート", "before": "reading_order/11_kirishima_chapter5_branch.md"},
    {"file": "dividers/10_chiyo.md", "title": "千代ルート", "before": "reading_order/13_chiyo_chapter5_branch.md"},
    {"file": "dividers/11_chapter6.md", "title": "六章", "before": "reading_order/17_chapter6.md"},
    {"file": "dividers/12_kuro.md", "title": "黒の章", "before": "reading_order/18_kuro.md"},
    {"file": "dividers/13_ao.md", "title": "蒼の章", "before": "reading_order/19_ao.md"},
    {"file": "dividers/14_atogaki.md", "title": "あとがき", "before": "reading_order/20_atogaki.md"},
    {"file": "dividers/15_appendix.md", "title": "附録", "before": arc.BOOKISH_ENDINGS_AND_RECOVERY_FILE},
]

JA_TOC_ITEMS = [
    ("名前", "reading_order/00_name.md"),
    ("はじまり", "reading_order/00_hajimari_gate.md"),
    ("序章", "reading_order/01_prologue.md"),
    ("一章", "reading_order/02_chapter1.md"),
    ("二章", "reading_order/03_chapter2.md"),
    ("三章", "reading_order/04_chapter3.md"),
    ("夏帆", "reading_order/05_natsuko.md"),
    ("四章", "reading_order/06_chapter4_to_hinase_branch.md"),
    ("日生光ルート", "reading_order/07_hinase_chapter4_branch.md"),
    ("五章", "reading_order/10_chapter5_to_kirichiyo_branch.md"),
    ("桐島七葵ルート", "reading_order/11_kirishima_chapter5_branch.md"),
    ("千代ルート", "reading_order/13_chiyo_chapter5_branch.md"),
    ("六章", "reading_order/17_chapter6.md"),
    ("黒の章", "reading_order/18_kuro.md"),
    ("蒼の章", "reading_order/19_ao.md"),
    ("あとがき", "reading_order/20_atogaki.md"),
    ("附録：結末と回収", arc.BOOKISH_ENDINGS_AND_RECOVERY_FILE),
    ("附録：内部資料", arc.BOOKISH_INTERNAL_STORIES_FILE),
]

JA_TOC_TITLES: dict[str, str | None] = {
    "book_toc.md": "目次",
    "reader_manual.md": "読本説明",
    "reading_order/00_name.md": "名前",
    "reading_order/00_hajimari_gate.md": "はじまり",
    "reading_order/00_hajimari.md": None,
    "reading_order/01_prologue.md": "序章",
    "reading_order/02_chapter1.md": "一章",
    "reading_order/03_chapter2.md": "二章",
    "reading_order/04_chapter3.md": "三章",
    "reading_order/05_natsuko.md": "夏帆",
    "reading_order/06_chapter4_to_hinase_branch.md": "四章",
    "reading_order/07_hinase_chapter4_branch.md": "日生光ルート",
    "reading_order/08_hinase.md": None,
    "reading_order/09_chapter4_after_hinase_branch.md": None,
    "reading_order/10_chapter5_to_kirichiyo_branch.md": "五章",
    "reading_order/11_kirishima_chapter5_branch.md": "桐島七葵ルート",
    "reading_order/12_kirishima.md": None,
    "reading_order/13_chiyo_chapter5_branch.md": "千代ルート",
    "reading_order/14_chiyo_kirishima_branch.md": None,
    "reading_order/15_chiyo.md": None,
    "reading_order/16_chapter5_after_kirichiyo_branch.md": None,
    "reading_order/17_chapter6.md": "六章",
    "reading_order/18_kuro.md": "黒の章",
    "reading_order/19_ao.md": "蒼の章",
    "reading_order/20_atogaki.md": "あとがき",
    arc.BOOKISH_ENDINGS_AND_RECOVERY_FILE: "附録：結末と回収",
    arc.BOOKISH_INTERNAL_STORIES_FILE: "附録：内部資料",
}

for spec in JA_DIVIDER_SPECS:
    JA_TOC_TITLES[spec["file"]] = None

JA_NAVIGATION_LINKS = {
    "reading_order/00_name.md": [("続けて読む：", "はじまり", "reading_order/00_hajimari_gate.md")],
    "reading_order/00_hajimari_gate.md": [
        ("続けて読む：", "はじまり", "reading_order/00_hajimari.md"),
        ("飛ぶ：", "序章", "reading_order/01_prologue.md"),
    ],
    "reading_order/00_hajimari.md": [("続けて読む：", "序章", "reading_order/01_prologue.md")],
    "reading_order/01_prologue.md": [("続けて読む：", "一章", "reading_order/02_chapter1.md")],
    "reading_order/02_chapter1.md": [("続けて読む：", "二章", "reading_order/03_chapter2.md")],
    "reading_order/03_chapter2.md": [("続けて読む：", "三章", "reading_order/04_chapter3.md")],
    "reading_order/04_chapter3.md": [("続けて読む：", "夏帆", "reading_order/05_natsuko.md")],
    "reading_order/05_natsuko.md": [("続けて読む：", "四章", "reading_order/06_chapter4_to_hinase_branch.md")],
    "reading_order/06_chapter4_to_hinase_branch.md": [
        ("続けて読む：", "日生光ルート", "reading_order/07_hinase_chapter4_branch.md"),
        ("飛ぶ：", "四章後半", "reading_order/09_chapter4_after_hinase_branch.md"),
    ],
    "reading_order/07_hinase_chapter4_branch.md": [("続けて読む：", "日生光ルート", "reading_order/08_hinase.md")],
    "reading_order/08_hinase.md": [("戻る：", "四章後半", "reading_order/09_chapter4_after_hinase_branch.md")],
    "reading_order/09_chapter4_after_hinase_branch.md": [("続けて読む：", "五章", "reading_order/10_chapter5_to_kirichiyo_branch.md")],
    "reading_order/10_chapter5_to_kirichiyo_branch.md": [
        ("続けて読む：", "桐島七葵ルート", "reading_order/11_kirishima_chapter5_branch.md"),
        ("続けて読む：", "千代ルート", "reading_order/13_chiyo_chapter5_branch.md"),
        ("飛ぶ：", "五章後半", "reading_order/16_chapter5_after_kirichiyo_branch.md"),
    ],
    "reading_order/11_kirishima_chapter5_branch.md": [("続けて読む：", "桐島七葵ルート", "reading_order/12_kirishima.md")],
    "reading_order/12_kirishima.md": [("戻る：", "五章後半", "reading_order/16_chapter5_after_kirichiyo_branch.md")],
    "reading_order/13_chiyo_chapter5_branch.md": [("続けて読む：", "千代ルート", "reading_order/14_chiyo_kirishima_branch.md")],
    "reading_order/14_chiyo_kirishima_branch.md": [("続けて読む：", "千代ルート", "reading_order/15_chiyo.md")],
    "reading_order/15_chiyo.md": [("戻る：", "五章後半", "reading_order/16_chapter5_after_kirichiyo_branch.md")],
    "reading_order/16_chapter5_after_kirichiyo_branch.md": [("続けて読む：", "六章", "reading_order/17_chapter6.md")],
    "reading_order/17_chapter6.md": [
        ("黒の章へ：", "黒の章", "reading_order/18_kuro.md"),
        ("蒼の章へ：", "蒼の章", "reading_order/19_ao.md"),
    ],
    "reading_order/18_kuro.md": [("飛ぶ：", "蒼の章", "reading_order/19_ao.md")],
    "reading_order/19_ao.md": [("続けて読む：", "あとがき", "reading_order/20_atogaki.md")],
    "reading_order/20_atogaki.md": [("続けて読む：", "附録", arc.BOOKISH_ENDINGS_AND_RECOVERY_FILE)],
}

FINE_NAV_LABELS = {
    "hinase": "日生光",
    "kirishima": "桐島七葵",
    "chiyo": "千代",
    "toya": "遠野十夜",
    "ao": "蒼",
}

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
    ("07_hinase_chapter4_branch.md", "四章", {"scene_min": 132, "scene_max": 142, "active_route_keys": ["hinase"]}),
    ("09_chapter4_after_hinase_branch.md", "四章", {"scene_min": 132, "active_route_keys": ["kirishima", "chiyo", "toya", "ao"]}),
    ("10_chapter5_to_kirichiyo_branch.md", "五章", {"scene_max": 231}),
    ("11_kirishima_chapter5_branch.md", "五章", {"scene_min": 232, "scene_max": 235, "active_route_keys": ["kirishima"]}),
    ("13_chiyo_chapter5_branch.md", "五章", {"scene_min": 232, "scene_max": 235, "active_route_keys": ["chiyo"]}),
    ("16_chapter5_after_kirichiyo_branch.md", "五章", {"scene_min": 232, "active_route_keys": ["toya", "ao"]}),
    ("17_chapter6.md", "六章", {}),
]

HINASE_NO_MORE_LIES = """遠野　紗夜: 「もう嘘を吐かないで下さい」
日生 光: 「どうして？」
遠野　紗夜: 「どうして……って、嘘を吐かれればとても悲しいからです」
遠野　紗夜: 「嘘は必ず誰かを傷つけます。貴方自身だって……」
日生 光: 「僕は嘘に救われてるよ」
遠野　紗夜: 「あ…………」
あの時、彼が話した物語を思い出した。
嘘吐きな少年の物語。
彼が嘘吐きならば、もしかしてあの物語も嘘だったのかもしれない。
一度嘘を吐けば、その嘘を隠す為に、また別の嘘を吐かなければいけなくて、嘘は次々に増えていく。
一度疑い出せばきりがない。
今の言葉だって、もう信じられないから。
ぽつりと私の目から一滴の水が零れた。
そして、もう一滴。
もう一滴。
遠野　紗夜: 「…………」
遠野　紗夜: 「……一つだけ、答えてくれますか？」
日生 光: 「いいよ」
遠野　紗夜: 「私を愛していますか？」
彼は何の迷いもなく言った。
日生 光: 「愛してる」
遠野　紗夜: 「嘘吐き」
私がそう言うと、彼は笑った。
その後、彼は私の前に現れることは二度となかった。
遠野　紗夜: 「さようなら、偽物の王子様」"""

AO_CANNOT_PROMISE = """遠野　紗夜: 「約束出来ません」
遠野 十夜: 「紗夜……」
遠野　紗夜: 「約束出来ません。そんなもの。だって、私は兄さんの傍にいたいのです」
遠野 十夜: 「紗夜。だけど、それは……！」
私は体を向き変え、兄を真摯に見つめた。
遠野　紗夜: 「……ねえ、十夜兄さん。私はやはりもうすぐ死んでしまうのでしょう？」
遠野 十夜: 「……そんなことはない」
遠野　紗夜: 「嘘。だって、兄さんは言ったではありませんか。『このまま苦しんで死ぬよりは良い』と」
遠野 十夜: 「！　それは……！」
兄は苦々しく顔を歪ませた。私はその頬に触れ、下へとゆっくり手を滑らせた。
遠野　紗夜: 「どのみち死ぬのなら、私は兄さんの傍で死にたいです……」
手は兄の胸元まで辿りつき、そのまま頭を預ける。
彼は直ぐには抱きしめてくれなかったが、やがて、兄は私の背中に手を回し、押しつけるように抱きしめてくれた。
遠野 十夜: 「蒼は良いのかい？」
耳元で囁いた言葉に私は目を細ませ、間を置いて言った。
遠野　紗夜: 「……はい」
遠野　紗夜: そう答えた次の瞬間、少女に今まで一番の苦しみが襲った。
遠野　紗夜: 少女はもがき苦しみながら、今までのことを振り返った。
遠野　紗夜: 少女は旅をしてきた。
遠野　紗夜: ずっと、ずっと長い旅を。
遠野　紗夜: けれど、それももうここでお終い。
遠野　紗夜: 少女の旅は、世界で一番美しい言葉を知ることなく終わる。
遠野　紗夜: もう少しでそれが何か見つけることが出来たというのに。
遠野　紗夜: そして、少女はそのままゆっくりと本を閉じたのだった。"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_if_changed(path: Path, text: str, changed: list[str]) -> None:
    text = text.rstrip() + "\n"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())


def clean_body(block: str) -> str:
    lines = block.strip().splitlines()[1:]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and lines[0].strip() == "---":
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and lines[-1].strip() == "---":
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
    return "\n".join(lines).strip()


def extract_heading_block(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    end = text.find(next_heading, start) if next_heading else len(text)
    if end < 0:
        end = len(text)
    return clean_body(text[start:end])


def remove_heading_block(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start < 0:
        return text
    end = text.find(next_heading, start) if next_heading else len(text)
    if end < 0:
        end = len(text)
    separator = "\n---\n\n"
    remove_start = start
    if text[max(0, start - len(separator)) : start] == separator:
        remove_start = start - len(separator)
    before = text[:remove_start].rstrip()
    after = text[end:].lstrip()
    if not after:
        return before + "\n"
    return f"{before}\n\n---\n\n{after}"


def add_choice_link(text: str, choice_line: str, anchor: str, nav_line: str, *, context: str | None = None) -> str:
    search_from = text.index(context) if context else 0
    choice_at = text.index(choice_line, search_from)
    anchor_line = f"<!-- anchor: {anchor} -->"
    if anchor_line not in text:
        text = text[:choice_at] + f"{anchor_line}\n\n" + text[choice_at:]
        choice_at += len(f"{anchor_line}\n\n")
    if nav_line not in text:
        insert_at = text.index(choice_line, choice_at) + len(choice_line)
        text = text[:insert_at] + "\n" + nav_line + text[insert_at:]
    return text


def insert_section_before(text: str, before_line: str, anchor: str, section: str) -> str:
    if f"<!-- anchor: {anchor} -->" in text:
        return text
    insert_at = text.index(before_line)
    return text[:insert_at] + section.rstrip() + "\n\n---\n\n" + text[insert_at:]


def append_section(text: str, anchor: str, section: str) -> str:
    if f"<!-- anchor: {anchor} -->" in text:
        return text
    return text.rstrip() + "\n\n---\n\n" + section.rstrip() + "\n"


def href_for(source_file: str) -> str:
    return arc.bookish_xhtml_filename(source_file).removeprefix("text/")


def write_frontmatter() -> list[str]:
    toc_lines = ["# 目次", ""]
    for label, source_file in JA_TOC_ITEMS:
        toc_lines.append(f"- [{label}]({href_for(source_file)})")
    write_text(BOOKISH / "book_toc.md", "\n".join(toc_lines))

    manual = """# 日本語版読本説明

## これは何か

これは《死神と少女》の日本語原文を、現在の zh-CN 読本と同じ構造で並べ直した参照用 bookish ツリーです。翻訳実験で原文と訳文を比較しやすくするため、章順、分岐、結末、bad end、附録の配置を zh-CN 側に合わせています。

## 読み方

前方の「目次」から各章へ移動できます。「選択：……」はゲーム内の選択点を残した構造マーカーです。「続けて読む」「戻る」「飛ぶ」などの行は、現在の読本順で次に読む場所を示します。

## 小見出し

本文中の `## 01`、`## 15-1`、`## 結末` などの小見出しは、原作から抽出した scene 標識です。人物名やルート名ではなく、原 scene との対応を確認するための番号です。同じ番号が続く場合は、同一 scene 内に複数ルートや条件差分があることを示します。

## 編集方針

この `bookish/` ツリーは日本語原文のローカル参照であり、git には入れません。構造を再同期する場合は `python3 scripts/bookish_sync_ja_structure.py` を実行してください。
"""
    write_text(BOOKISH / "reader_manual.md", manual)
    return FRONTMATTER


def write_dividers() -> list[str]:
    files: list[str] = []
    for spec in JA_DIVIDER_SPECS:
        write_text(BOOKISH / spec["file"], f"# {spec['title']}")
        files.append(spec["file"])
    return files


def append_ja_navigation(path: Path, source_file: str) -> None:
    entries = JA_NAVIGATION_LINKS.get(source_file, [])
    if not entries:
        return
    lines = [f"> {prefix}[{label}]({href_for(target)})" for prefix, label, target in entries]
    original = path.read_text(encoding="utf-8").rstrip()
    path.write_text(f"{original}\n\n---\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def route_keys_for_label(label: str | None, active_route_keys: list[str]) -> set[str]:
    if not label or label in {"全員共通", "全员共通"}:
        return set(active_route_keys)
    keys: set[str] = set()
    for part in label.split("・"):
        compact = part.strip()
        for route_key, route_label in FINE_NAV_LABELS.items():
            if compact == route_label and route_key in active_route_keys:
                keys.add(route_key)
    return keys


def apply_ja_fine_navigation(path: Path, source_file: str) -> None:
    active_route_keys = arc.BOOKISH_FINE_NAVIGATION_ACTIVE_ROUTES.get(source_file)
    if not active_route_keys:
        return

    segments = arc.split_markdown_segments(path.read_text(encoding="utf-8").splitlines())
    block_infos: list[dict[str, Any]] = []
    for segment_index, segment in enumerate(segments):
        if not any(line.strip() for line in segment):
            continue
        label = arc.markdown_segment_heading_label(segment)
        route_keys = route_keys_for_label(label, active_route_keys)
        if route_keys:
            block_infos.append(
                {
                    "segment_index": segment_index,
                    "route_keys": route_keys,
                    "anchor": f"route-block-{segment_index + 1:03d}",
                }
            )

    if len(block_infos) < 2:
        return

    appended_by_segment: dict[int, list[str]] = defaultdict(list)
    for block_position, block in enumerate(block_infos):
        grouped_targets: dict[int, list[str]] = defaultdict(list)
        for route_key in active_route_keys:
            if route_key not in block["route_keys"]:
                continue
            target_position: int | None = None
            for next_position in range(block_position + 1, len(block_infos)):
                if route_key in block_infos[next_position]["route_keys"]:
                    target_position = next_position
                    break
            if target_position is None or target_position == block_position + 1:
                continue
            grouped_targets[target_position].append(route_key)

        for target_position, route_keys in grouped_targets.items():
            target = block_infos[target_position]
            label = "・".join(FINE_NAV_LABELS[route_key] for route_key in route_keys)
            appended_by_segment[block["segment_index"]].append(
                f"> {label}ルートを続ける：[次の場面](#{target['anchor']})"
            )

    if not appended_by_segment:
        return

    for block in block_infos:
        arc.insert_markdown_anchor(segments[block["segment_index"]], block["anchor"])

    for segment_index, nav_lines in appended_by_segment.items():
        segment = segments[segment_index]
        while segment and not segment[-1].strip():
            segment.pop()
        if segment:
            segment.append("")
        segment.extend(nav_lines)

    write_segments(path, segments)


def marker_for_scene(scene: dict[str, Any]) -> str:
    marker = arc.bookish_display_scene_title(scene)
    chapter = scene.get("chapter") or ""
    prefix = f"{chapter}-"
    if marker.startswith(prefix):
        marker = marker[len(prefix) :]
    return marker


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


def chapter_blocks(data: dict[str, Any], route_plan: dict[str, Any], chapter: str) -> list[dict[str, Any]]:
    route_keys = arc.BOOKISH_CHAPTER_ROUTE_KEYS.get(chapter, arc.BOOKISH_PRIMARY_ROUTE_KEYS)
    return arc.build_bookish_chapter_section_blocks(data, route_plan, chapter, route_keys)


def normalize_file(path: Path, blocks: list[dict[str, Any]], scenes_by_index: dict[int, dict[str, Any]]) -> int:
    if not path.exists():
        return 0
    segments = arc.split_markdown_segments(path.read_text(encoding="utf-8").splitlines())
    changed = 0
    for index, block in enumerate(blocks):
        if index >= len(segments):
            break
        scene = scenes_by_index.get(block["scene_index"])
        if scene and replace_or_insert_heading(segments[index], marker_for_scene(scene)):
            changed += 1
    if changed:
        write_segments(path, segments)
    return changed


def normalize_scene_headings(data: dict[str, Any], route_plan: dict[str, Any]) -> dict[str, int]:
    scenes_by_index = {scene["scene_index"]: scene for scene in data["scene_annotations"]}
    changed_by_file: dict[str, int] = {}

    for filename, chapter in ROOT_CHAPTER_SPECS:
        changed = normalize_file(BOOKISH / filename, chapter_blocks(data, route_plan, chapter), scenes_by_index)
        if changed:
            changed_by_file[filename] = changed

    for filename, chapter, filters in READING_ORDER_SPECS:
        blocks = arc.filtered_bookish_blocks(chapter_blocks(data, route_plan, chapter), **filters)
        changed = normalize_file(READING / filename, blocks, scenes_by_index)
        if changed:
            changed_by_file[f"{arc.BOOKISH_READING_ORDER_DIRNAME}/{filename}"] = changed
    return changed_by_file


def apply_navigation(reading_order_files: list[str]) -> None:
    for source_file in reading_order_files:
        path = BOOKISH / source_file
        apply_ja_fine_navigation(path, source_file)
    for source_file in reading_order_files:
        append_ja_navigation(BOOKISH / source_file, source_file)


def integrate_endings() -> list[str]:
    changed: list[str] = []
    appendix = read(APPENDIX)
    ch1_054 = extract_heading_block(appendix, "### 054. 一章-終", "### 227. 日生-終１")
    hinase_227 = extract_heading_block(appendix, "### 227. 日生-終１", "### 228. 日生-終２")
    hinase_228 = extract_heading_block(appendix, "### 228. 日生-終２", "### 340. 六章-終")
    ch6_340 = extract_heading_block(appendix, "### 340. 六章-終", "### 377. 黒の章-終")
    kuro_377 = extract_heading_block(appendix, "### 377. 黒の章-終", "### 415. 蒼の章-終")
    ao_415 = extract_heading_block(appendix, "### 415. 蒼の章-終", None)
    missing = [
        name
        for name, body in {
            "一章-終": ch1_054,
            "日生-終１": hinase_227,
            "日生-終２": hinase_228,
            "六章-終": ch6_340,
            "黒の章-終": kuro_377,
            "蒼の章-終": ao_415,
        }.items()
        if not body
    ]
    if missing:
        raise RuntimeError(f"Missing Japanese appendix blocks: {', '.join(missing)}")

    ch1 = read(READING / "02_chapter1.md")
    ch1 = add_choice_link(
        ch1,
        "> 選択：承知する",
        "badend-ch1-016-choice",
        "> 飛ぶ：[一章-終](#badend-ch1-054)（選択「承知しない」）",
    )
    ch1 = add_choice_link(
        ch1,
        "> 選択：兄に事情を話す",
        "badend-ch1-034-choice",
        "> 飛ぶ：[一章-終](#badend-ch1-054)（選択「兄に話さない」）",
    )
    ch1_section = f"""<!-- anchor: badend-ch1-054 -->
## 一章-終

> 進入条件：一章 16-1 で「承知しない」、または一章 34 で「兄に話さない」を選択。

### 終

{ch1_054}

> 選択に戻る：[一章 16-1](#badend-ch1-016-choice) / [一章 34](#badend-ch1-034-choice)"""
    ch1 = insert_section_before(ch1, "> 続けて読む：[二章](reading_order_03_chapter2.xhtml)", "badend-ch1-054", ch1_section)
    write_if_changed(READING / "02_chapter1.md", ch1, changed)

    hinase = read(READING / "08_hinase.md")
    hinase = add_choice_link(
        hinase,
        "> 選択：嘘を吐いて",
        "badend-hinase-034-choice",
        "> 飛ぶ：[日生-終](#badend-hinase-227)（選択「嘘を吐かないで」）",
    )
    hinase_section = f"""<!-- anchor: badend-hinase-227 -->
## 日生-終

> 進入条件：日生 34 で「嘘を吐かないで」を選択。

### 嘘を吐かないで

{HINASE_NO_MORE_LIES}

### 終1

{hinase_227}

### 終2

{hinase_228}

> 選択に戻る：[日生 34](#badend-hinase-034-choice)"""
    hinase = insert_section_before(hinase, "> 戻る：[四章後半](reading_order_09_chapter4_after_hinase_branch.xhtml)", "badend-hinase-227", hinase_section)
    write_if_changed(READING / "08_hinase.md", hinase, changed)

    ch6_choice = """<!-- anchor: badend-ch6-choice -->

> 選択：抗う
> 飛ぶ：[六章-終](#badend-ch6-340)（選択「諦める」）"""
    ch6_section = f"""<!-- anchor: badend-ch6-340 -->
## 六章-終

> 進入条件：六章 01 で「諦める」を選択。

### 終

{ch6_340}

> 選択に戻る：[六章 01](#badend-ch6-choice)"""
    for path in [BOOKISH / "11_chapter6.md", READING / "17_chapter6.md"]:
        ch6 = read(path)
        if "badend-ch6-choice" not in ch6:
            ch6 = ch6.replace("## 01\n\n", "## 01\n\n" + ch6_choice + "\n\n", 1)
        ch6 = append_section(ch6, "badend-ch6-340", ch6_section)
        write_if_changed(path, ch6, changed)

    kuro = read(READING / "18_kuro.md")
    kuro = add_choice_link(
        kuro,
        "> 選択：拒絶する",
        "badend-kuro-choice",
        "> 飛ぶ：[黒の章-終](#badend-kuro-377)（選択「受け入れる」）",
    )
    kuro_section = f"""<!-- anchor: badend-kuro-377 -->
## 黒の章-終

> 進入条件：黒の章 22 で「受け入れる」を選択。

### 終

{kuro_377}

> 選択に戻る：[黒の章 22](#badend-kuro-choice)"""
    kuro = insert_section_before(kuro, "> 飛ぶ：[蒼の章](reading_order_19_ao.xhtml)", "badend-kuro-377", kuro_section)
    write_if_changed(READING / "18_kuro.md", kuro, changed)

    ao = read(READING / "19_ao.md")
    ao = add_choice_link(
        ao,
        "> 選択：はい",
        "badend-ao-034-choice",
        "> 飛ぶ：[蒼の章-終](#badend-ao-415)（選択「いいえ」）",
        context="蒼: 「お前は私を畏れているのか？」",
    )
    ao = add_choice_link(
        ao,
        "> 選択：約束出来る",
        "badend-ao-047-choice",
        "> 飛ぶ：[蒼の章-終（約束出来ない）](#badend-ao-047-local)（選択「約束出来ない」）",
        context="遠野 十夜: 「それが約束出来るなら全て話そう」",
    )
    ao_415_section = f"""<!-- anchor: badend-ao-415 -->
## 蒼の章-終

> 進入条件：蒼の章 34 で「いいえ」を選択。

### 終

{ao_415}

> 選択に戻る：[蒼の章 34](#badend-ao-034-choice)"""
    ao_047_section = f"""<!-- anchor: badend-ao-047-local -->
## 蒼の章-終（約束出来ない）

> 進入条件：蒼の章 47 で「約束出来ない」を選択。

### 終

{AO_CANNOT_PROMISE}

> 選択に戻る：[蒼の章 47](#badend-ao-047-choice)"""
    ao = insert_section_before(ao, "> 続けて読む：[あとがき](reading_order_20_atogaki.xhtml)", "badend-ao-415", ao_415_section)
    ao = insert_section_before(ao, "> 続けて読む：[あとがき](reading_order_20_atogaki.xhtml)", "badend-ao-047-local", ao_047_section)
    write_if_changed(READING / "19_ao.md", ao, changed)

    appendix = read(APPENDIX)
    appendix = remove_heading_block(appendix, "### 053. 一章-結末２", "### 056. 二章-02")
    bad_start = appendix.find("## Bad End / 终局分支")
    if bad_start >= 0:
        appendix = appendix[:bad_start].rstrip() + "\n"
    write_if_changed(APPENDIX, appendix, changed)
    return changed


def build_epub_source_files() -> list[str]:
    zh_manifest = json.loads((ROOT / "bookish_zhcn" / "manifest.json").read_text(encoding="utf-8"))
    return list(zh_manifest["epub"]["source_files"])


def write_manifest(
    data: dict[str, Any],
    entries: list[dict[str, Any]],
    route_plan: dict[str, Any],
    chapter_files: list[str],
    reading_order_files: list[str],
    appendix_files: list[str],
    divider_files: list[str],
    epub_outputs: dict[str, Any],
    heading_changes: dict[str, int],
    integrated_changes: list[str],
) -> None:
    manifest = {
        "source": data["meta"]["source"],
        "sha256": data["meta"]["sha256"],
        "scene_count": len(entries),
        "structure_synced_from": "bookish_zhcn",
        "structure_constraints": STRUCTURE_DOC,
        "protagonist": {
            "speaker": arc.PROTAGONIST_FULL_NAME,
            "placeholder_value": arc.PROTAGONIST_NAME,
        },
        "source_files": {
            "scenes_default_json": "_source/scenes_default.json",
            "archive_order_default_md": "_source/archive_order_default.md",
            "route_plan_json": "route_plan.json",
            "appendix_internal_stories_md": arc.BOOKISH_INTERNAL_STORIES_FILE,
            "appendix_endings_and_recovery_md": arc.BOOKISH_ENDINGS_AND_RECOVERY_FILE,
            "complete_epub_markdown": "complete_epub.md",
            "reading_order_dir": arc.BOOKISH_READING_ORDER_DIRNAME,
        },
        "epub": epub_outputs,
        "ladder_status": "structure_synced_reference",
        "file_structure": "zhcn_reviewed_reading_order",
        "chapter_files": arc.chapter_file_specs_for_manifest(),
        "generated_chapter_files": chapter_files,
        "reading_order_files": reading_order_files,
        "appendix_files": appendix_files,
        "divider_files": divider_files,
        "frontmatter_files": FRONTMATTER,
        "sync": {
            "scene_heading_files_changed": heading_changes,
            "integrated_ending_files_changed": integrated_changes,
            "bad_end_policy": "bad/end blocks moved into reading_order with entry condition and return links",
        },
    }
    write_text(BOOKISH / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))


def main() -> int:
    source_dir = BOOKISH / "_source"
    source_dir.mkdir(parents=True, exist_ok=True)

    data = arc.build_outputs()
    entries = arc.build_bookish_scene_entries(data)
    route_plan = arc.build_bookish_route_plan(data)
    chapter_files = arc.write_bookish_chapter_files(data, route_plan, BOOKISH)
    appendix_files = arc.write_bookish_appendix_files(data, route_plan, BOOKISH)
    reading_order_files = arc.write_bookish_reading_order_files(data, route_plan, BOOKISH)
    frontmatter_files = write_frontmatter()
    divider_files = write_dividers()

    apply_navigation(reading_order_files)
    heading_changes = normalize_scene_headings(data, route_plan)
    integrated_changes = integrate_endings()

    arc.write_json(source_dir / "scenes_default.json", entries)
    arc.write_bookish_archive_order(source_dir / "archive_order_default.md", entries)
    arc.write_json(BOOKISH / "route_plan.json", route_plan)
    arc.write_bookish_readme(BOOKISH / "README.md", data, entries, route_plan, appendix_files)

    epub_source_files = build_epub_source_files()
    non_frontmatter = [item for item in epub_source_files if item not in frontmatter_files]
    epub_outputs = arc.write_bookish_epub(
        data,
        non_frontmatter,
        base_dir=BOOKISH,
        epub_dir=BOOKISH / "epub",
        epub_file=BOOKISH / "bookish_complete.epub",
        complete_markdown=BOOKISH / "complete_epub.md",
        title=JA_TITLE,
        language=arc.BOOKISH_EPUB_LANGUAGE,
        author=JA_AUTHOR,
        identifier_suffix="shinigami-to-shoujo-ja-structure-reference",
        frontmatter_files=frontmatter_files,
        toc_titles=JA_TOC_TITLES,
    )
    write_manifest(
        data,
        entries,
        route_plan,
        chapter_files,
        reading_order_files,
        appendix_files,
        divider_files,
        epub_outputs,
        heading_changes,
        integrated_changes,
    )

    print(f"Synced Japanese bookish structure: {len(epub_source_files)} EPUB source files")
    print(f"Scene-heading files changed: {len(heading_changes)}")
    print(f"Integrated ending files changed: {len(integrated_changes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

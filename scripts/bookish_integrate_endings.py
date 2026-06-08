#!/usr/bin/env python3
"""Move selected zh-CN ending branches from appendix into reading flow."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from branch_explore_arc import parse_arc as arc  # noqa: E402


BOOKISH = ROOT / "bookish_zhcn"
READING = BOOKISH / "reading_order"
APPENDIX = BOOKISH / "appendix" / "endings_and_recovery.md"


HINASE_NO_MORE_LIES = """远野纱夜: 「请不要再说谎了」
日生光: 「为什么？」
远野纱夜: 「为什么……因为被人说谎会很难过」
远野纱夜: 「谎言一定会伤害某个人。就连你自己也……」
日生光: 「我可是被谎言拯救了」
远野纱夜: 「啊…………」
那时，他讲过的故事浮现在脑海。
关于爱说谎的少年的故事。
如果他是骗子，也许那个故事本身也是谎言。
一旦说了一个谎，就需要另一个谎来圆它，谎言会越来越多。
一旦开始怀疑，就没完没了。
因为就连现在的话，我也已经无法相信了。
一滴水从我眼中溢了出来。
然后又一滴。
又一滴。
远野纱夜: 「…………」
远野纱夜: 「……可以只回答我一个问题吗？」
日生光: 「可以」
远野纱夜: 「你爱我吗？」
他毫无迟疑地说道。
日生光: 「爱你」
远野纱夜: 「骗子」
听到我的话，他笑了。
随后，他再也没有出现在我面前。
远野纱夜: 「再见，虚假的王子」"""


AO_CANNOT_PROMISE = """远野纱夜: 「不能约定」
远野十夜: 「纱夜……」
远野纱夜: 「不能约定。那种事我做不到。因为我想待在哥哥身边」
远野十夜: 「纱夜。可是，那样……！」
我转过身，真挚地望着哥哥。
远野纱夜: 「……呐，十夜哥哥。我果然很快就会死了吧？」
远野十夜: 「……没有那回事」
远野纱夜: 「骗人。因为哥哥说了，『总比你就这样痛苦地死去要好』」
远野十夜: 「！那是……！」
哥哥痛苦地扭曲了脸。我把手贴上他的脸颊，慢慢向下滑去。
远野纱夜: 「反正都要死的话，我想死在哥哥身边……」
手来到哥哥胸前，我顺势把头靠了上去。
他没有立刻抱住我，但不久，哥哥将手臂绕到我背后，像要把我按进怀里一样抱紧了我。
远野十夜: 「苍也可以吗？」
他在我耳边低语。我眯起眼睛，隔了一会儿才说道。
远野纱夜: 「……嗯」
远野纱夜: 就在她这样回答的下一瞬间，少女遭遇了至今为止最剧烈的痛苦。
远野纱夜: 少女一边挣扎痛苦，一边回顾至今为止的一切。
远野纱夜: 少女踏上了旅途。
远野纱夜: 一直、一直走在漫长的旅途上。
远野纱夜: 但是，那也到此为止了。
远野纱夜: 少女的旅途，在还不知道世界上最美丽的话语是什么之前便结束了。
远野纱夜: 明明只差一点，就能找到那究竟是什么了。
远野纱夜: 随后，少女就那样缓缓合上了书。"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_if_changed(path: Path, text: str, changed: list[str]) -> None:
    text = text.rstrip() + "\n"
    if path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))


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
    sep = "\n---\n\n"
    remove_start = start
    if text[max(0, start - len(sep)) : start] == sep:
        remove_start = start - len(sep)
    before = text[:remove_start].rstrip()
    after = text[end:].lstrip()
    if not after:
        return before + "\n"
    return f"{before}\n\n---\n\n{after}"


def add_choice_link(
    text: str,
    choice_line: str,
    anchor: str,
    nav_line: str,
    *,
    context: str | None = None,
) -> str:
    search_from = text.index(context) if context else 0
    choice_at = text.index(choice_line, search_from)
    if f"<!-- anchor: {anchor} -->" not in text:
        text = text[:choice_at] + f"<!-- anchor: {anchor} -->\n\n" + text[choice_at:]
        choice_at += len(f"<!-- anchor: {anchor} -->\n\n")
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


def refresh_complete_markdown() -> None:
    manifest = json.loads((BOOKISH / "manifest.json").read_text(encoding="utf-8"))
    frontmatter = manifest["epub"].get("frontmatter_files", [])
    source_files = [item for item in manifest["epub"]["source_files"] if item not in frontmatter]
    arc.write_bookish_complete_markdown(
        BOOKISH,
        [*frontmatter, *source_files],
        BOOKISH / "complete_epub.md",
        arc.BOOKISH_ZHCN_EPUB_TITLE,
    )


def sanitize_integrated_endings(text: str) -> str:
    replacements = {
        "这双臂弯的温暖，钟塔的时间": "这双臂弯的温暖，时钟塔的时间",
        "那位少女的美貌，简直就如同\n真正的公主一样让人认错。": "那位少女美丽得简直让人\n几乎要误以为她是真正的公主。",
        "少女: 「死神』。」\n": "",
        "少女: 「少女的故事将不会再被续写下去」": "少女: 「少女的物语将不会再被续写下去」",
    }
    for before, after in replacements.items():
        text = text.replace(before, after)
    text = text.replace("。」", "」")
    return text


def main() -> int:
    changed: list[str] = []
    appendix = read(APPENDIX)
    ch1_054 = extract_heading_block(appendix, "### 054. 终", "### 227. 终1")
    hinase_227 = extract_heading_block(appendix, "### 227. 终1", "### 228. 终2")
    hinase_228 = extract_heading_block(appendix, "### 228. 终2", "### 340. 终")
    ch6_340 = extract_heading_block(appendix, "### 340. 终", "### 377. 终")
    kuro_377 = extract_heading_block(appendix, "### 377. 终", "### 415. 终")
    ao_415 = extract_heading_block(appendix, "### 415. 终", None)
    required = {
        "一章-终": ch1_054,
        "日生-终1": hinase_227,
        "日生-终2": hinase_228,
        "六章-终": ch6_340,
        "黑之章-终": kuro_377,
        "苍之章-终": ao_415,
    }
    missing = [name for name, body in required.items() if not body]
    if missing:
        existing_targets = [
            (READING / "02_chapter1.md", "badend-ch1-054"),
            (READING / "08_hinase.md", "badend-hinase-227"),
            (READING / "17_chapter6.md", "badend-ch6-340"),
            (READING / "18_kuro.md", "badend-kuro-377"),
            (READING / "19_ao.md", "badend-ao-415"),
        ]
        if not all(f"<!-- anchor: {anchor} -->" in read(path) for path, anchor in existing_targets):
            raise RuntimeError(f"Missing appendix blocks: {', '.join(missing)}")

    if ch1_054:
        ch1 = read(READING / "02_chapter1.md")
        ch1 = add_choice_link(
            ch1,
            "> 选择：答应",
            "badend-ch1-016-choice",
            "> 跳至：[一章-终](#badend-ch1-054)（选择「不答应」）",
        )
        ch1 = add_choice_link(
            ch1,
            "> 选择：把情况告诉哥哥",
            "badend-ch1-034-choice",
            "> 跳至：[一章-终](#badend-ch1-054)（选择「不告诉哥哥」）",
        )
        ch1_section = f"""<!-- anchor: badend-ch1-054 -->
## 一章-终

> 进入条件：一章 16-1 选择「不答应」，或一章 34 选择「不告诉哥哥」。

### 终

{ch1_054}

> 返回选择：[一章 16-1](#badend-ch1-016-choice) / [一章 34](#badend-ch1-034-choice)"""
        ch1 = insert_section_before(ch1, "> 继续阅读：[二章](reading_order_03_chapter2.xhtml)", "badend-ch1-054", ch1_section)
        ch1 = sanitize_integrated_endings(ch1)
        write_if_changed(READING / "02_chapter1.md", ch1, changed)

    if hinase_227 and hinase_228:
        hinase = read(READING / "08_hinase.md")
        hinase = add_choice_link(
            hinase,
            "> 选择：说谎",
            "badend-hinase-034-choice",
            "> 跳至：[日生-终](#badend-hinase-227)（选择「不要再说谎」）",
        )
        hinase_section = f"""<!-- anchor: badend-hinase-227 -->
## 日生-终

> 进入条件：日生 34 选择「不要再说谎」。

### 不要再说谎

{HINASE_NO_MORE_LIES}

### 终1

{hinase_227}

### 终2

{hinase_228}

> 返回选择：[日生 34](#badend-hinase-034-choice)"""
        hinase = insert_section_before(hinase, "> 返回主线：[四章后半](reading_order_09_chapter4_after_hinase_branch.xhtml)", "badend-hinase-227", hinase_section)
        write_if_changed(READING / "08_hinase.md", hinase, changed)

    if ch6_340:
        ch6_choice = """<!-- anchor: badend-ch6-choice -->

> 选择：抗争命运
> 跳至：[六章-终](#badend-ch6-340)（选择「放弃」）"""
        ch6_section = f"""<!-- anchor: badend-ch6-340 -->
## 六章-终

> 进入条件：六章 01 选择「放弃」。

### 终

{ch6_340}

> 返回选择：[六章 01](#badend-ch6-choice)"""
        for path in [BOOKISH / "11_chapter6.md", READING / "17_chapter6.md"]:
            ch6 = read(path)
            if "badend-ch6-choice" not in ch6:
                ch6 = ch6.replace("## 01\n\n", "## 01\n\n" + ch6_choice + "\n\n", 1)
            if path.name == "17_chapter6.md":
                ch6 = ch6.replace(
                    "> 继续阅读：[黑之章](reading_order_18_kuro.xhtml)",
                    "> 进入黑之章：[黑之章](reading_order_18_kuro.xhtml)（远野十夜/黑之章后续）\n"
                    "> 进入苍之章：[苍之章](reading_order_19_ao.xhtml)（苍线后续）",
                    1,
                )
                ch6 = insert_section_before(
                    ch6,
                    "> 进入黑之章：[黑之章](reading_order_18_kuro.xhtml)（远野十夜/黑之章后续）",
                    "badend-ch6-340",
                    ch6_section,
                )
            else:
                ch6 = append_section(ch6, "badend-ch6-340", ch6_section)
            ch6 = sanitize_integrated_endings(ch6)
            write_if_changed(path, ch6, changed)

    if kuro_377:
        kuro = read(READING / "18_kuro.md")
        kuro = add_choice_link(
            kuro,
            "> 选择：拒绝",
            "badend-kuro-choice",
            "> 跳至：[黑之章-终](#badend-kuro-377)（选择「接受」）",
        )
        kuro = kuro.replace(
            "> 继续阅读：[苍之章](reading_order_19_ao.xhtml)",
            "> 跳至：[苍之章](reading_order_19_ao.xhtml)",
            1,
        )
        kuro_section = f"""<!-- anchor: badend-kuro-377 -->
## 黑之章-终

> 进入条件：黑之章 22 选择「接受」。

### 终

{kuro_377}

> 返回选择：[黑之章 22](#badend-kuro-choice)"""
        kuro = insert_section_before(kuro, "> 跳至：[苍之章](reading_order_19_ao.xhtml)", "badend-kuro-377", kuro_section)
        write_if_changed(READING / "18_kuro.md", kuro, changed)

    if ao_415:
        ao = read(READING / "19_ao.md")
        ao = add_choice_link(
            ao,
            "> 选择：是的",
            "badend-ao-034-choice",
            "> 跳至：[苍之章-终](#badend-ao-415)（选择「不是」）",
            context="苍: 「你在害怕我吗？」",
        )
        ao = add_choice_link(
            ao,
            "> 选择：能约定",
            "badend-ao-047-choice",
            "> 跳至：[苍之章-终（不能约定）](#badend-ao-047-local)（选择「不能约定」）",
            context="远野十夜: 「如果能约定的话我就全部告诉你」",
        )
        ao_415_section = f"""<!-- anchor: badend-ao-415 -->
## 苍之章-终

> 进入条件：苍之章 34 选择「不是」。

### 终

{ao_415}

> 返回选择：[苍之章 34](#badend-ao-034-choice)"""
        ao_047_section = f"""<!-- anchor: badend-ao-047-local -->
## 苍之章-终（不能约定）

> 进入条件：苍之章 47 选择「不能约定」。

### 终

{AO_CANNOT_PROMISE}

> 返回选择：[苍之章 47](#badend-ao-047-choice)"""
        ao = insert_section_before(ao, "> 继续阅读：[后记](reading_order_20_atogaki.xhtml)", "badend-ao-415", ao_415_section)
        ao = insert_section_before(ao, "> 继续阅读：[后记](reading_order_20_atogaki.xhtml)", "badend-ao-047-local", ao_047_section)
        write_if_changed(READING / "19_ao.md", ao, changed)

    for path in [READING / "02_chapter1.md", BOOKISH / "11_chapter6.md", READING / "17_chapter6.md"]:
        text = sanitize_integrated_endings(read(path))
        write_if_changed(path, text, changed)

    appendix = read(APPENDIX)
    appendix = remove_heading_block(appendix, "### 053. 结末2", "### 056. 02")
    bad_start = appendix.find("## Bad End / 终局分支")
    if bad_start >= 0:
        appendix = appendix[:bad_start].rstrip() + "\n"
    write_if_changed(APPENDIX, appendix, changed)

    complete_before = read(BOOKISH / "complete_epub.md")
    refresh_complete_markdown()
    if read(BOOKISH / "complete_epub.md") != complete_before:
        changed.append("bookish_zhcn/complete_epub.md")

    for item in changed:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

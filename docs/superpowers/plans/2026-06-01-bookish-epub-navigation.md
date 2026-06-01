# Bookish EPUB Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add book-like EPUB navigation: a clickable in-book contents page, branch continuation links, divider pages, shortened reader-facing TOC entries, and less technical reader notes.

**Architecture:** Keep the canonical reading-order markdown files as the source of story content, then add a lightweight EPUB presentation layer in `branch_explore_arc/parse_arc.py`. The EPUB writer will support generated divider pages, hidden-from-TOC spine items, reader-facing TOC title aliases, and markdown links inside navigation blockquotes.

**Tech Stack:** Python stdlib, generated Markdown, generated XHTML/EPUB 3 files.

---

### Task 1: Add Link Rendering And Navigation Block Styling

**Files:**
- Modify: `branch_explore_arc/parse_arc.py`

- [ ] **Step 1: Write failing checks**

Run:

```bash
python3 - <<'PY'
from branch_explore_arc.parse_arc import markdown_inline_to_xhtml, markdown_to_epub_xhtml

html = markdown_inline_to_xhtml("[继续阅读：日生光线](reading_order_07_hinase_chapter4_branch.xhtml)")
assert '<a href="reading_order_07_hinase_chapter4_branch.xhtml">继续阅读：日生光线</a>' in html

xhtml = markdown_to_epub_xhtml("> 继续阅读：[日生光线](reading_order_07_hinase_chapter4_branch.xhtml)", "检查", "zh-CN")
assert '<blockquote class="navigation">' in xhtml
PY
```

Expected before implementation: assertion failure because links are escaped as plain text and navigation blockquotes are still generic notes.

- [ ] **Step 2: Implement**

Extend `markdown_inline_to_xhtml()` to recognize `[text](href)` and add `navigation` blockquote class for lines starting with `继续阅读：`, `返回主线：`, `跳至：`, or `也可跳至：`.

- [ ] **Step 3: Verify**

Run the command from Step 1 again. Expected: exit code `0`.

### Task 2: Add Reader-Facing Branch Links

**Files:**
- Modify: `branch_explore_arc/parse_arc.py`

- [ ] **Step 1: Write failing checks**

Run:

```bash
python3 - <<'PY'
from branch_explore_arc.parse_arc import bookish_navigation_lines

lines = bookish_navigation_lines("reading_order/06_chapter4_to_hinase_branch.md")
assert any("继续阅读：" in line and "日生光线" in line for line in lines)
assert any("跳至：" in line and "四章后半" in line for line in lines)
PY
```

Expected before implementation: import error or assertion failure because the helper does not exist.

- [ ] **Step 2: Implement**

Add a `BOOKISH_READER_NAVIGATION_LINKS` table keyed by reading-order source file. Add `bookish_navigation_lines(source_file)` that emits blockquote markdown lines using XHTML-relative hrefs.

- [ ] **Step 3: Attach Links**

Update `write_bookish_reading_order_files()` so generated/copy reading-order files append the configured navigation block at the end after translation/copying.

- [ ] **Step 4: Verify**

Run:

```bash
python3 - <<'PY'
from branch_explore_arc.parse_arc import bookish_navigation_lines
assert bookish_navigation_lines("reading_order/06_chapter4_to_hinase_branch.md")
assert bookish_navigation_lines("reading_order/08_hinase.md")
PY
```

### Task 3: Generate Divider Pages And Shortened EPUB TOC

**Files:**
- Modify: `branch_explore_arc/parse_arc.py`

- [ ] **Step 1: Write failing checks**

Run:

```bash
python3 - <<'PY'
from branch_explore_arc.parse_arc import build_zhcn_epub_source_files
sources, toc_titles = build_zhcn_epub_source_files(["reading_order/00_hajimari.md"], [])
assert any(item.startswith("dividers/") for item in sources)
assert toc_titles.get("reading_order/06_chapter4_to_hinase_branch.md") == "四章"
PY
```

Expected before implementation: import error or assertion failure because the helper does not exist.

- [ ] **Step 2: Implement**

Add a helper that creates a Chinese EPUB spine order with divider markdown files inserted before major sections and route branches. Return a `toc_titles` mapping that hides or aliases split files so reader-facing nav is concise.

- [ ] **Step 3: Modify EPUB Writer**

Allow `write_bookish_epub()` to receive `toc_titles` and skip divider files from EPUB nav/NCX. Add `body_class="divider-page"` for divider XHTML.

- [ ] **Step 4: Verify**

Run the Step 1 check again. Expected: exit code `0`.

### Task 4: Add In-Book Contents Page

**Files:**
- Modify: `branch_explore_arc/parse_arc.py`
- Generate: `bookish_zhcn/book_toc.md`

- [ ] **Step 1: Write failing checks**

Run:

```bash
python3 - <<'PY'
from branch_explore_arc.parse_arc import render_zhcn_book_toc
toc = "\n".join(render_zhcn_book_toc())
assert "# 目录" in toc
assert "[四章]" in toc
assert "chapter4_to_hinase_branch" not in toc
PY
```

Expected before implementation: import error or assertion failure because the helper does not exist.

- [ ] **Step 2: Implement**

Create `render_zhcn_book_toc()` and write `bookish_zhcn/book_toc.md`. Add it to `frontmatter_files` after `reader_manual.md`.

- [ ] **Step 3: Verify**

Run the Step 1 check again. Expected: exit code `0`.

### Task 5: Book-Like Notes

**Files:**
- Modify: `branch_explore_arc/parse_arc.py`

- [ ] **Step 1: Write failing checks**

Run:

```bash
python3 - <<'PY'
from branch_explore_arc.parse_arc import zhcn_reader_note
assert "appendix/" not in zhcn_reader_note("moved_to_appendix")
assert "bookish" not in zhcn_reader_note("empty_main_text").lower()
PY
```

Expected before implementation: import error or assertion failure because the helper does not exist.

- [ ] **Step 2: Implement**

Add `zhcn_reader_note(kind)` for the current technical notes and use it in chapter generation.

- [ ] **Step 3: Verify**

Run the Step 1 check again. Expected: exit code `0`.

### Task 6: Rebuild And Validate

**Files:**
- Regenerate: `bookish_zhcn/**`, `bookish_complete.zh.epub`, `bookish_zhcn/proofreading_report.md`

- [ ] **Step 1: Rebuild**

Run:

```bash
python3 branch_explore_arc/parse_arc.py
```

Expected: prints parsed section counts and finishes with `Bookish source written to: bookish`.

- [ ] **Step 2: Validate EPUB and generated text**

Run:

```bash
python3 - <<'PY'
import zipfile
from pathlib import Path

root = Path("/Users/chris/GitRepo/ProjectSTS")
with zipfile.ZipFile(root / "bookish_complete.zh.epub") as z:
    assert z.testzip() is None
    nav = z.read("OEBPS/nav.xhtml").decode("utf-8")
    assert "chapter4_to_hinase_branch" not in nav
    assert "四章" in nav and "日生光线" in nav
    assert "text/book_toc.xhtml" in z.namelist()
    toc = z.read("OEBPS/text/book_toc.xhtml").decode("utf-8")
    assert "继续阅读" not in toc

chapter = (root / "bookish_zhcn/reading_order/06_chapter4_to_hinase_branch.md").read_text(encoding="utf-8")
assert "继续阅读：" in chapter and "日生光线" in chapter
assert "appendix/endings_and_recovery.md" not in (root / "bookish_zhcn/complete_epub.md").read_text(encoding="utf-8")
PY
```

Expected: exit code `0`.

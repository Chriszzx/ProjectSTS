# Bookish Workspace

This directory is the staging area for the readable, book-like script.

## Current Scope

- Source ARC: `SCRDATA.ARC`
- SHA-256: `7244f1047d4f58f6960926d0c83b3d8397edfbafe9e3984ea073f26cd86ac680`
- Scenes available: 441
- Protagonist speaker: `遠野　紗夜`
- Name placeholder: `%s` -> `紗夜`
- Adjacent duplicate default-name format-text variants have been folded.
- Source `$...$` interactive word markers are stripped while keeping the marked word as plain text.
- Chapter files follow the original large-chapter count and order.
- Chapter-internal body order follows ascending ARC scene index; route labels are emitted inside that scene order.
- EPUB output uses `reading_order/`, which keeps the original chapter files as source/debug layers while arranging the ladder as branch side-stories that return to the main route.
- `00_hajimari.md` starts with the original `PRG_NAME.scr` default-name path, without displaying the name choices.
- The `はじまり` unlock conversation is noted but omitted from reader-facing body text.
- The route ladder is generated from `choices.txt`; bad/end branches are omitted from reader-facing chapters.
- Internal story scripts from the end of the extracted ARC text are generated as appendix files.
- `bookish_zhcn` mirrors this structure using `translated_processed_output_v2`.

## Files

- `DESIGN.md`: current bookish structure proposal and route-flow diagram.
- `_source/scenes_default.json`: structured scene bodies after default-name normalization.
- `_source/archive_order_default.md`: same cleaned bodies in archive order for inspection.
- `route_plan.json`: parsed walkthrough blocks and matched ARC choices.
- `manifest.json`: generation metadata and chapter file names.
- `reading_order/`: EPUB source layer ordered as main ladder, side route, return point.
- `appendix/internal_stories.md`: internal story texts separated from the main body.
- `appendix/endings_and_recovery.md`: walkthrough recovery, other endings, and bad/end scenes separated from the main body.
- `complete_epub.md`: complete EPUB-ready Markdown assembled from `reading_order/`.
- `epub/`: expanded EPUB source tree.
- `bookish_complete.epub`: packaged complete EPUB.

## Chapter Files

- `00_hajimari.md`
- `01_prologue.md`
- `02_chapter1.md`
- `03_chapter2.md`
- `04_chapter3.md`
- `05_natsuko.md`
- `06_chapter4.md`
- `07_hinase.md`
- `08_chapter5.md`
- `09_kirishima.md`
- `10_chiyo.md`
- `11_chapter6.md`
- `12_kuro.md`
- `13_ao.md`
- `14_atogaki.md`

## Appendix Files

- `appendix/internal_stories.md`
- `appendix/endings_and_recovery.md`

## Route Plan Summary

| Route | Parsed choices | Matched | Soft-skipped | Fallback menus | Unmatched planned choices |
|---|---:|---:|---:|---:|---:|
| 日生光 | 85 | 85 | 0 | 71 | 0 |
| 桐島七葵 | 102 | 102 | 0 | 54 | 0 |
| 千代 | 28 | 28 | 0 | 128 | 0 |
| 遠野十夜 | 99 | 98 | 1 | 58 | 0 |
| 六章-終 | 6 | 3 | 3 | 153 | 0 |
| 蒼 | 100 | 100 | 0 | 56 | 0 |
| 一章-結末２ | 22 | 22 | 0 | 134 | 0 |
| 夏帆-結末 | 21 | 21 | 0 | 135 | 0 |
| 日生25-2 | 48 | 48 | 0 | 108 | 0 |
| 四章37-2、六章03-1 | 95 | 93 | 2 | 63 | 0 |
| 蒼の章39-2 | 5 | 5 | 0 | 151 | 0 |

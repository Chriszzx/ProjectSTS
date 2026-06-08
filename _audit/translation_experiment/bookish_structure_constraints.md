# Bookish Structure Constraints

This document records the current zh-CN bookish structure used as the review
baseline before the next translation experiment. Generated files are excluded
from manual editing; the Markdown source files below are the editable source of
truth.

## Source Of Truth

- Editable zh-CN text lives in `bookish_zhcn/reading_order/*.md`,
  `bookish_zhcn/appendix/*.md`, `bookish_zhcn/book_toc.md`,
  `bookish_zhcn/reader_manual.md`, and `bookish_zhcn/dividers/*.md`.
- `bookish_zhcn/complete_epub.md`, `bookish_zhcn/epub/`, and the root EPUB are
  generated outputs. Do not hand-edit them.
- `bookish/` is a local Japanese reference tree and is ignored by git. It may be
  regenerated for comparison, but its large copyrighted text is not staged.

## EPUB Order

The zh-CN complete EPUB uses this 43-item source order:

1. `book_toc.md`
2. `reader_manual.md`
3. `dividers/00_story.md`
4. `reading_order/00_name.md`
5. `reading_order/00_hajimari_gate.md`
6. `reading_order/00_hajimari.md`
7. `dividers/01_prologue.md`
8. `reading_order/01_prologue.md`
9. `dividers/02_chapter1.md`
10. `reading_order/02_chapter1.md`
11. `dividers/03_chapter2.md`
12. `reading_order/03_chapter2.md`
13. `dividers/04_chapter3.md`
14. `reading_order/04_chapter3.md`
15. `dividers/05_natsuko.md`
16. `reading_order/05_natsuko.md`
17. `dividers/06_chapter4.md`
18. `reading_order/06_chapter4_to_hinase_branch.md`
19. `dividers/07_hinase.md`
20. `reading_order/07_hinase_chapter4_branch.md`
21. `reading_order/08_hinase.md`
22. `reading_order/09_chapter4_after_hinase_branch.md`
23. `dividers/08_chapter5.md`
24. `reading_order/10_chapter5_to_kirichiyo_branch.md`
25. `dividers/09_kirishima.md`
26. `reading_order/11_kirishima_chapter5_branch.md`
27. `reading_order/12_kirishima.md`
28. `dividers/10_chiyo.md`
29. `reading_order/13_chiyo_chapter5_branch.md`
30. `reading_order/14_chiyo_kirishima_branch.md`
31. `reading_order/15_chiyo.md`
32. `reading_order/16_chapter5_after_kirichiyo_branch.md`
33. `dividers/11_chapter6.md`
34. `reading_order/17_chapter6.md`
35. `dividers/12_kuro.md`
36. `reading_order/18_kuro.md`
37. `dividers/13_ao.md`
38. `reading_order/19_ao.md`
39. `dividers/14_atogaki.md`
40. `reading_order/20_atogaki.md`
41. `dividers/15_appendix.md`
42. `appendix/endings_and_recovery.md`
43. `appendix/internal_stories.md`

## Structural Rules

- The first two files are frontmatter: table of contents and reader manual.
- Divider files are one-heading section separators and precede major routes or
  appendices.
- Reading-order files are the primary review surface. Root chapter files are
  intermediate structured outputs and are not the preferred manual edit target.
- In body files, second-level scene headings use the original extracted scene
  marker, such as `## 01`, `## 15-1`, or `## 結末`, rather than route names.
- If one original scene contains route-specific variants, repeated scene markers
  are allowed. The marker identifies the source scene; the surrounding order and
  route navigation identify how to continue.
- Choice markers remain as blockquotes, e.g. `> 选择：...` / `> 選択：...`.
- Route and return links are blockquotes. Any normal content following a
  navigation block must start on a new EPUB page.
- Jump anchors use `<!-- anchor: ... -->`. Anchor names are stable review
  targets and should not be renamed casually.
- Bad/end sections embedded in the main flow begin with an entry-condition note
  and end with a return link to the source choice.
- 六章 keeps its 黑之章 / 苍之章 continuation links before the 六章 bad end block.
- `053` is merged into the existing 一章结末 content and is not retained as a
  duplicate appendix item. `苍之章39-2` remains appendix-only.

## Text-Level Constraints

- zh-CN dialogue should use Japanese-style brackets: primary `「」`, nested
  `『』`.
- For zh-CN dialogue, a final full stop inside `「...。」` is removed as
  `「...」`.
- Narration must remain narration. Speaker attribution should not be introduced
  merely because adjacent source lines share a character context.
- Translation alignment checks should compare line shape against the Japanese
  reference before applying automatic corrections.

## JA Structure Sync

Run `python3 scripts/bookish_sync_ja_structure.py` to rebuild the ignored
`bookish/` Japanese reference tree with the same structure, frontmatter,
divider order, scene-heading policy, route links, and integrated bad/end
placement used by `bookish_zhcn/`.

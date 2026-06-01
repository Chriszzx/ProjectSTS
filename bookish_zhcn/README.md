# Bookish zh-CN Workspace

这个目录是 `bookish` 的简体中文阅读版草稿。

## Current Scope

- Source ARC: `SCRDATA.ARC`
- SHA-256: `7244f1047d4f58f6960926d0c83b3d8397edfbafe9e3984ea073f26cd86ac680`
- Structure source: `bookish` scene-order ladder generated from `choices.txt`.
- Translation source: `bookish/bookish_complete.ja.zh.epub` is the authoritative JP/ZH source; `translated_processed_output_v2`, `processed_output_v2`, `Json/v0.1.0`, and `Modified/ja_zh` are fallbacks.
- Source `$...$` interactive word markers are stripped while keeping the marked word as plain text.
- EPUB output uses `reading_order/`, mirroring the Japanese main-ladder plus side-route return structure.
- `reader_manual.md` is inserted before the story body in the generated EPUB.
- `cover.jpg` is packaged as the generated EPUB cover image.
- `_audit/translation_alignment_audit.md` lists likely untranslated, structurally mismatched, or length-outlier lines.
- Translation source files loaded: 442
- Translation line pairs loaded: 44846
- Authoritative EPUB pairs loaded: 53017
- Missing translation hits are left as Japanese so they can be reviewed directly.

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

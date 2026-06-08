# Bookish zh-CN Workspace

这个目录是 `bookish` 的简体中文阅读版草稿。

## Current Scope

- Source ARC: `SCRDATA.ARC`
- SHA-256: `7244f1047d4f58f6960926d0c83b3d8397edfbafe9e3984ea073f26cd86ac680`
- Structure source: `bookish` scene-order ladder generated from `choices.txt`.
- Translation source: `bookish/bookish_complete.ja.zh.epub` is the default JP/ZH source used by the generator.
- Current Markdown has been reconciled against the read-only Apple Books reference package `死神与少女 Bookish 中文完整剧本.epub`.
- Apple Books reference package digest: `c4a4abd8a2e57efd60814b9d18354e64848b4b91d0de1cf4815661c69c289131` (53 files, 3659562 bytes).
- The Apple Books package is a reference only; it is not copied, moved, regenerated, or modified by this workspace.
- Root `bookish_complete.zh.epub` is the frozen EPUB reference packaged from this reviewed `bookish_zhcn` state.
- New zh-CN EPUB generation should write `bookish_zhcn.epub`, leaving `bookish_complete.zh.epub` as the reference.
- Legacy translation outputs are ignored by default; they are loaded only when `BookishTranslator(..., allow_legacy_fallbacks=True)` is used for debugging.
- Source `$...$` interactive word markers are stripped while keeping the marked word as plain text.
- EPUB output uses `reading_order/`, mirroring the Japanese main-ladder plus side-route return structure.
- `reader_manual.md` is inserted before the story body in the generated EPUB.
- `cover.jpg` is packaged as the generated EPUB cover image.
- `_audit/translation_alignment_audit.md` lists likely untranslated, structurally mismatched, or length-outlier lines.
- Legacy fallback loading: disabled
- Legacy source files loaded: 0
- Legacy line pairs loaded: 0
- Authoritative EPUB pairs loaded: 53017
- `reading_order/`, appendices, `reader_manual.md`, and ignored `complete_epub.md` are reconstructed from the Apple Books reference XHTML.
- Top-level chapter Markdown is rebuilt from matching Books reference blocks where the source structure is exact; chapter 4 and chapter 5 use context-scoped line mappings for branch material.
- Current audit after Apple Books reconciliation: 371 `speaker_shape_mismatch` findings, 0 `japanese_kana_in_translation`, 0 `unchanged_japanese_line`.

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

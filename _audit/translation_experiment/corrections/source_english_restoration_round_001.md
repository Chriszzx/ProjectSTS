# Source English Restoration Round 001

Scope: restore English/Latin-script tokens that are present in the Japanese source but had been translated or normalized into Chinese in `bookish_zhcn` chapter files and `reading_order` files.

Reference source searched:

- `bookish/_source/scenes_default.json`
- `processed_output_v3_1`
- `branch_explore_arc/script_annotated.md`

Applied corrections:

- Restored `Let's party` where source uses `Ｌｅｔ’ｓ　ｐａｒｔｙ`:
  - `bookish_zhcn/03_chapter2.md`
  - `bookish_zhcn/appendix/endings_and_recovery.md`
  - `bookish_zhcn/reading_order/03_chapter2.md`
- Restored `I Am a Cat` where source uses `Ｉ　Ａｍ　ａ　Ｃａｔ`:
  - `bookish_zhcn/04_chapter3.md`
  - `bookish_zhcn/reading_order/04_chapter3.md`
- Restored `OK` where source uses `ＯＫ`:
  - `bookish_zhcn/09_kirishima.md`
  - `bookish_zhcn/reading_order/12_kirishima.md`
  - `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md`
- Restored the chapter 3 English quotation block to complete English sentences, matching `processed_output_v3_1/chapter3/chapter3_38.txt:13-16`:
  - `bookish_zhcn/04_chapter3.md`
  - `bookish_zhcn/reading_order/04_chapter3.md`

Confirmed already preserved:

- `under the rose`
- `sub rose`
- `CLOSE`
- `DNA`
- `Let's Go`
- `LOVE`
- `Depth`
- `CHAPTER`

Rejected after review:

- `HR` and `OB` are present as abbreviations in the Japanese source, but in this context they should remain localized as `班会` and `毕业生`; the attempted restoration was reverted.

Not edited:

- `bookish_zhcn/complete_epub.md`, because it is treated as a generated/review artifact and should be refreshed only when explicitly requested.

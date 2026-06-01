# Name Normalization Check

This records the current default-name normalization checks used for the
bookish source layer and `script_annotated.md`.

## Rules

- Protagonist speaker: `PLAYER` -> `遠野　紗夜`
- Protagonist placeholder: `%s` -> `紗夜`
- Adjacent duplicate `%s` format-text variants are folded into one line.
- Natural repeated lines that are not name-placeholder variants are preserved.

## Aggregate Checks

- `bookish/_source/scenes_default.json` scenes: 441
- Body lines inspected: 43760
- Body lines starting with `PLAYER:`: 0
- Body lines containing `%s`: 0
- Consecutive exact duplicates remaining: 19
  - These are not automatically removed because sampled cases are ordinary
    repeated dramatic text such as `「…………」`, `違う。`, or repeated short
    narration fragments, not protagonist-name variants.

## Sensitive Examples

| Case | Expected Text | `script_annotated.md` | `bookish/_source/archive_order_default.md` |
|---|---|---:|---:|
| Main speaker rewrite | `遠野　紗夜: 「…………」` | line 25 | line 13 |
| Simple name call | `遠野 十夜: 「紗夜！」` | line 26 | line 14 |
| Leading subject insertion | `遠野 十夜: 「紗夜は俺の世界で一番大切な人だ。心配をするのは当たり前のことだろう」` | line 39 | line 27 |
| Punctuation before name | `遠野 十夜: 「……紗夜は夜が好きかい？」` | line 47 | line 35 |
| Mid-sentence particle gap | `遠野 十夜: 「で、紗夜に意見を聞こうと思って」` | line 267 | line 231 |
| Mid-sentence `が` gap | `遠野 十夜: 「そうだけど、多分紗夜が思っているようなものとは違うよ」` | line 273 | line 237 |
| Double `に` gap | `遠野 十夜: 「もちろん。出来上がったら一番初めに紗夜に見せるよ」` | line 493 | line 433 |
| Honorific gap | `？？？: 「あれ、紗夜ちゃんじゃないか。どうしたのかな？」` | line 1616 | line 1440 |

## Current Output Files

- `branch_explore_arc/script_annotated.md`
- `bookish/_source/scenes_default.json`
- `bookish/_source/archive_order_default.md`

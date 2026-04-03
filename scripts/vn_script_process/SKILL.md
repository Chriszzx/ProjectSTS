---
name: vn-script-process
description: Preprocess raw ProjectSTS / Shinigami to Shoujo visual novel script dumps before translation. Use this whenever the user wants to clean OG.txt or OG/split_output/*.txt into translation-ready scene files, map split files into chapter/route directories, normalize protagonist placeholder handling, rewrite unnamed protagonist dialogue with the canonical full speaker name `遠野　紗夜`, or separate common/route outputs by split order instead of the legacy pipeline. Prefer this skill over ad-hoc manual cleanup whenever the request involves raw VN script restructuring, namespace merge, duplicate NAME-placeholder repair, or dry-run generation of cleaned script files.
---

# VN Script Process

Use this skill to turn raw split script dumps into stable, translation-ready text files.

This skill is intentionally separate from translation. Its job is preprocessing only:
- remove engine/title noise
- merge name lines with dialogue lines
- preserve narration
- resolve protagonist placeholder behavior consistently
- rewrite unnamed protagonist dialogue as `遠野　紗夜「...」`
- map outputs into chapter/route directories by split number

## Files in this skill

- `process_script.py` — main processor
- `chapter_mapping.json` — sequential split-to-output mapping
- `special_character.txt` — character name list
- `SKILL.md` — this guide

## Repo-local location

Inside ProjectSTS, keep these files together under:
- `scripts/vn_script_process/`

Run commands from the repo root.

## Project assumptions

Current ProjectSTS layout:
- raw full dump: `OG/OG.txt`
- raw split files: `OG/split_output/*.txt`
- old legacy outputs: `OG/combined_output/*.txt`
- manual examples: some files under `OG/prologue/` and early `OG/chapter1/`

Treat `OG/split_output/*.txt` as the authoritative processing input.
Do **not** assume existing chapter folders are complete generated outputs.
Do **not** reuse the legacy `combination.py` behavior blindly.

## Confirmed processing rules

These are the important user-approved rules.

### 1) Unnamed protagonist dialogue uses `遠野　紗夜`

Rewrite unnamed protagonist dialogue to the protagonist's canonical full Japanese speaker name.

Example:
- raw: `「……」`
- output: `遠野　紗夜「……」`

Do **not** use the old `so` marker in new output.

### 2) Protagonist placeholder resolves to `紗夜`

When the game dump clearly omitted the protagonist name from dialogue variants, insert:
- `紗夜`

Do **not** expand it to `遠野　紗夜`.

### 3) Side routes stay in separate directories

Output is split by sequential mapping, including side-route folders such as:
- `natsuko/`
- `hinase/`
- `kirishima/`
- `chiyo/`
- `chapter7_kuro/`
- `chapter7_ao/`

Do **not** force everything into the old chapter-only structure.

### 4) Output mapping is one-to-one by split order

Each `split_output_N.txt` maps to exactly one destination file from `chapter_mapping.json`.

### 5) Choice branches use `###`

For consecutive choice lines written as `『...』`:
- keep the first line unchanged
- prefix later consecutive options with `###`

## Processing behavior

`process_script.py` currently runs this pipeline:

1. Remove title lines such as `シナリオタイトル...`
2. Merge namespace lines:
   - character-name line + following dialogue line -> one line
3. Join multiline dialogue safely
4. Merge duplicate NAME-placeholder variants
5. Resolve standalone name-call remnants like `蒼` -> `蒼「紗夜」` when appropriate
6. Mark unnamed dialogue with `遠野　紗夜`
7. Mark alternate choice lines with `###`
8. Clean and write output

## Important heuristic rule

Be conservative about inserting `紗夜`.

Only insert the protagonist name when the split strongly indicates a missing NAME placeholder. Typical good cases:
- `……` + `は夜が好きかい？`
- `で、` + `に意見を聞こうと思って`
- `多分` + `が思っているような`
- `一番初めに` + `に見せるよ`
- `あれ、` + `ちゃんじゃないか`

Do **not** insert `紗夜` for ordinary line-wrap continuations just because the next line starts with a particle.

Bad false-positive example:
- raw:
  - `「今度の物語は、`
  - `死神`
  - `を主人公にしようと思ってるんだ」`
- correct output:
  - `今度の物語は、死神を主人公にしようと思ってるんだ`
- incorrect output:
  - `今度の物語は、死神紗夜を主人公にしようと思ってるんだ`

If a change risks reintroducing this false positive, stop and re-test before continuing.

## Command patterns

### Process one file to stdout

```bash
python3 scripts/vn_script_process/process_script.py \
  -i OG/split_output/split_output_10.txt \
  -c scripts/vn_script_process/special_character.txt
```

### Process one file to an output file

```bash
python3 scripts/vn_script_process/process_script.py \
  -i OG/split_output/split_output_10.txt \
  -c scripts/vn_script_process/special_character.txt \
  -o /tmp/test_output.txt
```

### Dry-run a split range with mapping

```bash
python3 scripts/vn_script_process/process_script.py \
  -i OG/split_output \
  -o /tmp/projectsts-dryrun \
  -c scripts/vn_script_process/special_character.txt \
  -m scripts/vn_script_process/chapter_mapping.json \
  -r 1-20 \
  --dry-run
```

### Generate cleaned files into a separate directory

```bash
python3 scripts/vn_script_process/process_script.py \
  -i OG/split_output \
  -o processed_output_v2 \
  -c scripts/vn_script_process/special_character.txt \
  -m scripts/vn_script_process/chapter_mapping.json \
  -r 1-20
```

Prefer writing to a separate test output directory first. Do not overwrite user content blindly.

## Required validation after edits

After changing `process_script.py`, re-test at least:
- `OG/split_output/split_output_2.txt`
- `OG/split_output/split_output_4.txt`
- `OG/split_output/split_output_10.txt`

Verify these outputs still hold:
- `遠野　十夜「紗夜は俺の世界で一番大切な人だ。心配をするのは当たり前のことだろう」`
- `遠野　十夜「……紗夜は夜が好きかい？」`
- `遠野　十夜「で、紗夜に意見を聞こうと思って」`
- `遠野　十夜「そうだけど、多分紗夜が思っているようなものとは違うよ」`
- `遠野　十夜「もちろん。出来上がったら一番初めに紗夜に見せるよ」`
- `蒼「紗夜」`
- `？？？「あれ、紗夜ちゃんじゃないか。どうしたのかな？」`
- `今度の物語は、死神を主人公にしようと思ってるんだ`

Also verify:
- no leftover duplicate pair artifacts
- no leftover `so` markers in newly generated output
- no internal join markers leaked into output

## When responding to the user

Be explicit about:
- which split files or ranges were processed
- where output was written
- whether it was a dry run or real write
- which heuristic-sensitive cases were checked

If verification fails, describe the exact bad line and stop to fix it before claiming completion.

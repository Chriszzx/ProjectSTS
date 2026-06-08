# Parallel Translation Review Spec

Version: `parallel-translation-review/v0.1`

This specification defines an extensible format for comparing Japanese source,
the current authoritative zh-CN translation, and one optimized zh-CN candidate
from an LLM or human translation pass.

The format is intentionally conservative: experiment files are review material,
not generation input. Accepted blocks must still be applied to `bookish_zhcn` in
a separate reviewed change.

## Goals

- Compare different LLM translation experiments on identical source/current
  blocks.
- Preserve enough provenance to reproduce or explain each candidate.
- Keep human review readable in Markdown while keeping machine-readable JSONL.
- Make acceptance explicit so experiments cannot silently overwrite
  `bookish_zhcn`.

## Non-Goals

- This spec does not define final EPUB generation.
- This spec does not make any LLM output authoritative by itself.
- This spec does not require every model to use the same prompt, only that the
  prompt and model details are recorded.

## Directory Layout

Canonical layout:

```text
_audit/translation_experiment/parallel/
  SPEC.md
  README.md
  schemas/
    review_block.schema.json
    run_manifest.schema.json
  templates/
    review_block.json
    run_manifest.json
  runs/
    <run_id>/
      manifest.json
  <review_set>.<candidate_id>.md
  <review_set>.<candidate_id>.jsonl
```

The current pilot keeps `prologue.md` and `prologue.jsonl` at the folder root.
That is allowed for early experiments; new multi-model experiments should prefer
the `<review_set>.<candidate_id>` naming convention.

## Naming

- `review_set_id`: stable source slice, for example
  `ro01-prologue-opening`.
- `candidate_id`: one model/prompt pass, for example
  `dsv4-pro-third-draft`.
- `run_id`: usually `<review_set_id>--<candidate_id>`.
- `block id`: stable unit id inside one review set, for example
  `ro01-prologue-0006`.

Block ids must stay stable across candidates for the same review set. This is
what lets us compare multiple LLMs line by line.

## Run Manifest

Every serious LLM experiment should have:

```text
runs/<run_id>/manifest.json
```

The manifest records:

- schema version
- source/current files
- human view file
- JSONL data file
- model identity
- prompt identity or prompt file
- decoding parameters when known
- reviewer notes

If a detail is unknown, use `null`, not a guessed value.

## Review Block JSONL

Each JSONL line is one review block. Required fields:

- `id`
- `source_file`
- `current_file`
- `draft_source`
- `status`
- `ja`
- `current_zh`
- `draft_zh`
- `note`

Allowed `status` values:

- `candidate`: proposed, not accepted
- `accepted`: approved for later backfill
- `rejected`: reviewed and not accepted
- `needs_review`: cannot decide without more review

Optional extension fields:

- `schema_version`
- `review_set_id`
- `candidate_id`
- `run_id`
- `unit_index`
- `segment_kind`
- `speaker`
- `route_context`
- `tags`
- `scores`
- `reviewer`
- `review_note`

Tools must preserve unknown fields when rewriting JSONL.

## Markdown View

Markdown is the human review surface. It should mirror JSONL order.

Each block should use:

````md
## <block-id>

- status: `candidate`
- note: ...

```ja
...
```

```current_zh
...
```

```draft_zh
...
```
````

The fenced block names are part of the format. Do not rename `ja`,
`current_zh`, or `draft_zh`.

## Segmentation

Prefer semantic units:

- short narration paragraph
- dialogue beat
- repeated reading segment
- choice line plus immediate response

Do not split only to make a table look neat. If the original line break matters,
preserve it and mention the reason in `note`.

## Model Comparison

For comparing multiple LLMs:

1. Keep the same `review_set_id`.
2. Keep the same block ids and `ja/current_zh` text.
3. Create one `candidate_id` per model/prompt pass.
4. Store one JSONL and one Markdown view per candidate.
5. Compare by block id, not by line number.

Example:

```text
prologue-opening.dsv4-pro-third-draft.md
prologue-opening.dsv4-pro-third-draft.jsonl
prologue-opening.gpt5-literary-pass.md
prologue-opening.gpt5-literary-pass.jsonl
runs/ro01-prologue-opening--dsv4-pro-third-draft/manifest.json
runs/ro01-prologue-opening--gpt5-literary-pass/manifest.json
```

## Acceptance Policy

`accepted` means only this:

- the candidate block may be considered for a later backfill patch

It does not mean the block has already changed `bookish_zhcn`.

Backfill requirements:

- only apply `accepted` blocks
- show a targeted diff against `bookish_zhcn`
- preserve source alignment unless the review note explicitly approves a line
  break change
- regenerate or compare EPUB only after the backfill patch is reviewed

## Extension Rules

- Add new optional fields instead of changing required field meanings.
- Increment this spec version for breaking changes.
- Keep field names in snake_case.
- Keep status values small and stable.
- Use UTF-8.
- Use JSONL for data and Markdown for review; do not invent model-specific
  formats.

# Parallel Translation Review

This folder holds translation experiment material only. It is not an input to
`bookish_zhcn` EPUB generation unless an entry is explicitly accepted and later
applied by a separate reviewed step.

The extensible protocol is defined in `SPEC.md`. New LLM experiments should add
a run manifest under `runs/<run_id>/manifest.json` and write review blocks that
match `schemas/review_block.schema.json`.

## File Roles

- `*.md`: human review view. Each block places Japanese source, current zh-CN,
  and draft zh-CN next to one another in a stable unit.
- `*.jsonl`: machine-readable mirror of the same review blocks. One JSON object
  per line.
- `runs/<run_id>/manifest.json`: model, prompt, decoding, source, and file
  metadata for one LLM experiment.
- `schemas/`: JSON Schema files for validation.
- `templates/`: copyable starting points for new experiments.

## Review Block Schema

Each block has:

- `id`: stable review unit id, usually `roNN-section-####`.
- `source_file`: Japanese source Markdown path.
- `current_file`: current authoritative zh-CN Markdown path.
- `draft_source`: experiment file or agent pass that produced the draft.
- `status`: one of `candidate`, `accepted`, `rejected`, `needs_review`.
- `ja`: Japanese source text.
- `current_zh`: current `bookish_zhcn` text.
- `draft_zh`: proposed optimized translation.
- `note`: short reason, risk, or review instruction.

## Policy

- Default status is `candidate`; it does not change `bookish_zhcn`.
- Only `accepted` blocks may be backfilled into `bookish_zhcn`, and that should
  happen in a separate change with a targeted diff.
- Keep source and current translation verbatim enough to audit alignment.
- Prefer review blocks that follow semantic paragraphs or dialogue beats, not
  arbitrary single lines, unless line-level structure matters.
- If a draft intentionally changes line breaks, record that in `note`.

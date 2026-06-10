# zhcn residual cleanup round 002

Date: 2026-06-09

Scope:
- Editable Chinese markdown under `bookish_zhcn/`, including top-level chapters, `reading_order/`, and `appendix/`.
- Excluded generated/reference output: `bookish_zhcn/complete_epub.md`, `bookish_zhcn/epub/`, divider/doc/report files.
- `bookish_zhcn/00_hajimari.md` keeps the user-authored unlock-note structure, but its `時計塔` term follows the project rule and is normalized to `时钟塔`.

User constraints:
- Do not alter the self-edited `hajimari` unlock note.
- `時計塔` is normally translated with the same-length Chinese term `时钟塔`; this includes `hajimari` when the source word is `時計塔`.
- Do not alter `Depth（深层的言叶）`.
- For quote fixes, source bracket form has highest priority.

Applied:
- Normalized clocktower terminology to `时钟塔`.
- Replaced raw `本物` in the Hinase line with `真货`.
- Replaced remaining Japanese long vowel mark `ー` with `～` in Chinese dialogue.
- Converted closed Chinese curly single quotes to Japanese secondary quotes `『』`.
- Fixed line-local half secondary quotes where the original/source structure is a closed inner quote.
- Fixed AO route source-alignment errors:
  - Restored the magician's missing lines around `你自己不这么觉得吗？` and `可是，我并不害怕你`.
  - Replaced duplicated `男人的名字。` with `男人的名字。/死神。`.
- Rechecked the `十年前？/十年も前にこの本は書かれたというの？` source and revised the Chinese to:
  - `十年前？`
  - `这本书竟然在十年前就写成了？`

Post-scan:
- `时计塔|钟楼|(?<!时)钟塔`: 0
- `本物|偽物`: 0
- `ー`: 0
- `‘|’`: 0
- Old duplicated ten-years phrasing: 0
- Mixed `『《...》』`: 0
- Known AO stale magician lines: 0
- Remaining secondary quote half-lines: 29, all inspected as cross-line quote blocks in letters or embedded story text rather than line-local bracket corruption.
- Adjacent exact duplicates still exist in dream/monologue passages such as repeated `「…………」`, `想见你。`, and `好寂寞。`; these were spot-checked and treated as intentional rhythm/repetition rather than branch residue.

Verification:
- `git diff --check` passed.

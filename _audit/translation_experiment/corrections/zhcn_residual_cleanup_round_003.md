# zhcn residual cleanup round 003

Date: 2026-06-10

Scope:
- Editable Chinese markdown under `bookish_zhcn/`, including top-level chapters, `reading_order/`, and `appendix/`.
- Excluded generated/reference output: `bookish_zhcn/complete_epub.md`, `bookish_zhcn/epub/`, and audit/report files under `bookish_zhcn/_audit/`.
- `00_hajimari` unlock note remains user-authored and intentionally preserved.
- `Depth（深层的言叶）` remains intentionally preserved.

Applied:
- Unified title-like `ユメミルセカイ` occurrences to `梦见世界`.
  - See `title_yumemiru_sekai_round_001.md`.
  - Kept ordinary `夢見る世界` phrases as natural Chinese, e.g. `梦中的世界`.
- Cleaned remaining person-identity terms in the 日生真伪 axis:
  - `真品/赝品` -> `真货/冒牌货` or `正牌/冒牌的` by grammatical role.
  - `本尊` -> `本人`.
  - `假货` -> `冒牌货` or `冒牌的` by grammatical role.
  - 名词位残留 `正牌和冒牌` -> `真货和冒牌货`.
- Cleaned one non-日生 mother/double motif line:
  - `真正的母亲成了假的母亲，而假的母亲成了真正的母亲`.
- Converted remaining same-level nested dialogue quotes from inner `「...」` to secondary `『...』` when they occur inside an already-open dialogue line.
- Corrected the 日生告白 line pair from duplicated `我喜欢你 / 我喜欢你` to `我喜欢你 / 我喜欢的是你`, matching source `好きだよ / 君が好きだ`.

Post-scan:
- `时计塔|钟楼|(?<!时)钟塔`: 0
- `太宰巴|巴女士|巴小姐`: 0
- `本物|偽物`: 0
- `本尊|真品|赝品|假货|正牌和冒牌`: 0
- `言叶`, excluding preserved `Depth（深层的言叶）`: 0
- `ー`: 0
- `‘|’`: 0
- Mixed `『《...》』`: 0
- Old `ユメミルセカイ` title variants: 0
- Same-level nested dialogue quote `「...「...」...」`: 0
- Dialogue-final `。」`: 0
- Adjacent duplicate lines after excluding pure pause/ellipsis performance lines: 0

Known intentional remains:
- `00_hajimari` / `reading_order/00_hajimari_gate` unlock notes.
- `Depth（深层的言叶）`.
- Cross-line embedded-story quote blocks, where line-local bracket checks are not applicable.

Verification:
- `git diff --check` passed.

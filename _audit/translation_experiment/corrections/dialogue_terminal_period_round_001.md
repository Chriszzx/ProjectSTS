# Dialogue Terminal Period Round 001

Date: 2026-06-08

## Rule

删除中文对话引号 `「」` 内末尾的句号：

- before: `角色: 「台词。」`
- after: `角色: 「台词」`

问号、叹号、省略号等保留不动。

## Scope

应用到 `bookish_zhcn` 的正文/附录 Markdown 源文件：

- `bookish_zhcn/*.md`，排除 `complete_epub.md`
- `bookish_zhcn/reading_order/*.md`
- `bookish_zhcn/appendix/*.md`

不修改审计基准、测试基准输出和已生成的 `bookish_zhcn/epub/`。

## Result

- 当前 Markdown 源文件共清理 `11984` 个 `。」`。
- `bookish_zhcn/complete_epub.md` 已刷新。
- 同步了生成管线与修正规则脚本，避免后续重跑时重新带回旧格式。
- 顺手修正两处旧文本多余闭引号：
  - `心想「你明明知道」。」` -> `心想「你明明知道」`
  - `仿佛在说「今天我就陪你任性一整天」。」` -> `仿佛在说「今天我就陪你任性一整天」`

## Verification

- `python3 scripts/dialogue_terminal_period_apply.py --dry-run`
- `rg -n "。」" bookish_zhcn --glob '*.md' --glob '!bookish_zhcn/_audit/**' --glob '!bookish_zhcn/epub/**' --glob '!bookish_zhcn/complete_epub.md'`
- `rg -n "。」" bookish_zhcn/complete_epub.md`
- `python3 -m unittest tests.test_bookish_epub_generation tests.test_contextual_term_apply tests.test_honorific_guideline_apply tests.test_terminology_guideline_apply tests.test_translation_cleanup_audit`
- `git diff --check -- bookish_zhcn branch_explore_arc/parse_arc.py scripts tests`

# Endings Integration Round 001

Date: 2026-06-08

## Scope

将附录中的终局分支提升到 bookish zh-CN 主阅读流，保留人工可审查的进入条件与返回链接。

## Decisions

- `053. 结末2` 与正文已有的一章结末内容重复，本轮从附录删除，不再重复保留。
- `苍之章39-2` 按用户指示忽略，不提升到正文，继续留作附录观察项。
- `六章` 结尾不再只导向黑之章，而是同时给出黑之章与苍之章入口。
- `黑之章` 末尾到苍之章的链接改为“跳至”，避免误读为唯一线性续读。

## Integrated Branches

- 一章-终：从一章 16-1「不答应」与一章 34「不告诉哥哥」进入，结尾返回对应选择。
- 日生-终：从日生 34「不要再说谎」进入，合并终1/终2，结尾返回对应选择。
- 六章-终：在六章 01 补入「抗争命运 / 放弃」提示，从「放弃」进入，结尾返回六章 01。
- 黑之章-终：从黑之章 22「接受」进入，结尾返回对应选择。
- 苍之章-终：从苍之章 34「不是」进入，结尾返回对应选择。
- 苍之章-终（不能约定）：从苍之章 47「不能约定」进入，结尾返回对应选择。

## Text Fixes Inside Moved Blocks

- `钟塔的时间` -> `时钟塔的时间`
- 删除六章-终中误抽取的残句 `少女: 「死神』。」`
- `少女的故事将不会再被续写下去` -> `少女的物语将不会再被续写下去`

## Verification

- `python3 -m unittest tests.test_bookish_epub_generation`
- `python3 scripts/bookish_scene_heading_apply.py --dry-run`
- `python3 scripts/bookish_integrate_endings.py` rerun produced no additional changes after idempotence cleanup.

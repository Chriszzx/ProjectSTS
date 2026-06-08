# 敬语准则回填 checkpoint：honorific_guideline_round_001

> 记录时间：2026-06-05  
> 状态：暂停在“自动/半自动敬语修正工具收紧与 dry-run 评估”阶段。  

## 当前结论

- 本轮尚未把敬语工具应用到真实 `bookish_zhcn/reading_order/*.md`。
- 已按用户要求修正准则表：`臥待 → 纱夜 / 紗夜ちゃん` 固定译为“小纱夜”，与夏帆的“纱夜酱”分开。
- `scripts/honorific_guideline_apply.py` 已从危险的“非空行 zip 对齐”改为“说话人对白锚点 + 局部日文触发语确认”。
- `tests/test_honorific_guideline_apply.py` 已加入边界测试，当前单测通过：
  - 插入中文导航行后仍能靠说话人锚点改 `日生学长 -> 日生前辈`、`大小姐 -> 小姐`。
  - 夏帆的 `七葵先輩 / 七葵前辈` 不会被误改成“桐岛前辈”。
  - 光自己的“叫我光先生。不然，叫光前辈也行”不会被误改。
  - 千代的 `紗夜、さん？` / `纱夜、小姐？` 会改成 `纱夜？`。

## 已实现的自动规则

- `日生先輩`：`日生学长 -> 日生前辈`
- `桐島先輩`：`桐岛学长 -> 桐岛前辈`
- `光先輩`：仅在明确为 `光先輩` 且非元称呼句时，`光先生 -> 光前辈`
- 私下/恋人语境 `光さん`：`光先生 -> 光`，并处理 `光先生您 -> 光，你`
- 光的 `お嬢`：`大小姐 -> 小姐`
- 千代的 `お嬢さん`：`大小姐 -> 小姐`
- 纱夜/叙述的 `千代さん`：`千代先生/千代小姐 -> 千代`，并处理 `千代您 -> 千代，您`
- 千代的 `紗夜さん` / `紗夜、さん`：`纱夜小姐/纱夜、小姐 -> 纱夜`
- 卧待的 `紗夜ちゃん`：`纱夜酱 -> 小纱夜`

## dry-run 结果

在临时副本上运行当前工具，预计自动回填 839 条：

| rule_id | 数量 |
|---|---:|
| `chiyo-ojousan` | 82 |
| `chiyo-sayo-san` | 9 |
| `gashomachi-to-sayo-chan` | 3 |
| `hikari-ojo` | 121 |
| `hikari-san-private` | 62 |
| `hikari-senpai` | 27 |
| `hinase-senpai` | 80 |
| `sayo-to-chiyo-san` | 455 |

dry-run 后明显语病检查：

- `日生学长`: 0
- `千代小姐`: 0
- `桐岛学长`: 0
- `千代您`: 0
- `光您`: 0
- `叫我光前辈。不然，叫光前辈`: 0

## 未完成事项

1. 仍有 6 处 `千代先生` 残留在 dry-run 结果中，集中在 `04_chapter3.md` 的重复选择块，原因是这些块没有拿到精确对白锚点。
2. 下一步应实现一个更窄的兜底：
   - 只在“没有精确日文行”的情况下启用。
   - 按章节比例在较宽窗口内找同说话人/同触发语。
   - 如果已有精确日文行但日文是 `お嬢様` 或其他例外，不得兜底改写。
3. 兜底完成后，再跑临时副本 dry-run，确认残留和误伤。
4. 最后才运行真实 apply，生成：
   - `_audit/translation_experiment/corrections/honorific_guideline_round_001.md`
   - `_audit/translation_experiment/corrections/honorific_guideline_round_001.operations.jsonl`
   - `_audit/translation_experiment/corrections/honorific_guideline_round_001.alignment_warnings.jsonl`
5. 真实 apply 后运行完整测试：
   - `python3 -m unittest discover -s tests`

## 明天续作提醒

- 不要重新生成 EPUB。
- 不要运行会重建 `bookish_zhcn` 的 `branch_explore_arc/parse_arc.py`。
- Apple Books 里的完整 EPUB 仍只作为可读参考，不可动。
- 本轮敬语工具目前只做 dry-run 评估，真实 `bookish_zhcn` 尚未落地本轮敬语改动。

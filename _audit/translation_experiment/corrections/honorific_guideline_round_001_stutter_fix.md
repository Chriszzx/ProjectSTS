# 敬语称呼准则回填记录：honorific_guideline_round_001_stutter_fix

> 生成时间：2026-06-08 10:31:53
> 范围：`bookish/reading_order/*.md` 与 `bookish_zhcn/reading_order/*.md`
> 原则：按敬语准则策略表回填；只在日文对应行证明称呼关系时自动改；每条操作保留日文依据。

## 本轮状态

- 自动回填：2
- 非空行数量不一致的文件：23

## 规则统计

### hikari-senpai

- 说明：纱夜 → 光先輩：光前辈
- LLM 初判：`光先輩` 仍是前后辈称呼，不应译成“先生”；保留名呼作“光前辈”。
- 本轮应用：0

### hinase-senpai

- 说明：纱夜 → 日生：日生先輩 = 日生前辈
- LLM 初判：策略表规定 `日生先輩` 统一译为“日生前辈”，避免“学长/前辈”摇摆。
- 本轮应用：0

### kirishima-senpai

- 说明：纱夜 → 桐岛：桐島先輩 = 桐岛前辈
- LLM 初判：策略表规定 `桐島先輩` 统一译为“桐岛前辈”。
- 本轮应用：0

### hikari-san-private

- 说明：纱夜/叙述 → 光：光さん = 光
- LLM 初判：策略表规定恋人后私下 `光さん` 译为“光”，正式场合才可用“光先生”。
- 本轮应用：0

### hikari-ojo

- 说明：光 → 纱夜：お嬢 = 小姐
- LLM 初判：策略表规定 `お嬢` 译为“小姐”，`お嬢様` 才译“大小姐”。
- 本轮应用：0

### chiyo-ojousan

- 说明：千代 → 纱夜：お嬢さん = 小姐
- LLM 初判：策略表规定千代的 `お嬢さん` 译为“小姐”，不译“大小姐”。
- 本轮应用：2

### sayo-to-chiyo-san

- 说明：纱夜/叙述 → 千代：千代さん = 千代
- LLM 初判：策略表规定 `千代さん` 默认译“千代”，用句式和“您/请”保留敬度。
- 本轮应用：0

### chiyo-sayo-san

- 说明：千代 → 纱夜：紗夜さん = 纱夜
- LLM 初判：策略表规定千代关键转换 `紗夜さん` 译为“纱夜”，保留从“小姐”到名字的转换。
- 本轮应用：0

### gashomachi-to-sayo-chan

- 说明：卧待 → 纱夜：紗夜ちゃん = 小纱夜
- LLM 初判：用户修正策略表：卧待对纱夜的 `紗夜ちゃん` 固定译“小纱夜”，与夏帆的“纱夜酱”分开。
- 本轮应用：0

## 自动回填明细

- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2623` `chiyo-ojousan`
  - ja `2473`: 千代: 「お、お嬢さん？」
  - before: 千代: 「大、小姐？」
  - after: 千代: 「小、小姐？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6646` `chiyo-ojousan`
  - ja `6357`: 千代: 「お、お嬢さん？」
  - before: 千代: 「大、小姐？」
  - after: 千代: 「小、小姐？」

## 对齐警告

- `bookish_zhcn/reading_order/00_hajimari.md` ja_nonempty=36, zh_nonempty=38
- `bookish_zhcn/reading_order/00_hajimari_gate.md` ja_nonempty=2, zh_nonempty=5
- `bookish_zhcn/reading_order/00_name.md` ja_nonempty=5, zh_nonempty=7
- `bookish_zhcn/reading_order/01_prologue.md` ja_nonempty=1124, zh_nonempty=1125
- `bookish_zhcn/reading_order/02_chapter1.md` ja_nonempty=5794, zh_nonempty=5865
- `bookish_zhcn/reading_order/03_chapter2.md` ja_nonempty=4491, zh_nonempty=4543
- `bookish_zhcn/reading_order/04_chapter3.md` ja_nonempty=8057, zh_nonempty=8151
- `bookish_zhcn/reading_order/05_natsuko.md` ja_nonempty=3, zh_nonempty=5
- `bookish_zhcn/reading_order/06_chapter4_to_hinase_branch.md` ja_nonempty=803, zh_nonempty=819
- `bookish_zhcn/reading_order/07_hinase_chapter4_branch.md` ja_nonempty=644, zh_nonempty=646
- `bookish_zhcn/reading_order/08_hinase.md` ja_nonempty=2953, zh_nonempty=2955
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md` ja_nonempty=6344, zh_nonempty=6468
- `bookish_zhcn/reading_order/10_chapter5_to_kirichiyo_branch.md` ja_nonempty=85, zh_nonempty=89
- `bookish_zhcn/reading_order/11_kirishima_chapter5_branch.md` ja_nonempty=430, zh_nonempty=432
- `bookish_zhcn/reading_order/12_kirishima.md` ja_nonempty=3634, zh_nonempty=3636
- `bookish_zhcn/reading_order/13_chiyo_chapter5_branch.md` ja_nonempty=416, zh_nonempty=418
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md` ja_nonempty=3666, zh_nonempty=3668
- `bookish_zhcn/reading_order/15_chiyo.md` ja_nonempty=468, zh_nonempty=470
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md` ja_nonempty=3592, zh_nonempty=3652
- `bookish_zhcn/reading_order/17_chapter6.md` ja_nonempty=3, zh_nonempty=5
- `bookish_zhcn/reading_order/18_kuro.md` ja_nonempty=3129, zh_nonempty=3131
- `bookish_zhcn/reading_order/19_ao.md` ja_nonempty=4776, zh_nonempty=4778
- `bookish_zhcn/reading_order/20_atogaki.md` ja_nonempty=203, zh_nonempty=205

## 人工审核说明

- `*.operations.jsonl` 是全量操作记录，可按 `human_status` 做二次人工验收。
- `*.alignment_warnings.jsonl` 记录非空行数不一致文件；本轮不使用非空行 zip，而是使用说话人锚点与局部日文触发语确认。

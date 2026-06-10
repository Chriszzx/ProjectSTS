# Branch Variant Cleanup Round 001

- Generated: 2026-06-09T12:58:26
- Operations requested: 57
- Applied: 55
- Skipped: 2

## Policy

- 固定默认主角名为纱夜：保留含纱夜的默认名分支，删除相邻通用/自定义名分支。
- 对 `IF_SKIP/JUMP_OVER` 造成的相邻互斥差分，只保留当前默认/已选路径的一条。
- 对选项后的同一句双译文，保留更符合当前中文口径的一条。

## Applied Operations

### `03_chapter2.md:181` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜酱是特别的啊。那不是当然的嘛～」
- Drop: 宫泽夏帆: 「因为特别嘛。那不是当然的嘛～」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `03_chapter2.md:679` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜是值日生，得早点准备才行，对吧？」
- Drop: 宫泽夏帆: 「今天因为是值日生，不早点准备不行，对吧？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `03_chapter2.md:810` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜是值日生，得早点准备才行，对吧？」
- Drop: 宫泽夏帆: 「今天因为是值日生，不早点准备不行，对吧？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `reading_order/03_chapter2.md:185` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜酱是特别的啊。那不是当然的嘛～」
- Drop: 宫泽夏帆: 「因为特别嘛。那不是当然的嘛～」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `reading_order/03_chapter2.md:706` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜是值日生，得早点准备才行，对吧？」
- Drop: 宫泽夏帆: 「今天因为是值日生，不早点准备不行，对吧？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `reading_order/03_chapter2.md:844` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜是值日生，得早点准备才行，对吧？」
- Drop: 宫泽夏帆: 「今天因为是值日生，不早点准备不行，对吧？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `appendix/endings_and_recovery.md:1251` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜酱是特别的啊。那不是当然的嘛～」
- Drop: 宫泽夏帆: 「因为特别嘛。那不是当然的嘛～」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `appendix/endings_and_recovery.md:1369` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「纱夜是值日生，得早点准备才行，对吧？」
- Drop: 宫泽夏帆: 「今天因为是值日生，不早点准备不行，对吧？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `07_hinase.md:585` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「说这种话～。要是纱夜不在的话，你不是早就乖乖张嘴了？」
- Drop: 宫泽夏帆: 「说这种话～。要是旁边没别人的话，你不是早就乖乖张嘴了？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `reading_order/08_hinase.md:585` `default_name_variant_keep_sayo`

- Keep: 宫泽夏帆: 「说这种话～。要是纱夜不在的话，你不是早就乖乖张嘴了？」
- Drop: 宫泽夏帆: 「说这种话～。要是旁边没别人的话，你不是早就乖乖张嘴了？」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `12_kuro.md:1838` `default_name_variant_keep_sayo`

- Keep: 远野十夜: 「……该道歉的是我才对。纱夜」
- Drop: 远野十夜: 「……该道歉的是我」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `reading_order/18_kuro.md:1842` `default_name_variant_keep_sayo`

- Keep: 远野十夜: 「……该道歉的是我才对。纱夜」
- Drop: 远野十夜: 「……该道歉的是我」
- Note: 固定默认主角名为纱夜；保留含纱夜的默认名分支，删除相邻通用分支。

### `02_chapter1.md:4685` `if_skip_jump_over_keep_first_branch`

- Keep: 远野十夜: 「我又不是一直待在纱夜身边。据我所知，你最近好像经常和她在一起吧」
- Drop: 远野十夜: 「我又不是总陪在纱夜身边。听你说来，最近你好像经常和她在一起」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/02_chapter1.md:4834` `if_skip_jump_over_keep_first_branch`

- Keep: 远野十夜: 「我又不是一直待在纱夜身边。据我所知，你最近好像经常和她在一起吧」
- Drop: 远野十夜: 「我又不是总陪在纱夜身边。听你说来，最近你好像经常和她在一起」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `04_chapter3.md:7415` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不是‘你’，是夏帆！这边是纱夜！！要好好叫名字啊～」
- Drop: 宫泽夏帆: 「不是‘你’，是夏帆！她叫纱夜！！要好好叫名字啊～」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `04_chapter3.md:7734` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不是‘你’，是夏帆！这边是纱夜！！要好好叫名字啊～」
- Drop: 宫泽夏帆: 「不是‘你’，是夏帆！她叫纱夜！！要好好叫名字啊～」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/04_chapter3.md:7641` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不是『你』，是夏帆！这边是纱夜！！要好好叫名字啊～」
- Drop: 宫泽夏帆: 「不是『你』，是夏帆！她叫纱夜！！要好好叫名字啊～」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/04_chapter3.md:7965` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不是『你』，是夏帆！这边是纱夜！！要好好叫名字啊～」
- Drop: 宫泽夏帆: 「不是『你』，是夏帆！她叫纱夜！！要好好叫名字啊～」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `06_chapter4.md:5158` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「……嘿嘿。说什么便当只是借口，其实我只是想去纱夜家玩而已啦」
- Drop: 宫泽夏帆: 「……嘿嘿。说什么便当只是借口，其实我只是想去纱夜家玩而已啦」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `06_chapter4.md:5222` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「好耶！啊，那那我能去纱夜家吗！？」
- Drop: 宫泽夏帆: 「好耶！啊，那那我能去纱夜家吗！？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/09_chapter4_after_hinase_branch.md:4319` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「……嘿嘿。说什么便当只是借口，其实我只是想去纱夜家玩而已啦」
- Drop: 宫泽夏帆: 「……嘿嘿。说什么便当只是借口，其实我只是想去纱夜家玩而已啦」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/09_chapter4_after_hinase_branch.md:4385` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「好耶！啊，那那我能去纱夜家吗！？」
- Drop: 宫泽夏帆: 「好耶！啊，那那我能去纱夜家吗！？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `07_hinase.md:191` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「早上我等着纱夜，正觉得她难得迟到呢，结果她突然跟日生前辈手牵手出现了！！」
- Drop: 宫泽夏帆: 「早上我正想着纱夜难得迟到呢，结果她突然跟日生前辈手牵手出现了！！」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `07_hinase.md:376` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「我不知道啦，但纱夜你的情况就不成立」
- Drop: 宫泽夏帆: 「我不知道啦，不过，纱夜你的情况就是不成立啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `07_hinase.md:527` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「纱夜你家，真的全是书耶～。真搞不懂你是怎么生活的」
- Drop: 宫泽夏帆: 「纱夜你家，真的全是书耶～。真搞不懂你是怎么生活的」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `07_hinase.md:1761` `if_skip_jump_over_keep_first_branch`

- Keep: 日生光: 「实际上，是吧。有很多个‘远野纱夜’，但每一个都是‘远野纱夜’」
- Drop: 日生光: 「实际上，是吧。有很多个‘远野纱夜’，但每一个都是‘远野纱夜’，没有区别」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/08_hinase.md:191` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「早上我等着纱夜，正觉得她难得迟到呢，结果她突然跟日生前辈手牵手出现了！！」
- Drop: 宫泽夏帆: 「早上我正想着纱夜难得迟到呢，结果她突然跟日生前辈手牵手出现了！！」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/08_hinase.md:376` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「我不知道啦，但纱夜你的情况就不成立」
- Drop: 宫泽夏帆: 「我不知道啦，不过，纱夜你的情况就是不成立啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/08_hinase.md:527` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「纱夜你家，真的全是书耶～。真搞不懂你是怎么生活的」
- Drop: 宫泽夏帆: 「纱夜你家，真的全是书耶～。真搞不懂你是怎么生活的」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/08_hinase.md:1765` `if_skip_jump_over_keep_first_branch`

- Keep: 日生光: 「实际上，是吧。有很多个『远野纱夜』，但每一个都是『远野纱夜』」
- Drop: 日生光: 「实际上，是吧。有很多个『远野纱夜』，但每一个都是『远野纱夜』，没有区别」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `08_chapter5.md:438` `if_skip_jump_over_keep_first_branch`

- Keep: 日生光: 「总觉得有点可惜啊。纱夜外表明明那么漂亮，性格却带刺，该怎么说呢」
- Drop: 日生光: 「总觉得有点可惜啊。纱夜外表明明非常漂亮，性格却带刺，该怎么说呢」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/11_kirishima_chapter5_branch.md:188` `if_skip_jump_over_keep_first_branch`

- Keep: 日生光: 「总觉得有点可惜啊。纱夜外表明明那么漂亮，性格却带刺，该怎么说呢」
- Drop: 日生光: 「总觉得有点可惜啊。纱夜外表明明非常漂亮，性格却带刺，该怎么说呢」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/13_chiyo_chapter5_branch.md:188` `if_skip_jump_over_keep_first_branch`

- Keep: 日生光: 「总觉得有点可惜啊。纱夜外表明明那么漂亮，性格却带刺，该怎么说呢」
- Drop: 日生光: 「总觉得有点可惜啊。纱夜外表明明非常漂亮，性格却带刺，该怎么说呢」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/16_chapter5_after_kirichiyo_branch.md:199` `if_skip_jump_over_keep_first_branch`

- Keep: 日生光: 「总觉得有点可惜啊。纱夜外表明明那么漂亮，性格却带刺，该怎么说呢」
- Drop: 日生光: 「总觉得有点可惜啊。纱夜外表明明非常漂亮，性格却带刺，该怎么说呢」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `09_kirishima.md:61` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「……我好像没怎么见过纱夜戴首饰，如果我送你，你会戴吗？」
- Drop: 宫泽夏帆: 「……我好像没怎么见过纱夜戴首饰，如果我送你，你会戴吗？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `09_kirishima.md:759` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「啊哈哈哈！ 好意外～。那个人明明给人运动系的印象～。对吧？ 喂！ 咦！？ 纱、纱夜～？」
- Drop: 宫泽夏帆: 「啊哈哈哈！ 好意外～。那个人明明给人运动系的印象～。对吧？ 喂！ 咦！？ 纱夜～？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `09_kirishima.md:3588` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不知什么时候，七葵前辈开始叫纱夜的名字了……嘛，虽然我也觉得大概是在交往吧，但纱夜不告诉我啊」
- Drop: 宫泽夏帆: 「不知什么时候，七葵前辈开始叫纱夜的名字了……嘛，虽然我也觉得大概是在交往吧，但纱夜什么都不说啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/12_kirishima.md:61` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「……我好像没怎么见过纱夜戴首饰，如果我送你，你会戴吗？」
- Drop: 宫泽夏帆: 「……我好像没怎么见过纱夜戴首饰，如果我送你，你会戴吗？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/12_kirishima.md:761` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「啊哈哈哈！ 好意外～。那个人明明给人运动系的印象～。对吧？ 喂！ 咦！？ 纱、纱夜～？」
- Drop: 宫泽夏帆: 「啊哈哈哈！ 好意外～。那个人明明给人运动系的印象～。对吧？ 喂！ 咦！？ 纱夜～？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/12_kirishima.md:3594` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不知什么时候，七葵前辈开始叫纱夜的名字了……嘛，虽然我也觉得大概是在交往吧，但纱夜不告诉我啊」
- Drop: 宫泽夏帆: 「不知什么时候，七葵前辈开始叫纱夜的名字了……嘛，虽然我也觉得大概是在交往吧，但纱夜什么都不说啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/14_chiyo_kirishima_branch.md:61` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「……我好像没怎么见过纱夜戴首饰，如果我送你，你会戴吗？」
- Drop: 宫泽夏帆: 「……我好像没怎么见过纱夜戴首饰，如果我送你，你会戴吗？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/14_chiyo_kirishima_branch.md:784` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「啊哈哈哈！ 好意外～。那个人明明给人运动系的印象～。对吧？ 喂！ 咦！？ 纱、纱夜～？」
- Drop: 宫泽夏帆: 「啊哈哈哈！ 好意外～。那个人明明给人运动系的印象～。对吧？ 喂！ 咦！？ 纱夜～？」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/14_chiyo_kirishima_branch.md:3632` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「不知什么时候，七葵前辈开始叫纱夜的名字了……嘛，虽然我也觉得大概是在交往吧，但纱夜不告诉我啊」
- Drop: 宫泽夏帆: 「不知什么时候，七葵前辈开始叫纱夜的名字了……嘛，虽然我也觉得大概是在交往吧，但纱夜什么都不说啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `12_kuro.md:2357` `if_skip_jump_over_keep_first_branch`

- Keep: 远野十夜: 「纱夜以前说过苍色是间隙的颜色，但对我来说，苍色看起来是夜的颜色啊」
- Drop: 远野十夜: 「以前纱夜说过苍色是间隙的颜色，但对我来说，苍色看起来是夜的颜色啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/18_kuro.md:2361` `if_skip_jump_over_keep_first_branch`

- Keep: 远野十夜: 「纱夜以前说过苍色是间隙的颜色，但对我来说，苍色看起来是夜的颜色啊」
- Drop: 远野十夜: 「以前纱夜说过苍色是间隙的颜色，但对我来说，苍色看起来是夜的颜色啊」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `13_ao.md:657` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「诶？我拒绝了哦～。因为纱夜酱在嘛」
- Drop: 宫泽夏帆: 「诶？我拒绝了哦～。因为纱夜酱在嘛」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `13_ao.md:1392` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「啊……这、这不是理所当然的吗！有纱夜在的话，一定会非常开心的！！」
- Drop: 宫泽夏帆: 「啊……这、这不是理所当然的吗！有纱夜在的话，一定会超级开心的！！」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/19_ao.md:659` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「诶？我拒绝了哦～。因为纱夜酱在嘛」
- Drop: 宫泽夏帆: 「诶？我拒绝了哦～。因为纱夜酱在嘛」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `reading_order/19_ao.md:1394` `if_skip_jump_over_keep_first_branch`

- Keep: 宫泽夏帆: 「啊……这、这不是理所当然的吗！有纱夜在的话，一定会非常开心的！！」
- Drop: 宫泽夏帆: 「啊……这、这不是理所当然的吗！有纱夜在的话，一定会超级开心的！！」
- Note: 相邻文本来自同一个 IF_SKIP/JUMP_OVER 条件块；当前主线只保留默认/已选路径的第一分支。

### `02_chapter1.md:2167` `post_choice_duplicate_drop_second`

- Keep: 太宰友惠: 「总觉得，真令人怀念……」
- Drop: 太宰友惠: 「总觉得，真令人怀念……」
- Note: 选项后同一句连续重复；保留第一条。

### `02_chapter1.md:3365` `post_choice_duplicate_drop_second`

- Keep: 太宰友惠: 「必须去那个地方……！无论如何……」
- Drop: 太宰友惠: 「必须去那个地方……！无论如何……」
- Note: 选项后同一句连续重复；保留第一条。

### `reading_order/02_chapter1.md:2233` `post_choice_duplicate_drop_second`

- Keep: 太宰友惠: 「总觉得，真令人怀念……」
- Drop: 太宰友惠: 「总觉得，真令人怀念……」
- Note: 选项后同一句连续重复；保留第一条。

### `reading_order/02_chapter1.md:3472` `post_choice_duplicate_drop_second`

- Keep: 太宰友惠: 「必须去那个地方……！无论如何……」
- Drop: 太宰友惠: 「必须去那个地方……！无论如何……」
- Note: 选项后同一句连续重复；保留第一条。

### `reading_order/02_chapter1.md:4977` `double_translation_keep_better_second`

- Keep: 图书管理员: 「是吗……太宰同学啊。总觉得好怀念啊」
- Drop: 图书管理员: 「是吗啊……太宰桑啊。感觉，好怀念啊」
- Note: 同一日文行的双译文；保留更符合当前称呼和中文口径的第二条。

### `reading_order/02_chapter1.md:4980` `double_translation_keep_better_second`

- Keep: 图书管理员: 「她啊，偷偷和班主任在交往呢」
- Drop: 图书管理员: 「她和自己的班主任偷偷交往着呢」
- Note: 同一信息的双译文；保留更贴近日文语气的第二条。

## Skipped Operations

### `02_chapter1.md` `double_translation_keep_better_second` `adjacent_pair_not_found`

- Keep: 图书管理员: 「是吗……太宰同学啊。总觉得好怀念啊」
- Drop: 图书管理员: 「是吗啊……太宰桑啊。感觉，好怀念啊」

### `02_chapter1.md` `double_translation_keep_better_second` `adjacent_pair_not_found`

- Keep: 图书管理员: 「她啊，偷偷和班主任在交往呢」
- Drop: 图书管理员: 「她和自己的班主任偷偷交往着呢」

## Manual Follow-up

### `02_chapter1.md` / `reading_order/02_chapter1.md` `chapter1_librarian_post_choice_manual_followup`

- Source: `processed_output_v3_1/chapter1/chapter1_38.txt:104-167`
- Note: 图书管理员说明太宰友惠过去的段落，原文每个信息点只有一条；中文里连续出现的同义双译不是可保留分支。
- Applied: 顶层 `02_chapter1.md` 使用旧 speaker `司书`，因此手动补清此前两条 `adjacent_pair_not_found`，并同步清理同段后续双译。
- Removed examples:
  - `司书/图书管理员: 「就是有点迷糊，早上还顶着睡癖来，被学生取笑什么的」`
  - `司书/图书管理员: 「谁知道呢。这我就不知道了」`
  - `司书/图书管理员: 「大概是受不了了吧」`
  - `司书/图书管理员: 「谁知道呢？这种事我不是她，所以不清楚」`

### `multiple` `default_name_adjacent_variant_followup`

- Sources checked:
  - `processed_output_v3_1/chapter1/chapter1_1.txt:78`
  - `processed_output_v3_1/chapter1/chapter1_24.txt:53-56`
  - `Json/v0.1.0/chapter2/chapter2_22.json`
  - `Json/v0.1.0/kirishima/kirishima_15.json`
  - `Json/v0.1.0/chapter5/chapter5_29.json`
  - `Json/v0.1.0/hinase/hinase_17.json`
  - `Json/v0.1.0/chapter7_ao/chapter7_ao_43.json`
- Policy: 固定默认主角名后，默认名/泛称相邻差分只保留含“纱夜”的当前主线表达；同一选项后同场景双译只保留一条。
- Representative removals:
  - `？？？: 「哎呀，在这种地方。怎么了？」`
  - `卧待春夫: 「嗯。你也是」`
  - `宫泽夏帆: 「我想果然还是黑色适合你，但偶尔也试试白色。嗯嗯，很配哦～」`
  - `远野十夜: 「对不起……」`

### `multiple` `post_rescan_targeted_cleanup`

- Sources checked:
  - `processed_output_v3_1/chapter1/chapter1_23.txt:1-5`
  - `processed_output_v3_1/chapter7_kuro/chapter7_kuro_32.txt:38-47`
  - `processed_output_v3_1/chapter7_ao/chapter7_ao_12.txt:35`
  - `processed_output_v3_1/chapter7_ao/chapter7_ao_30.txt:3`
  - `processed_output_v3_1/chapter7_ao/chapter7_ao_48.txt:85-88`
- Applied:
  - Removed residual duplicate/generic lines such as `宫泽夏帆: 「……喂」`, `远野十夜: 「纱夜，我爱你啊」`, and one duplicate `宫泽夏帆: 「纱夜酱！早上好～！！」`.
  - Restored the AO line to source shape: `苍` / `『我必须杀了远野纱夜』` / `苍: 「我必须杀了远野」`.

### `multiple` `single_source_line_duplicate_and_misalignment_cleanup`

- Sources checked:
  - `processed_output_v3_1/chapter1/chapter1_26.txt:132-136`
  - `processed_output_v3_1/chapter1/chapter1_42.txt:232-290`
  - `processed_output_v3_1/chapter5/chapter5_45.txt:48`
  - `processed_output_v3_1/chapter7_kuro/chapter7_kuro_33.txt:86`
  - `processed_output_v3_1/chapter6/chapter6_2.txt:64`
  - `processed_output_v3_1/chapter6/chapter6_5.txt:226`
  - `processed_output_v3_1/chapter7_ao/chapter7_ao_27.txt:43`
- Applied:
  - Replaced the second duplicated `太宰友惠: 「不要！！我说了不要！！！！」` with the missing source line `太宰友惠: 「为什么就是不明白呢！！！！」`.
  - Restored the chapter1 Tomoe/sister block where several distinct source lines had collapsed into repeated Chinese lines.
  - Removed single-source duplicate lines in chapter5, chapter6, kuro, and ao.

### `multiple` `honorific_adjacent_variant_cleanup`

- Sources checked:
  - `processed_output_v3_1/chapter3/chapter3_15.txt:280-282`
  - `processed_output_v3_1/chapter4/chapter4_5.txt:3-19`
- Applied:
  - Replaced adjacent Wolmachi/Haruo greeting variants with `卧待春夫: 「小纱夜，你好。放学回家吗？」`.
  - Removed adjacent `管家: 「纱夜大小姐」` / `管家: 「纱夜大小姐……」`, retaining source `紗夜様` as `纱夜小姐`.

### `04_chapter3.md` / `reading_order/04_chapter3.md` `stray_quote_honorific_residue_cleanup`

- Source: `processed_output_v3_1/chapter3/chapter3_7.txt:208`
- Before: `卧待春夫: 「纱夜你毕竟是天生的」大小姐嘛」`
- After: `卧待春夫: 「小纱夜毕竟是天生的大小姐嘛」`
- Note: 原文 `紗夜ちゃんは根っからのお嬢様だもんねぇ`；中文行残留半边引号，且卧待对纱夜称呼应按准则使用“小纱夜”。

### `multiple` `final_similarity_rescan_cleanup`

- Sources checked:
  - `processed_output_v3_1/chapter5/chapter5_35.txt:25-27`
  - `processed_output_v3_1/chapter7_ao/chapter7_ao_40.txt:71-74`
  - `processed_output_v3_1/chapter7_kuro/chapter7_kuro_36.txt:72-77`
- Applied:
  - Removed adjacent `远野十夜: 「……我也是。我心爱的纱夜」`, retaining the first/default line `远野十夜: 「……我也是。我心爱的，心爱的纱夜」`.
  - Removed adjacent AO route non-default duplicate `远野十夜: 「但是，那声哥哥、哥哥的呼唤，……对我而言，那听起来总是悲痛的呼喊」`.
  - Corrected Kuro ending speaker from `十夜: 「我也爱你，十夜」` to `远野纱夜: 「我也爱你，十夜」`.

# 敬语称呼准则回填记录：chiyo_address_round_001

> 生成时间：2026-06-08 10:45:57
> 范围：`bookish/reading_order/*.md` 与 `bookish_zhcn/reading_order/*.md`
> 原则：按敬语准则策略表回填；只在日文对应行证明称呼关系时自动改；每条操作保留日文依据。

## 本轮状态

- 自动回填：62
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
- 本轮应用：0

### sayo-to-chiyo-san

- 说明：纱夜/叙述 → 千代：千代さん = 千代
- LLM 初判：策略表规定 `千代さん` 默认译“千代”，不显性化为先生/小姐/女士/同学/桑；距离感由句式承担。
- 本轮应用：44

### sayo-to-chiyo-san-truncation

- 说明：纱夜 → 千代：千代さ…… = 千代……
- LLM 初判：`千代さ……` 是 `千代さん` 的被打断呼唤；中文按本轮策略保留“千代……”，不残留“千代小”。
- 本轮应用：1

### sayo-to-chiyo-topic-naturalization

- 说明：纱夜 → 千代：千代さん 的中文话题句自然化
- LLM 初判：`千代さん` 后缀不在中文中硬贴成身份或机械二人称；保留“千代”话题感，并按语境使用“你/您/省略”。
- 本轮应用：17

### chiyo-sayo-san

- 说明：千代 → 纱夜：紗夜さん = 纱夜
- LLM 初判：策略表规定千代关键转换 `紗夜さん` 译为“纱夜”，保留从“小姐”到名字的转换。
- 本轮应用：0

### gashomachi-to-sayo-chan

- 说明：卧待 → 纱夜：紗夜ちゃん = 小纱夜
- LLM 初判：用户修正策略表：卧待对纱夜的 `紗夜ちゃん` 固定译“小纱夜”，与夏帆的“纱夜酱”分开。
- 本轮应用：0

## 自动回填明细

- `bookish_zhcn/reading_order/02_chapter1.md:3590` `sayo-to-chiyo-san`
  - ja `3482`: けれど、千代さんは、私の質問に対し、自分達とともゑさんは知り合いではないと答えた。
  - before: 但是，千代女士在回答我的问题时，说的是她和我们以及巴女士并不相识。
  - after: 但是，千代在回答我的问题时，说的是她和我们以及巴女士并不相识。
- `bookish_zhcn/reading_order/02_chapter1.md:4287` `sayo-to-chiyo-topic-naturalization`
  - ja `4153`: 遠野　紗夜: 「……千代さん、どうしてこんな処に？　桐島先輩なら、先程カウンターの方にいましたけれど」
  - before: 远野纱夜: 「……千代，您怎么会在这里？桐岛前辈刚才在服务台那边哦」
  - after: 远野纱夜: 「……千代，怎么会在这里？桐岛前辈刚才在服务台那边哦」
- `bookish_zhcn/reading_order/02_chapter1.md:4307` `sayo-to-chiyo-topic-naturalization`
  - ja `4173`: 遠野　紗夜: 「……ですが、千代さんは私に気づいて欲しいと仰るし、私には何が何だか……」
  - before: 远野纱夜: 「……但是，千代，您却又希望我察觉到什么，我完全搞不懂……」
  - after: 远野纱夜: 「……可是千代却希望我察觉到什么，我完全搞不懂……」
- `bookish_zhcn/reading_order/02_chapter1.md:4641` `sayo-to-chiyo-san`
  - ja `4500`: ともゑさんのこと、桐島先輩と千代さんのこと、兄は終始顎に手を添え、考え込んでいた。
  - before: 关于巴女士的事，关于桐岛前辈和千代女士的事，哥哥始终托着下巴，陷入沉思。
  - after: 关于巴女士的事，关于桐岛前辈和千代的事，哥哥始终托着下巴，陷入沉思。
- `bookish_zhcn/reading_order/02_chapter1.md:4693` `sayo-to-chiyo-san`
  - ja `4552`: もしかすると、千代さんが伝えたかったことはこのことなのではないかと思った。
  - before: 我心想，说不定千代女士想告诉我的，就是这件事。
  - after: 我心想，说不定千代想告诉我的，就是这件事。
- `bookish_zhcn/reading_order/02_chapter1.md:5743` `sayo-to-chiyo-san`
  - ja `5577`: ちなみに、席順は私の隣に蒼が、向かいの席に桐島先輩と千代さんが座っている。
  - before: 顺便一提，座位顺序是我旁边坐着苍，对面坐着桐岛前辈和千代女士。
  - after: 顺便一提，座位顺序是我旁边坐着苍，对面坐着桐岛前辈和千代。
- `bookish_zhcn/reading_order/02_chapter1.md:5747` `sayo-to-chiyo-san`
  - ja `5581`: 遠野　紗夜: 「千代さんは、一体どういう存在なのですか？」
  - before: 远野纱夜: 「千代女士，到底是什么样的存在？」
  - after: 远野纱夜: 「千代，到底是什么样的存在？」
- `bookish_zhcn/reading_order/02_chapter1.md:5761` `sayo-to-chiyo-san`
  - ja `5595`: と、私は少し首を傾け、千代さんの方を見た。
  - before: 我稍微歪了歪头，看向千代女士。
  - after: 我稍微歪了歪头，看向千代。
- `bookish_zhcn/reading_order/02_chapter1.md:5765` `sayo-to-chiyo-san`
  - ja `5599`: 遠野　紗夜: 「千代さんは確かにここにいる、それは確かなことなのです。ここにいる、私達の頭がおかしくなっていない限り」
  - before: 远野纱夜: 「千代女士确实在这里，这是确凿的事实。他就在这里，只要我们的脑子没出问题」
  - after: 远野纱夜: 「千代确实在这里，这是确凿的事实。他就在这里，只要我们的脑子没出问题」
- `bookish_zhcn/reading_order/02_chapter1.md:5769` `sayo-to-chiyo-san`
  - ja `5603`: 紅茶に砂糖を一杯入れ、ぐるぐるとかき混ぜた時に、千代さんが「あ」と声をあげた。
  - before: 往红茶里加了一勺糖，搅动时，千代女士「啊」了一声。
  - after: 往红茶里加了一勺糖，搅动时，千代「啊」了一声。
- `bookish_zhcn/reading_order/02_chapter1.md:5828` `sayo-to-chiyo-topic-naturalization`
  - ja `5662`: 遠野　紗夜: 「はい。……蒼も千代さん達のように不思議な存在を認識出来ますし、それに……」
  - before: 远野纱夜: 「嗯。……苍也能像千代你们那样认知不可思议的存在，而且……」
  - after: 远野纱夜: 「嗯。……苍也能像千代他们那样认知不可思议的存在，而且……」
- `bookish_zhcn/reading_order/02_chapter1.md:5926` `sayo-to-chiyo-topic-naturalization`
  - ja `5760`: 遠野　紗夜: 「……千代さんも言ったでしょう？　私は好奇心が旺盛だと」
  - before: 远野纱夜: 「……千代你也说过吧？说我好奇心旺盛。」
  - after: 远野纱夜: 「……千代也说过吧？说我好奇心旺盛。」
- `bookish_zhcn/reading_order/04_chapter3.md:1109` `sayo-to-chiyo-topic-naturalization`
  - ja `1080`: 遠野　紗夜: 「……本当に気にしないで下さい。家にあげることくらい、何でもないことですから。千代さんなら尚更に」
  - before: 远野纱夜: 「……真的别在意。请您来家里这点小事根本不算什么。尤其是千代，您」
  - after: 远野纱夜: 「……真的别在意。请您来家里这点小事根本不算什么。尤其是千代」
- `bookish_zhcn/reading_order/04_chapter3.md:1138` `sayo-to-chiyo-topic-naturalization`
  - ja `1109`: 遠野　紗夜: 「ふふ。私なんかより、千代さんの方がずっとお優しいと思います」
  - before: 远野纱夜: 「呵呵。我觉得比起我，千代，您要温柔得多了」
  - after: 远野纱夜: 「呵呵。我觉得比起我，千代要温柔得多了」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1039` `sayo-to-chiyo-san`
  - ja `970`: 遠野　紗夜: 「こんにちは、千代さん」
  - before: 远野纱夜: 「你好，千代同学」
  - after: 远野纱夜: 「你好，千代」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1041` `sayo-to-chiyo-san`
  - ja `972`: 千代さんの背後から剣道着姿の桐島先輩が呆れ顔にやって来た。
  - before: 从千代同学背后，穿着剑道服的桐岛前辈一脸无奈地走了过来。
  - after: 从千代背后，穿着剑道服的桐岛前辈一脸无奈地走了过来。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1042` `sayo-to-chiyo-san`
  - ja `973`: 千代さんは腰に手をあて、口を窄めて言う。
  - before: 千代同学双手叉腰，撅着嘴说。
  - after: 千代双手叉腰，撅着嘴说。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1066` `sayo-to-chiyo-san`
  - ja `996`: 遠野　紗夜: 「ちなみに、千代さんは初めてで宜しいのですか？」
  - before: 远野纱夜: 「话说回来，千代同学是第一次吗？」
  - after: 远野纱夜: 「话说回来，千代是第一次吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1068` `sayo-to-chiyo-san`
  - ja `998`: 遠野　紗夜: 「ということは、千代さんはあの時、あの場にいたのですか？」
  - before: 远野纱夜: 「也就是说，千代同学当时也在场吗？」
  - after: 远野纱夜: 「也就是说，千代当时也在场吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1073` `sayo-to-chiyo-san`
  - ja `1003`: そう言うと、千代さんは目を輝かせ、声のトーンを一気にあげた。
  - before: 听我这么说，千代同学眼睛一亮，声音一下子提高了。
  - after: 听我这么说，千代眼睛一亮，声音一下子提高了。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1079` `sayo-to-chiyo-san`
  - ja `1009`: 思わず苦笑すると、千代さんは真剣な顔をし、
  - before: 我不由苦笑，千代同学却一脸认真，
  - after: 我不由苦笑，千代却一脸认真，
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1088` `sayo-to-chiyo-san`
  - ja `1018`: 千代さんは顔を真っ赤にさせながら、照れ笑いをした。
  - before: 千代同学脸红到了脖子根，不好意思地笑了。
  - after: 千代脸红到了脖子根，不好意思地笑了。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1123` `sayo-to-chiyo-san`
  - ja `1047`: 遠野　紗夜: 「こんにちは、千代さん」
  - before: 远野纱夜: 「你好，千代同学」
  - after: 远野纱夜: 「你好，千代」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1125` `sayo-to-chiyo-san`
  - ja `1049`: 千代さんの背後から剣道着姿の桐島先輩が呆れ顔にやって来た。
  - before: 从千代同学背后，穿着剑道服的桐岛前辈一脸无奈地走了过来。
  - after: 从千代背后，穿着剑道服的桐岛前辈一脸无奈地走了过来。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1126` `sayo-to-chiyo-san`
  - ja `1050`: 千代さんは腰に手をあて、口を窄めて言う。
  - before: 千代同学双手叉腰，撅着嘴说。
  - after: 千代双手叉腰，撅着嘴说。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1148` `sayo-to-chiyo-san`
  - ja `1071`: 遠野　紗夜: 「ちなみに、千代さんは初めてで宜しいのですか？」
  - before: 远野纱夜: 「话说回来，千代同学是第一次吗？」
  - after: 远野纱夜: 「话说回来，千代是第一次吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1150` `sayo-to-chiyo-san`
  - ja `1073`: 遠野　紗夜: 「ということは、千代さんはあの時、あの場にいたのですか？」
  - before: 远野纱夜: 「也就是说，千代同学当时也在场吗？」
  - after: 远野纱夜: 「也就是说，千代当时也在场吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1155` `sayo-to-chiyo-san`
  - ja `1078`: そう言うと、千代さんは目を輝かせ、声のトーンを一気にあげた。
  - before: 听我这么说，千代同学眼睛一亮，声音一下子提高了。
  - after: 听我这么说，千代眼睛一亮，声音一下子提高了。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1161` `sayo-to-chiyo-san`
  - ja `1084`: 思わず苦笑すると、千代さんは真剣な顔をし、
  - before: 我不由苦笑，千代同学却一脸认真，
  - after: 我不由苦笑，千代却一脸认真，
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1170` `sayo-to-chiyo-san`
  - ja `1093`: 千代さんは顔を真っ赤にさせながら、照れ笑いをした。
  - before: 千代同学脸红到了脖子根，不好意思地笑了。
  - after: 千代脸红到了脖子根，不好意思地笑了。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1277` `sayo-to-chiyo-topic-naturalization`
  - ja `1193`: 遠野　紗夜: 「千代さんが学校に来るのには許可がいるのですか？」
  - before: 远野纱夜: 「千代你来学校需要许可吗？」
  - after: 远野纱夜: 「千代来学校需要许可吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1446` `sayo-to-chiyo-topic-naturalization`
  - ja `1356`: 遠野　紗夜: 「千代さんが学校に来るのには許可がいるのですか？」
  - before: 远野纱夜: 「千代你来学校需要许可吗？」
  - after: 远野纱夜: 「千代来学校需要许可吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1615` `sayo-to-chiyo-topic-naturalization`
  - ja `1519`: 遠野　紗夜: 「千代さんが学校に来るのには許可がいるのですか？」
  - before: 远野纱夜: 「千代你来学校需要许可吗？」
  - after: 远野纱夜: 「千代来学校需要许可吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1784` `sayo-to-chiyo-topic-naturalization`
  - ja `1682`: 遠野　紗夜: 「千代さんが学校に来るのには許可がいるのですか？」
  - before: 远野纱夜: 「千代你来学校需要许可吗？」
  - after: 远野纱夜: 「千代来学校需要许可吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2559` `sayo-to-chiyo-topic-naturalization`
  - ja `2414`: 千代さんは、授業を聞いていてつまらなくはありませんか？
  - before: 「千代你听课会觉得无聊吗？」
  - after: 「千代听课会觉得无聊吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2654` `sayo-to-chiyo-topic-naturalization`
  - ja `2504`: 遠野　紗夜: 「……千代さんは、私と図書館に行くのが嫌でしょうか？」
  - before: 远野纱夜: 「……千代，您是不愿意和我一起去图书馆吗？」
  - after: 远野纱夜: 「……千代，是不愿意和我一起去图书馆吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2719` `sayo-to-chiyo-topic-naturalization`
  - ja `2564`: 遠野　紗夜: 「……千代さんは、私と図書館に行くのが嫌でしょうか？」
  - before: 远野纱夜: 「……千代，您是不愿意和我一起去图书馆吗？」
  - after: 远野纱夜: 「……千代，是不愿意和我一起去图书馆吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3082` `sayo-to-chiyo-topic-naturalization`
  - ja `2909`: 遠野　紗夜: 「ああ……そういえば千代さんは、桐島先輩の居場所なら分かるのですよね？」
  - before: 远野纱夜: 「啊……说起来，千代你能感知到桐岛前辈在哪里对吧？」
  - after: 远野纱夜: 「啊……说起来，千代能感知到桐岛前辈在哪里对吧？」
- `bookish_zhcn/reading_order/12_kirishima.md:474` `sayo-to-chiyo-topic-naturalization`
  - ja `473`: 遠野　紗夜: 「……千代さんは素敵ですね」
  - before: 远野纱夜: 「……千代，您很优秀呢」
  - after: 远野纱夜: 「……千代真是很棒呢」
- `bookish_zhcn/reading_order/12_kirishima.md:2768` `sayo-to-chiyo-san`
  - ja `2764`: 遠野　紗夜: 「千代さん、おはようございます」
  - before: 远野纱夜: 「千代同学，早上好」
  - after: 远野纱夜: 「千代，早上好」
- `bookish_zhcn/reading_order/12_kirishima.md:2771` `sayo-to-chiyo-san`
  - ja `2767`: 千代さんは手を握ってくれた。
  - before: 千代同学握住了我的手。
  - after: 千代握住了我的手。
- `bookish_zhcn/reading_order/12_kirishima.md:2803` `sayo-to-chiyo-san`
  - ja `2799`: 今日も桐島先輩の眸には千代さんの姿は映らない。
  - before: 今天，桐岛前辈的眼里依然映不出千代同学的身影。
  - after: 今天，桐岛前辈的眼里依然映不出千代的身影。
- `bookish_zhcn/reading_order/12_kirishima.md:2811` `sayo-to-chiyo-san`
  - ja `2807`: 千代さんの顔が花開く様に輝く。
  - before: 千代同学的脸像花朵绽放一样亮了起来。
  - after: 千代的脸像花朵绽放一样亮了起来。
- `bookish_zhcn/reading_order/12_kirishima.md:2822` `sayo-to-chiyo-san`
  - ja `2817`: 遠野　紗夜: 「千代さんが手を繋いで欲しいと」
  - before: 远野纱夜: 「千代同学说想牵一下手」
  - after: 远野纱夜: 「千代说想牵一下手」
- `bookish_zhcn/reading_order/12_kirishima.md:2832` `sayo-to-chiyo-san`
  - ja `2827`: 遠野　紗夜: 「違うと言っています。千代さんが言うには、桐島先輩が帰り道に迷うから手を引いていったのだと」
  - before: 远野纱夜: 「他说不对。千代同学说，是因为桐岛前辈回家会迷路，他才牵着前辈走的」
  - after: 远野纱夜: 「他说不对。千代说，是因为桐岛前辈回家会迷路，他才牵着前辈走的」
- `bookish_zhcn/reading_order/12_kirishima.md:2838` `sayo-to-chiyo-san`
  - ja `2833`: 遠野　紗夜: 「違いません、と千代さんは言っています」
  - before: 远野纱夜: 「他说就是，千代同学这么说的」
  - after: 远野纱夜: 「他说就是，千代这么说的」
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2810` `sayo-to-chiyo-san`
  - ja `2803`: 遠野　紗夜: 「千代さん、おはようございます」
  - before: 远野纱夜: 「千代同学，早上好」
  - after: 远野纱夜: 「千代，早上好」
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2813` `sayo-to-chiyo-san`
  - ja `2806`: 千代さんは手を握ってくれた。
  - before: 千代同学握住了我的手。
  - after: 千代握住了我的手。
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2845` `sayo-to-chiyo-san`
  - ja `2838`: 今日も桐島先輩の眸には千代さんの姿は映らない。
  - before: 今天，桐岛前辈的眼里依然映不出千代同学的身影。
  - after: 今天，桐岛前辈的眼里依然映不出千代的身影。
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2853` `sayo-to-chiyo-san`
  - ja `2846`: 千代さんの顔が花開く様に輝く。
  - before: 千代同学的脸像花朵绽放一样亮了起来。
  - after: 千代的脸像花朵绽放一样亮了起来。
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2864` `sayo-to-chiyo-san`
  - ja `2856`: 遠野　紗夜: 「千代さんが手を繋いで欲しいと」
  - before: 远野纱夜: 「千代同学说想牵一下手」
  - after: 远野纱夜: 「千代说想牵一下手」
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2874` `sayo-to-chiyo-san`
  - ja `2866`: 遠野　紗夜: 「違うと言っています。千代さんが言うには、桐島先輩が帰り道に迷うから手を引いていったのだと」
  - before: 远野纱夜: 「他说不对。千代同学说，是因为桐岛前辈回家会迷路，他才牵着前辈走的」
  - after: 远野纱夜: 「他说不对。千代说，是因为桐岛前辈回家会迷路，他才牵着前辈走的」
- `bookish_zhcn/reading_order/14_chiyo_kirishima_branch.md:2880` `sayo-to-chiyo-san`
  - ja `2872`: 遠野　紗夜: 「違いません、と千代さんは言っています」
  - before: 远野纱夜: 「他说就是，千代同学这么说的」
  - after: 远野纱夜: 「他说就是，千代这么说的」
- `bookish_zhcn/reading_order/15_chiyo.md:4` `sayo-to-chiyo-topic-naturalization`
  - ja `4`: 遠野　紗夜: 「千代さん、私の所へ来ませんか？」
  - before: 远野纱夜: 「千代，您要不要来我这边？」
  - after: 远野纱夜: 「千代，愿意到我这里来吗？」
- `bookish_zhcn/reading_order/15_chiyo.md:366` `sayo-to-chiyo-san-truncation`
  - ja `364`: 遠野　紗夜: 「千代さ……」
  - before: 远野纱夜: 「千代小……」
  - after: 远野纱夜: 「千代……」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:2872` `sayo-to-chiyo-topic-naturalization`
  - ja `2773`: 遠野　紗夜: 「今頃、桐島先輩は、千代さんのことを心配していらっしゃるのではありませんか？」
  - before: 远野纱夜: 「现在，桐岛前辈是不是正担心着千代你呢？」
  - after: 远野纱夜: 「现在，桐岛前辈是不是正担心着千代呢？」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:3386` `sayo-to-chiyo-san`
  - ja `3270`: 遠野　紗夜: 「千代さんのことですか？」
  - before: 远野纱夜: 「您是指千代同学吗？」
  - after: 远野纱夜: 「您是指千代吗？」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:3389` `sayo-to-chiyo-san`
  - ja `3273`: 遠野　紗夜: 「今日は千代さんはいらっしゃらないのですか？」
  - before: 远野纱夜: 「今天千代同学不在吗？」
  - after: 远野纱夜: 「今天千代不在吗？」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:3404` `sayo-to-chiyo-san`
  - ja `3286`: 彼が言うには、昨日私の前に現れた際に千代さんは一緒にいたのだそうだ。
  - before: 据他说，昨天出现在我面前时，千代同学是和他在一起的。
  - after: 据他说，昨天出现在我面前时，千代是和他在一起的。
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:3409` `sayo-to-chiyo-san`
  - ja `3291`: 遠野　紗夜: 「……千代さんは何と？」
  - before: 远野纱夜: 「……千代同学怎么说？」
  - after: 远野纱夜: 「……千代怎么说？」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:3412` `sayo-to-chiyo-san`
  - ja `3294`: 千代さんの姿がこの目に映らなくなった。
  - before: 我的眼睛里，再也映不出千代同学的身影了。
  - after: 我的眼睛里，再也映不出千代的身影了。
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:3425` `sayo-to-chiyo-san`
  - ja `3307`: 遠野　紗夜: 「正しいこととは何ですか？　千代さんの姿が見えないことですか？」
  - before: 远野纱夜: 「您所说的‘正确’是什么？是指看不见千代同学这件事吗？」
  - after: 远野纱夜: 「您所说的‘正确’是什么？是指看不见千代这件事吗？」

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

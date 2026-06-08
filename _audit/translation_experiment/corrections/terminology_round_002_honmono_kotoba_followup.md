# 上下文术语修正记录：terminology_round_002_honmono_kotoba_followup

> 生成时间：2026-06-08 11:47:20
> 范围：`bookish_zhcn/reading_order/*.md`
> 原则：只修正 `言葉` 与 `本物/偽物` 中可由局部上下文稳定判断的 legacy 译法；剩余项进入人工审核。

## 本轮状态

- 自动上下文修正：11
- 人工候选：462

## 自动规则统计

### kotoba-theme-beautiful-words

- 说明：言葉主题词：美しい言葉 -> 美丽/最美的话语
- 初判：`美しい言葉 / 世界で一番美しい言葉` 是全书主题词，这里不是实际语言系统；中文用“话语”比“语言/言语”更自然，也保留诗性。
- 本轮应用：2

### kotoba-world-coloring-scene

- 说明：言葉约定场景：世界を彩る言葉
- 初判：山丘约定场景中的 `言葉` 指能描绘世界、使故事诞生的表达，不是外语或语言系统；叙述中可按语境用“话语/词语”。
- 本轮应用：0

### kotoba-flower-language

- 说明：花相关言葉：花言葉/花に言葉を込める
- 初判：`花言葉` 固定为“花语”；`花に言葉を込める` 在中文里译为“把话语寄托在花上”更顺，也能接住下一句“花语”。
- 本轮应用：0

### kotoba-speech-register

- 说明：言语书面腔：按上下文改为话语/话
- 初判：这些句子里的 `言葉` 是发话、安慰、伤人或表达；“言语”偏书面，按中文自然度改为“话语/话”。
- 本轮应用：2

### kotoba-lexical-word-context

- 说明：言葉词汇语境：词语/各种话语
- 初判：这些句子紧邻“词汇/每学会一个词/旅途中收集”等线索，`言葉` 不是语言系统；按中文语义分别用“词语”或“话语”。
- 本轮应用：7

### kotoba-depth-title

- 说明：Depth副标题：深层之语
- 初判：系统提示中的 `Depth` 副标题需要固定，统一为较自然且不生硬的“深层之语”。
- 本轮应用：0

### honmono-attributive-hinase

- 说明：本物/偽物修饰人名：正牌/冒牌
- 初判：用户确认“正牌/冒牌”适合修饰身份/人名；这里都是日生身份轴的修饰语，替换后避免“真品/赝品/假货+人名”的物品感。
- 本轮应用：0

### honmono-nisemono-legacy-object

- 说明：人物身份轴：去除真品/赝品物品感
- 初判：“真品/赝品”用于人物身份不自然；日生身份轴中改成“正牌/冒牌”或保留“冒牌货”更符合中文口语。
- 本轮应用：0

### honmono-noun-register

- 说明：本物/偽物名词位：本人/冒牌货
- 初判：独立名词位不硬套“正牌/冒牌”：严肃身份确认用“本人”，明确 impostor 用“冒牌货”；成对比较时用“正牌/冒牌”作为标签。
- 本轮应用：0

### honmono-family-context

- 说明：非日生身份轴：母亲真伪
- 初判：亲缘/童话语境不能用鉴定物品的“赝品”；保留真/假的残酷倒置即可。
- 本轮应用：0

## 人工候选统计

### kotoba-remaining-review

- 说明：言葉剩余人工判断
- 初判：剩余项需继续区分主题话语、实际语言系统、单个词、故事台词和 UI 标题。
- 本轮候选：260

### honmono-remaining-review

- 说明：本物/偽物剩余人工判断
- 初判：剩余项需看说话人语气：正牌/冒牌只作修饰或成对标签，名词位按本人、正主、真货、冒牌货等判断。
- 本轮候选：202

## 自动修正明细

- `bookish_zhcn/reading_order/01_prologue.md:263` `kotoba-theme-beautiful-words`
  - before: 远野十夜: 「这样的语言」
  - after: 远野十夜: 「这样的话语」
- `bookish_zhcn/reading_order/01_prologue.md:268` `kotoba-theme-beautiful-words`
  - before: 远野十夜: 「但是，在这个故事里，少女和死神为了寻找那样美好的语言，将要在世界上旅行一番旅程。」
  - after: 远野十夜: 「但是，在这个故事里，少女和死神为了寻找那样美好的话语，将要在世界上旅行一番旅程。」
- `bookish_zhcn/reading_order/04_chapter3.md:3525` `kotoba-speech-register`
  - before: 向苍道谢的不仅是言语，也是我的真心。
  - after: 向苍道谢的不只是话语，也是我的真心。
- `bookish_zhcn/reading_order/18_kuro.md:2553` `kotoba-lexical-word-context`
  - before: 远野纱夜教会了我语言。
  - after: 远野纱夜教会了我词语。
- `bookish_zhcn/reading_order/18_kuro.md:3022` `kotoba-speech-register`
  - before: 远野十夜: 「确实，我……远野十夜或许只是幻想。这份情感和语言，或许也映照着你的心。可是，即便如此，也希望你相信。」
  - after: 远野十夜: 「确实，我……远野十夜或许只是幻想。这份情感和话语，或许也映照着你的心。可是，即便如此，也希望你相信。」
- `bookish_zhcn/reading_order/19_ao.md:896` `kotoba-lexical-word-context`
  - before: 苍: 「我收集了语言。但是，找不到能够匹配这份挂心的词汇。」
  - after: 苍: 「我收集了词语。但是，找不到能够匹配这份挂心的词汇。」
- `bookish_zhcn/reading_order/19_ao.md:897` `kotoba-lexical-word-context`
  - before: 苍: 「我不知道是因为我失去了记忆，还是从一开始就不存在那样的语言。」
  - after: 苍: 「我不知道是因为我失去了记忆，还是从一开始就不存在那样的词语。」
- `bookish_zhcn/reading_order/19_ao.md:3086` `kotoba-lexical-word-context`
  - before: 从幼时起就对任何事物都提不起热情的我，是这本《死神与少女》教会了我认识语言。
  - after: 从幼时起就对任何事物都提不起热情的我，是这本《死神与少女》教会了我认识词语。
- `bookish_zhcn/reading_order/19_ao.md:4839` `kotoba-lexical-word-context`
  - before: 远野纱夜: 「然后，所有遇到的人都教会了我语言」
  - after: 远野纱夜: 「然后，所有遇到的人都教会了我各种话语」
- `bookish_zhcn/reading_order/19_ao.md:4840` `kotoba-lexical-word-context`
  - before: 远野纱夜: 「那些语言，即使与我追寻的不同，也各自是美丽的话语」
  - after: 远野纱夜: 「那些话语，即使与我追寻的不同，也各自美丽」
- `bookish_zhcn/reading_order/19_ao.md:4847` `kotoba-lexical-word-context`
  - before: 苍: 「那是如果不曾在旅途中收集其他许多语言就无法明白的语言」
  - after: 苍: 「那是如果不曾在旅途中收集其他许多话语就无法明白的话语」

## 人工候选样例

- `bookish_zhcn/reading_order/01_prologue.md:157` `honmono-remaining-review`
  - text: 像这样立刻去向本人要答案，就什么思考都没有了，会失去阅读的乐趣。
- `bookish_zhcn/reading_order/02_chapter1.md:1618` `honmono-remaining-review`
  - text: 就算像这样想再多，不直接问他本人也不知道的事，想也是白费功夫。
- `bookish_zhcn/reading_order/02_chapter1.md:1774` `honmono-remaining-review`
  - text: 从外表来看，感觉他年纪和我们也差不多，而且他本人也说了『有朋友在』，所以我猜测他可能是这所学校的相关人士。
- `bookish_zhcn/reading_order/02_chapter1.md:3335` `honmono-remaining-review`
  - text: 而且他本人的容貌也非常美，或许反而因为这一点才更显眼。
- `bookish_zhcn/reading_order/02_chapter1.md:3374` `honmono-remaining-review`
  - text: 站在那里的，正是事件中心人物之一——太宰巴本人。
- `bookish_zhcn/reading_order/02_chapter1.md:4705` `honmono-remaining-review`
  - text: 那些全都是精装书，所以应该比看上去要重得多，但苍本人却丝毫没显出这回事，一脸若无其事的神情。
- `bookish_zhcn/reading_order/02_chapter1.md:4814` `honmono-remaining-review`
  - text: 还有两个选择，要么直接问巴女士本人，要么去问她的姐姐，但我还是决定先再看一遍那本相册。
- `bookish_zhcn/reading_order/03_chapter2.md:46` `honmono-remaining-review`
  - text: 对此，他本人似乎并不特别在意，我也就不再过分追问了。
- `bookish_zhcn/reading_order/03_chapter2.md:216` `honmono-remaining-review`
  - text: 虽然没穿校服，但那个青年确实如夏帆所说，正是日生前辈本人。
- `bookish_zhcn/reading_order/03_chapter2.md:3008` `honmono-remaining-review`
  - text: 路易斯: 「不是这样吗？本人怎么吃得开心才是最重要的吧！」
- `bookish_zhcn/reading_order/03_chapter2.md:3765` `honmono-remaining-review`
  - text: 路易斯: 「哦！那么，您就是那家书店的真正主人了！」
- `bookish_zhcn/reading_order/04_chapter3.md:791` `honmono-remaining-review`
  - text: 苍本人似乎并不在意，只是瞥了我一眼，又扭过头去。
- `bookish_zhcn/reading_order/04_chapter3.md:4804` `honmono-remaining-review`
  - text: 远野纱夜: 「还特地跑到学校来，你们是朋友对吧？想知道他在学校的情况，直接问本人不就没有任何问题了吗？」
- `bookish_zhcn/reading_order/04_chapter3.md:5017` `honmono-remaining-review`
  - text: 苍: 「既然本人那么说了，那就应该是那样吧」
- `bookish_zhcn/reading_order/04_chapter3.md:5039` `honmono-remaining-review`
  - text: 宫泽夏帆: 「想知道的话直接问本人不就好了。他要是不说，自己调查就行了嘛」
- `bookish_zhcn/reading_order/04_chapter3.md:6539` `honmono-remaining-review`
  - text: ？？？: 「终于，真正的日生光出现了」
- `bookish_zhcn/reading_order/04_chapter3.md:6556` `honmono-remaining-review`
  - text: 日生光: 「他害怕的是，万一真正的自己被当成冒牌货了怎么办」
- `bookish_zhcn/reading_order/04_chapter3.md:6558` `honmono-remaining-review`
  - text: 日生光: 「而且周围人的反应，包括学校和家里，没有一个人认为我是冒牌的日生光」
- `bookish_zhcn/reading_order/04_chapter3.md:6709` `honmono-remaining-review`
  - text: ？？？: 「终于，真正的日生光出现了」
- `bookish_zhcn/reading_order/04_chapter3.md:6726` `honmono-remaining-review`
  - text: 日生光: 「他害怕的是，万一真正的自己被当成冒牌货了怎么办」
- `bookish_zhcn/reading_order/04_chapter3.md:6728` `honmono-remaining-review`
  - text: 日生光: 「而且周围人的反应，包括学校和家里，没有一个人认为我是冒牌的日生光」
- `bookish_zhcn/reading_order/04_chapter3.md:6862` `honmono-remaining-review`
  - text: 远野纱夜: 「嗯。暂时来说是这样。据他本人说只是睡眠不足」
- `bookish_zhcn/reading_order/04_chapter3.md:6979` `honmono-remaining-review`
  - text: 桐岛七葵: 「住手，威廉。远野的父母跟远野本人没关系吧」
- `bookish_zhcn/reading_order/04_chapter3.md:6998` `honmono-remaining-review`
  - text: 宫泽夏帆: 「再说凭什么你来决定？ 夏目到底幸不幸福，不问本人怎么会知道！」
- `bookish_zhcn/reading_order/04_chapter3.md:7041` `honmono-remaining-review`
  - text: 我重新转向本人，道了谢。
- `bookish_zhcn/reading_order/04_chapter3.md:7078` `honmono-remaining-review`
  - text: 夏目悠希: 「这我还想问呢！……那家伙好像认识我，但我对他本人有没有印象……大概没有，应该」
- `bookish_zhcn/reading_order/04_chapter3.md:7450` `honmono-remaining-review`
  - text: 但当事人夏目本人似乎并不怎么在意这一点，
- `bookish_zhcn/reading_order/04_chapter3.md:7774` `honmono-remaining-review`
  - text: 但当事人夏目本人似乎并不怎么在意这一点，
- `bookish_zhcn/reading_order/04_chapter3.md:8378` `honmono-remaining-review`
  - text: 其实我心里明白，她本人并没有错。
- `bookish_zhcn/reading_order/07_hinase_chapter4_branch.md:388` `honmono-remaining-review`
  - text: 远野十夜: 「嗯，谁知道呢。说到底，也许取决于公主本人」
- `bookish_zhcn/reading_order/07_hinase_chapter4_branch.md:389` `honmono-remaining-review`
  - text: 远野纱夜: 「取决于公主本人……」
- `bookish_zhcn/reading_order/07_hinase_chapter4_branch.md:493` `honmono-remaining-review`
  - text: 桐岛七葵: 「问题在于本人的上进心和努力。如果你自己想变强的话，总有一天一定能做到的」
- `bookish_zhcn/reading_order/08_hinase.md:611` `honmono-remaining-review`
  - text: 日生光: 「那是他们本人决定的事情。」
- `bookish_zhcn/reading_order/08_hinase.md:1919` `honmono-remaining-review`
  - text: 日生光: 「正牌和冒牌的区别。」
- `bookish_zhcn/reading_order/08_hinase.md:1922` `honmono-remaining-review`
  - text: 女学生: 「光看是看不出来的。在我看来，你看起来很像真货。」
- `bookish_zhcn/reading_order/08_hinase.md:1931` `honmono-remaining-review`
  - text: 日生光: 「除非杀掉真正的日生光，彻底销毁证据。」
- `bookish_zhcn/reading_order/08_hinase.md:1933` `honmono-remaining-review`
  - text: 日生光: 「但是，当事人日生光本人和日生紫却很难注意到这点。」
- `bookish_zhcn/reading_order/08_hinase.md:1937` `honmono-remaining-review`
  - text: 日生光: 「确实。真正的日生光虽然迟了，但发现了自己和我的区别，对自己是真货有了自信。」
- `bookish_zhcn/reading_order/08_hinase.md:1938` `honmono-remaining-review`
  - text: 女学生: 「然后，作为冒牌货的你会离开这个小镇。」
- `bookish_zhcn/reading_order/08_hinase.md:2478` `honmono-remaining-review`
  - text: 日生紫: 「至今为止和我们在一起的「日生光」是冒牌货」
- `bookish_zhcn/reading_order/08_hinase.md:2490` `honmono-remaining-review`
  - text: 日生光: 「刚才这位祖母也说了，你认为是『日生光』的那个是『冒牌货」
- `bookish_zhcn/reading_order/08_hinase.md:2512` `honmono-remaining-review`
  - text: 日生光: 「要怎样才能让你相信呢。那个冒牌货昨天就已经不知道跑到哪里去了」
- `bookish_zhcn/reading_order/08_hinase.md:2579` `honmono-remaining-review`
  - text: 日生光: 「你说对吧？因为那家伙，可是完美地扮演了大家所期望的‘日生光’啊。要是没人相信我的话，反而认定我是冒牌货，那岂不得憋屈死。」
- `bookish_zhcn/reading_order/08_hinase.md:2583` `honmono-remaining-review`
  - text: 日生光: 「我一直在找。能分辨假货和真货的证据。」
- `bookish_zhcn/reading_order/08_hinase.md:2586` `honmono-remaining-review`
  - text: 日生光: 「真是蠢到家了！！居然被冒牌货的谎言耍得团团转！！」
- `bookish_zhcn/reading_order/08_hinase.md:2629` `honmono-remaining-review`
  - text: 是吗。原来真货会这样发怒啊，我像站在旁观者立场一样冷静地想道。
- `bookish_zhcn/reading_order/08_hinase.md:2672` `honmono-remaining-review`
  - text: 如果我认识的那个人是冒牌货的话，
- `bookish_zhcn/reading_order/08_hinase.md:2770` `honmono-remaining-review`
  - text: 日生光: 「为了接近真货，我把容貌、兴趣爱好全部改了。」
- `bookish_zhcn/reading_order/08_hinase.md:2771` `honmono-remaining-review`
  - text: 日生光: 「连这说话方式，也和真货一样吧？」
- `bookish_zhcn/reading_order/08_hinase.md:2773` `honmono-remaining-review`
  - text: 和真货一样。
- `bookish_zhcn/reading_order/08_hinase.md:2775` `honmono-remaining-review`
  - text: 远野纱夜: 「……我并不怎么了解正牌的‘日生光’。」
- `bookish_zhcn/reading_order/08_hinase.md:2777` `honmono-remaining-review`
  - text: 是的。对我来说，那才是『真货』。
- `bookish_zhcn/reading_order/08_hinase.md:2799` `honmono-remaining-review`
  - text: 日生光: 「但是『日生光』是假的。既不是『我』，更不是正牌的『日生光」
- `bookish_zhcn/reading_order/08_hinase.md:2948` `honmono-remaining-review`
  - text: 没想到，被囚禁的公主，竟然就是魔女本人
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:621` `honmono-remaining-review`
  - text: 远野十夜: 「嗯，谁知道呢。说到底，也许取决于公主本人」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:622` `honmono-remaining-review`
  - text: 远野纱夜: 「取决于公主本人……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:728` `honmono-remaining-review`
  - text: 桐岛七葵: 「问题在于本人的上进心和努力。如果你自己想变强的话，总有一天一定能做到的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:1990` `honmono-remaining-review`
  - text: 桐岛七葵: 「如果在意的话，明天直接去问本人不就好了。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2038` `honmono-remaining-review`
  - text: 之前他似乎本人也说过类似的事。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2059` `honmono-remaining-review`
  - text: 桐岛七葵: 「如果在意的话，明天直接去问本人不就好了。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:2378` `honmono-remaining-review`
  - text: 桐岛七葵: 「怎么可能。那确实就是你本人」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3123` `honmono-remaining-review`
  - text: 无声无息地出现的，正是事件中心人物——日生前辈本人。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3213` `honmono-remaining-review`
  - text: 桐岛七葵: 「……啊，这么说来确实。不过，如果是本人那也正常吧」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3214` `honmono-remaining-review`
  - text: 远野纱夜: 「嗯……果然，那时的他就是日生本人吧……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3244` `honmono-remaining-review`
  - text: 那时候的他，真的是日生本人吗？
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3390` `honmono-remaining-review`
  - text: 桐岛七葵: 「……啊，这么说来确实。不过，如果是本人那也正常吧」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3391` `honmono-remaining-review`
  - text: 远野纱夜: 「嗯……果然，那时的他就是日生本人吧……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3421` `honmono-remaining-review`
  - text: 那时候的他，真的是日生本人吗？
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3656` `honmono-remaining-review`
  - text: 苍: 「这样一来，声称看到二重身的第三方，如果被说成只是和别人长得像，或者就是本人，那话题就到此为止了」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3673` `honmono-remaining-review`
  - text: 远野纱夜: 「可是，我们见到的日生前辈毫无疑问就是日生前辈本人，这样一来，连那句话本身都有可能是谎言」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3693` `honmono-remaining-review`
  - text: 日生光: 「初次见面和不是初次见面的人，晚上好。我才是正牌的『日生光」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3705` `honmono-remaining-review`
  - text: 桐岛七葵: 「正牌的『日生光』？那你说我们一直见到的是谁？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3706` `honmono-remaining-review`
  - text: 日生光: 「冒牌的『日生光」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3714` `honmono-remaining-review`
  - text: 远野纱夜: 「如果您的话是真的，那就意味着存在两个外貌相同的叫『日生光』的人。您说是冒牌货的那位日生前辈，难道不是二重身或者失散的兄弟吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3716` `honmono-remaining-review`
  - text: 桐岛七葵: 「可你说自己是正牌的『日生光』吧？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3717` `honmono-remaining-review`
  - text: 日生光: 「正因为是真的，才不知道啊。冒牌货反而知道更多真相」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3722` `honmono-remaining-review`
  - text: 远野纱夜: 「那，真正的您和冒牌的『日生光』穿着相同的服装，这是什么原因？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3731` `honmono-remaining-review`
  - text: 日生光: 「我回到这个镇上，从发现我的冒牌货那天起，就一直在监视『日生光』。当然，也监视了你们」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3734` `honmono-remaining-review`
  - text: 日生光: 「希望你们能找到证据，证明『日生光』是冒牌货」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3741` `honmono-remaining-review`
  - text: 日生光: 「正因为是真的啊。单论这一点，反而冒牌货可能更接近真的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3744` `honmono-remaining-review`
  - text: 桐岛七葵: 「但也有可能你本人是冒牌货，在说谎吧？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3747` `honmono-remaining-review`
  - text: 远野纱夜: 「……简单来说，您直接出现在冒牌货面前不就好了吗？那样的话，通过检查之类的方法，就能知道谁是真的了」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3753` `honmono-remaining-review`
  - text: 日生光: 「冒牌货知道真的存在」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3770` `honmono-remaining-review`
  - text: 日生光: 「但是，我是真的。正牌的『日生光』。那家伙，不是我」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3773` `honmono-remaining-review`
  - text: 日生光: 「我和那家伙都是相同的『日生光』，但一定有什么东西能证明那家伙是冒牌货。因为那家伙不是真的嘛」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3774` `honmono-remaining-review`
  - text: 苍: 「那么，假设我们认识的『日生光』是冒牌货，作为正牌的『日生光』，你打算今后怎么做？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3852` `honmono-remaining-review`
  - text: 桐岛七葵: 「正牌的『日生光』？那你说我们一直见到的是谁？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3853` `honmono-remaining-review`
  - text: 日生光: 「冒牌的『日生光」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3861` `honmono-remaining-review`
  - text: 远野纱夜: 「如果您的话是真的，那就意味着存在两个外貌相同的叫『日生光』的人。您说是冒牌货的那位日生前辈，难道不是二重身或者失散的兄弟吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3863` `honmono-remaining-review`
  - text: 桐岛七葵: 「可你说自己是正牌的『日生光』吧？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3864` `honmono-remaining-review`
  - text: 日生光: 「正因为是真的，才不知道啊。冒牌货反而知道更多真相」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3869` `honmono-remaining-review`
  - text: 远野纱夜: 「那，真正的您和冒牌的『日生光』穿着相同的服装，这是什么原因？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3878` `honmono-remaining-review`
  - text: 日生光: 「我回到这个镇上，从发现我的冒牌货那天起，就一直在监视『日生光』。当然，也监视了你们」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3881` `honmono-remaining-review`
  - text: 日生光: 「希望你们能找到证据，证明『日生光』是冒牌货」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3888` `honmono-remaining-review`
  - text: 日生光: 「正因为是真的啊。单论这一点，反而冒牌货可能更接近真的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3891` `honmono-remaining-review`
  - text: 桐岛七葵: 「但也有可能你本人是冒牌货，在说谎吧？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3894` `honmono-remaining-review`
  - text: 远野纱夜: 「……简单来说，您直接出现在冒牌货面前不就好了吗？那样的话，通过检查之类的方法，就能知道谁是真的了」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3900` `honmono-remaining-review`
  - text: 日生光: 「冒牌货知道真的存在」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3917` `honmono-remaining-review`
  - text: 日生光: 「但是，我是真的。正牌的『日生光』。那家伙，不是我」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3920` `honmono-remaining-review`
  - text: 日生光: 「我和那家伙都是相同的『日生光』，但一定有什么东西能证明那家伙是冒牌货。因为那家伙不是真的嘛」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3921` `honmono-remaining-review`
  - text: 苍: 「那么，假设我们认识的『日生光』是冒牌货，作为正牌的『日生光』，你打算今后怎么做？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3999` `honmono-remaining-review`
  - text: 远野十夜: 「你没见过那个正牌的『日生前辈』和冒牌的『日生前辈』站在一起的样子吧。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4076` `honmono-remaining-review`
  - text: 远野十夜: 「你没见过那个正牌的『日生前辈』和冒牌的『日生前辈』站在一起的样子吧。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4181` `honmono-remaining-review`
  - text: 远野纱夜: 「关于日生前辈的事。就是找出正牌和冒牌货的区别。我们在学校会和日生前辈碰面，但你不一样」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4413` `honmono-remaining-review`
  - text: 但这样根本分不清哪个是正牌哪个是冒牌，
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4422` `honmono-remaining-review`
  - text: 远野纱夜: 「连本人都没发现的话，我们这些外人就更不可能发现了吧……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4498` `honmono-remaining-review`
  - text: 日生光: 「称呼起来不方便吧？正牌也好冒牌也好，都叫日生光的话」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4520` `honmono-remaining-review`
  - text: 仿佛『冒牌的日生光』从一开始
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4521` `honmono-remaining-review`
  - text: 就不存在一样，他就是『正牌的日生光』。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4523` `honmono-remaining-review`
  - text: 我们也从一开始就不知道『正牌的日生光』是什么样子。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4525` `honmono-remaining-review`
  - text: 分辨出『正牌』和『冒牌』呢？
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4618` `honmono-remaining-review`
  - text: 仿佛『冒牌的日生光』从一开始
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4619` `honmono-remaining-review`
  - text: 就不存在一样，他就是『正牌的日生光』。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4621` `honmono-remaining-review`
  - text: 我们也从一开始就不知道『正牌的日生光』是什么样子。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4623` `honmono-remaining-review`
  - text: 分辨出『正牌』和『冒牌』呢？
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4834` `honmono-remaining-review`
  - text: 千代: 「那么，『日生』同学一直是『日生光』同学本人？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4847` `honmono-remaining-review`
  - text: 桐岛七葵: 「你也该老实回答了吧。为什么你作为本人，却不肯出现在冒牌货面前？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4853` `honmono-remaining-review`
  - text: 日生光: 「我没有自信。我非常害怕被别人说我是冒牌货。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4856` `honmono-remaining-review`
  - text: 远野纱夜: 「话是这么说，但您应该是本人吧？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4861` `honmono-remaining-review`
  - text: 日生光: 「正牌的『日生光』、冒牌的『日生光』，还有理想的『日生光』。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4869` `honmono-remaining-review`
  - text: 日生光: 「但是，那不是我。那是假的、冒牌的我。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4870` `honmono-remaining-review`
  - text: 日生光: 「我拼命地扮演着冒牌的『日生光』。每天每天每天。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4878` `honmono-remaining-review`
  - text: 日生光: 「之后就如各位所知，久违地回到家里，却发现有个和我一模一样的冒牌货大摇大摆地待在那里。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4881` `honmono-remaining-review`
  - text: 日生光: 「周围的人毫不怀疑。关系不错的朋友、共同生活了几十年的外婆，全都深信不疑地认为那个冒牌货才是本人。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4882` `honmono-remaining-review`
  - text: 日生光: 「这就是我不愿意出现在那家伙面前的原因。以现在的情况来看，反而是我更像冒牌货。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4891` `honmono-remaining-review`
  - text: 远野纱夜: 「那么，现在我们接触的这个『日生光』，是『本人』吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4892` `honmono-remaining-review`
  - text: 日生光: 「所以我从一开始就说了，我是『本人』啊。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4893` `honmono-remaining-review`
  - text: 远野纱夜: 「但是，在我们看来，您和那个冒牌的『日生光』看起来没有任何区别。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4894` `honmono-remaining-review`
  - text: 日生光: 「那也没办法。因为本人和冒牌货，都在扮演同一个理想的『日生光』。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4910` `honmono-remaining-review`
  - text: 苍: 「本人和冒牌货，甚至还出现了理想的『日生光』吗。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4919` `honmono-remaining-review`
  - text: 桐岛七葵: 「那家伙去追日生了……追那个自称‘真货’的家伙了」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4952` `honmono-remaining-review`
  - text: 远野纱夜: 「正牌的‘日生光’、冒牌的‘日生光’、理想的‘日生光’……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4961` `honmono-remaining-review`
  - text: 远野纱夜: 「据说存在一个理想的‘日生光’，而真货和假货都在分别扮演那个理想的‘日生光’」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4972` `honmono-remaining-review`
  - text: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:4978` `honmono-remaining-review`
  - text: 那个人说过，希望我们能找到『日生光』是冒牌货的证据。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5031` `honmono-remaining-review`
  - text: 远野纱夜: 「正牌的‘日生光’、冒牌的‘日生光’、理想的‘日生光’……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5040` `honmono-remaining-review`
  - text: 远野纱夜: 「据说存在一个理想的‘日生光’，而真货和假货都在分别扮演那个理想的‘日生光’」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5051` `honmono-remaining-review`
  - text: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5057` `honmono-remaining-review`
  - text: 那个人说过，希望我们能找到『日生光』是冒牌货的证据。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5268` `honmono-remaining-review`
  - text: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5348` `honmono-remaining-review`
  - text: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5438` `honmono-remaining-review`
  - text: 日生光: 「我想换个叫法，好跟那个冒牌货区分开来啦。纱夜叫纱夜，苍先生叫苍先生，但桐岛君名字是七葵，所以就叫小七。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5462` `honmono-remaining-review`
  - text: 日生光: 「名字明明是用来区分的，可被冒用了名字的我，还能算是‘真货’吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5517` `honmono-remaining-review`
  - text: 日生光: 「这样我就是真货了。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5776` `honmono-remaining-review`
  - text: 远野纱夜: 「我终于明白了。明白那个能证明谁才是冒牌货、谁才是真货的方法」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5779` `honmono-remaining-review`
  - text: 远野纱夜: 「在两个日生光并排的情况下，我会准确判断出哪一个是真货」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5780` `honmono-remaining-review`
  - text: 日生光: 「那有什么确切的依据吗？不会把正牌和冒牌弄错吧？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:5795` `honmono-remaining-review`
  - text: 千代: 「你是什么时候发现正牌和冒牌的区别的？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6044` `honmono-remaining-review`
  - text: 远野纱夜: 「我一直在寻找，你所说的，正牌和冒牌的区别到底在哪里。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6094` `honmono-remaining-review`
  - text: 桐岛七葵: 「是啊。那家伙，真正的日生光去哪儿了？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6097` `honmono-remaining-review`
  - text: 苍: 「根据纱夜的话来整理，从一开始，你们面前就没有出现过真正的日生光。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6132` `honmono-remaining-review`
  - text: 日生光: 「明明抓着我这个冒牌货，却毫不怀疑地喊着『光先生』呢。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6139` `honmono-remaining-review`
  - text: 日生光: 「看到您那副样子，我立刻就明白真货为什么逃跑了。确实，这实在是太压抑了。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6142` `honmono-remaining-review`
  - text: 日生光: 「意识到这一点之后，我就老实照着办了。很轻松哦，完全变成真正的日生光这件事。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6181` `honmono-remaining-review`
  - text: 关于他的事，关于一直以来发生的事，关于真正的日生光现在怎么样了的事，还有……
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6191` `honmono-remaining-review`
  - text: 远野纱夜: 「有两个一模一样的人，在本人不在的时候，冒牌货顶替了正主——这种童话故事谁会信呢？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6200` `honmono-remaining-review`
  - text: 远野纱夜: 「您从日生前辈身上寻求的，并不是日生前辈本人」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6201` `honmono-remaining-review`
  - text: 远野纱夜: 「真正的日生前辈——他难道不是希望您能注意到他吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6224` `honmono-remaining-review`
  - text: 日生光: 「唉——明明以为能顺利成功的。只要没被你发现，我本来能变成真货的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6227` `honmono-remaining-review`
  - text: 远野纱夜: 「如果你真想变成真货，你本来能撒出更完美的谎的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6228` `honmono-remaining-review`
  - text: 远野纱夜: 「甚至能在我们得知真货存在之前，就变成真货——难道不是吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6250` `honmono-remaining-review`
  - text: 苍: 「但你并没有那么做。不仅如此，你还特意采取了行动——让我们知道存在正牌和冒牌两个日生光」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6251` `honmono-remaining-review`
  - text: 苍: 「然后，你让我们去寻找证明冒牌货就是冒牌货的证据」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6272` `honmono-remaining-review`
  - text: 远野纱夜: 「只是，我所认识的那个『日生光』并不是真货——一直都是『你」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6414` `honmono-remaining-review`
  - text: 日生光: 「唉——明明以为能顺利成功的。只要没被你发现，我本来能变成真货的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6417` `honmono-remaining-review`
  - text: 远野纱夜: 「如果你真想变成真货，你本来能撒出更完美的谎的」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6418` `honmono-remaining-review`
  - text: 远野纱夜: 「甚至能在我们得知真货存在之前，就变成真货——难道不是吗？」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6440` `honmono-remaining-review`
  - text: 苍: 「但你并没有那么做。不仅如此，你还特意采取了行动——让我们知道存在正牌和冒牌两个日生光」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6441` `honmono-remaining-review`
  - text: 苍: 「然后，你让我们去寻找证明冒牌货就是冒牌货的证据」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6462` `honmono-remaining-review`
  - text: 远野纱夜: 「只是，我所认识的那个『日生光』并不是真货——一直都是『你」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6661` `honmono-remaining-review`
  - text: 那儿的，不是刚才应该在港口的他……而是真正的日生光。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6664` `honmono-remaining-review`
  - text: 真正的日生光似乎昏迷着，双眼紧闭。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6704` `honmono-remaining-review`
  - text: 不过，后来真正的日生光告诉了我们。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6713` `honmono-remaining-review`
  - text: 日生光: 「我明明应该在这里，那眼前的那个家伙是谁？那不是我。那是个长着我模样的冒牌货。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6714` `honmono-remaining-review`
  - text: 日生光: 「更让我惊讶的是，所有人都对那个冒牌货是『日生光』深信不疑。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6716` `honmono-remaining-review`
  - text: 日生光: 「要是外人，倒还说得通。可就连有血缘关系的奶奶，都对面那个冒牌货深信不疑，这一点可真让我吃惊。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6721` `honmono-remaining-review`
  - text: 日生光: 「你说对吧？因为那家伙，可是完美地扮演了大家所期望的‘日生光’啊。要是没人相信我的话，反而认定我是冒牌货，那岂不得憋屈死。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6728` `honmono-remaining-review`
  - text: 日生光: 「说起来，你可能没注意到，有一次我真的在你们面前露过脸。不过是假扮成冒牌日生光的模样。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6735` `honmono-remaining-review`
  - text: 日生光: 「之后，我继续监视着那个冒牌货。」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6738` `honmono-remaining-review`
  - text: 日生光: 「一开始我完全搞不懂他在干什么，可偷听了对话才发现，那家伙好像是在主动跟你们暴露冒牌货的存在。」
- 其余 282 条见 `*.review.jsonl`。

## 人工审核说明

- `*.operations.jsonl` 记录自动上下文修正，可逐条验收或回滚。
- `*.review.jsonl` 记录尚需人工或 LLM 精判的剩余候选。

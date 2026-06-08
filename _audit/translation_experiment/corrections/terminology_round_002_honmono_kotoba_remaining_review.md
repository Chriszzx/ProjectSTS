# 上下文术语修正记录：terminology_round_002_honmono_kotoba_remaining_review

> 生成时间：2026-06-08 11:48:11
> 范围：`bookish_zhcn/reading_order/*.md`
> 原则：只修正 `言葉` 与 `本物/偽物` 中可由局部上下文稳定判断的 legacy 译法；剩余项进入人工审核。

## 本轮状态

- 自动上下文修正：0
- 人工候选：417

## 自动规则统计

### kotoba-theme-beautiful-words

- 说明：言葉主题词：美しい言葉 -> 美丽/最美的话语
- 初判：`美しい言葉 / 世界で一番美しい言葉` 是全书主题词，这里不是实际语言系统；中文用“话语”比“语言/言语”更自然，也保留诗性。
- 本轮应用：0

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
- 本轮应用：0

### kotoba-lexical-word-context

- 说明：言葉词汇语境：词语/各种话语
- 初判：这些句子紧邻“词汇/每学会一个词/旅途中收集”等线索，`言葉` 不是语言系统；按中文语义分别用“词语”或“话语”。
- 本轮应用：0

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
- 本轮候选：157

## 自动修正明细

- 本轮没有自动修正。

## 人工候选样例

- `bookish_zhcn/reading_order/03_chapter2.md:216` `honmono-remaining-review`
  - text: 虽然没穿校服，但那个青年确实如夏帆所说，正是日生前辈本人。
- `bookish_zhcn/reading_order/03_chapter2.md:3765` `honmono-remaining-review`
  - text: 路易斯: 「哦！那么，您就是那家书店的真正主人了！」
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
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3123` `honmono-remaining-review`
  - text: 无声无息地出现的，正是事件中心人物——日生前辈本人。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3214` `honmono-remaining-review`
  - text: 远野纱夜: 「嗯……果然，那时的他就是日生本人吧……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3244` `honmono-remaining-review`
  - text: 那时候的他，真的是日生本人吗？
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3391` `honmono-remaining-review`
  - text: 远野纱夜: 「嗯……果然，那时的他就是日生本人吧……」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:3421` `honmono-remaining-review`
  - text: 那时候的他，真的是日生本人吗？
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
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6820` `honmono-remaining-review`
  - text: 这，就是正主。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6836` `honmono-remaining-review`
  - text: 我想，一定没有人能察觉到他是冒牌货吧。那个少女也是。
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6840` `honmono-remaining-review`
  - text: 「终于，真正的日生光出现了」
- `bookish_zhcn/reading_order/09_chapter4_after_hinase_branch.md:6842` `honmono-remaining-review`
  - text: 他似乎在我传达消息之前，就已经察觉到了真货的存在。
- `bookish_zhcn/reading_order/10_chapter5_to_kirichiyo_branch.md:80` `honmono-remaining-review`
  - text: 因为，我所认识的，是那个『冒牌货』。
- `bookish_zhcn/reading_order/11_kirishima_chapter5_branch.md:77` `honmono-remaining-review`
  - text: 远野纱夜: 「……我并不是讨厌光前辈。只是，至今仍然不敢相信我所认识的他是冒牌货」
- `bookish_zhcn/reading_order/11_kirishima_chapter5_branch.md:86` `honmono-remaining-review`
  - text: 桐岛七葵: 「毕竟，是血缘相通的家人啊。相处的时间，也是真货长得多吧」
- `bookish_zhcn/reading_order/13_chiyo_chapter5_branch.md:77` `honmono-remaining-review`
  - text: 远野纱夜: 「……我并不是讨厌光前辈。只是，至今仍然不敢相信我所认识的他是冒牌货」
- `bookish_zhcn/reading_order/13_chiyo_chapter5_branch.md:86` `honmono-remaining-review`
  - text: 桐岛七葵: 「毕竟，是血缘相通的家人啊。相处的时间，也是真货长得多吧」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:88` `honmono-remaining-review`
  - text: 远野纱夜: 「……我并不是讨厌光前辈。只是，至今仍然不敢相信我所认识的他是冒牌货」
- `bookish_zhcn/reading_order/16_chapter5_after_kirichiyo_branch.md:97` `honmono-remaining-review`
  - text: 桐岛七葵: 「毕竟，是血缘相通的家人啊。相处的时间，也是真货长得多吧」
- `bookish_zhcn/reading_order/20_atogaki.md:90` `honmono-remaining-review`
  - text: 卧待春夫: 「顺便说，这件事，那个……冒牌的『日生光』也注意到了」
- `bookish_zhcn/reading_order/20_atogaki.md:100` `honmono-remaining-review`
  - text: 卧待春夫: 「他没有时间了。当然，他本也可以成为真货」
- `bookish_zhcn/reading_order/20_atogaki.md:154` `honmono-remaining-review`
  - text: 卧待春夫: 「你正如所见，是这个世界里的局外人，而冒牌日生君是知道她的一切却仍然能爱她的人。而且更重要的是，他有着把公主带出去的职责」
- `bookish_zhcn/reading_order/01_prologue.md:15` `kotoba-remaining-review`
  - text: 「我在寻找世界上最美的话语。」
- `bookish_zhcn/reading_order/01_prologue.md:16` `kotoba-remaining-review`
  - text: 「美丽的话语，是指诗吗？」
- `bookish_zhcn/reading_order/01_prologue.md:25` `kotoba-remaining-review`
  - text: 并且能够共同拥有的美丽话语。」
- `bookish_zhcn/reading_order/01_prologue.md:232` `kotoba-remaining-review`
  - text: 远野十夜: 「然后，旅人少女对死神说道：‘我在寻找世界上最美的话语’」
- `bookish_zhcn/reading_order/01_prologue.md:233` `kotoba-remaining-review`
  - text: 远野纱夜: 「世界上最美的话语吗」
- `bookish_zhcn/reading_order/01_prologue.md:238` `kotoba-remaining-review`
  - text: 远野十夜: 「嗯……确实，‘爱’、‘希望’、‘和平’，我觉得都是很好的词语」
- `bookish_zhcn/reading_order/01_prologue.md:243` `kotoba-remaining-review`
  - text: 远野纱夜: 「所以，就不是美丽的词语吗？」
- `bookish_zhcn/reading_order/01_prologue.md:244` `kotoba-remaining-review`
  - text: 远野十夜: 「不，我觉得它们确实是美丽的词语」
- `bookish_zhcn/reading_order/01_prologue.md:263` `kotoba-remaining-review`
  - text: 远野十夜: 「这样的话语」
- `bookish_zhcn/reading_order/01_prologue.md:268` `kotoba-remaining-review`
  - text: 远野十夜: 「但是，在这个故事里，少女和死神为了寻找那样美好的话语，将要在世界上旅行一番旅程。」
- `bookish_zhcn/reading_order/01_prologue.md:285` `kotoba-remaining-review`
  - text: 远野纱夜: 「死神和旅人少女去寻找美好话语的那部分，感觉有种幻想色彩，非常吸引我。」
- `bookish_zhcn/reading_order/02_chapter1.md:2023` `kotoba-remaining-review`
  - text: 苍: 「一本叫《花之语言》的书。不过已经读完了」
- `bookish_zhcn/reading_order/02_chapter1.md:2054` `kotoba-remaining-review`
  - text: 远野纱夜: 「嗯。就是你刚才在读的《花之语言》」
- `bookish_zhcn/reading_order/02_chapter1.md:2713` `kotoba-remaining-review`
  - text: 我们像是忘记了语言一般，只是沉默着，眺望下方铺展开的景色。
- `bookish_zhcn/reading_order/02_chapter1.md:2788` `kotoba-remaining-review`
  - text: 连我自己都觉得不可思议，话语自然而然地就说了出来。
- `bookish_zhcn/reading_order/02_chapter1.md:2793` `kotoba-remaining-review`
  - text: 远野纱夜: 「是话语」
- `bookish_zhcn/reading_order/02_chapter1.md:2794` `kotoba-remaining-review`
  - text: 苍: 「话语？」
- `bookish_zhcn/reading_order/02_chapter1.md:2798` `kotoba-remaining-review`
  - text: 远野纱夜: 「这个世界很美。所以，我想寻找给这个世界增添色彩的话语」
- `bookish_zhcn/reading_order/02_chapter1.md:2803` `kotoba-remaining-review`
  - text: 远野纱夜: 「描绘这景色的词语就有这么多，一定还有更多、更多的，超出我现在能想到的词语吧」
- `bookish_zhcn/reading_order/02_chapter1.md:2804` `kotoba-remaining-review`
  - text: 远野纱夜: 「来寻找给这个世界增添色彩的话语吧」
- `bookish_zhcn/reading_order/02_chapter1.md:2805` `kotoba-remaining-review`
  - text: 远野纱夜: 「我想知道。那些美丽的话语」
- `bookish_zhcn/reading_order/02_chapter1.md:2813` `kotoba-remaining-review`
  - text: 远野纱夜: 「因为，没有话语的话，故事就不会诞生吧？」
- `bookish_zhcn/reading_order/02_chapter1.md:2823` `kotoba-remaining-review`
  - text: 苍: 「了解话语」
- 其余 237 条见 `*.review.jsonl`。

## 人工审核说明

- `*.operations.jsonl` 记录自动上下文修正，可逐条验收或回滚。
- `*.review.jsonl` 记录尚需人工或 LLM 精判的剩余候选。

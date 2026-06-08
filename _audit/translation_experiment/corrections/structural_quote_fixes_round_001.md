# Structural and quote fixes round 001

Scope:
- Removed dialogue wrappers only for reviewed high-confidence source narration lines.
- Replaced paired single quotes inside fully closed dialogue lines with 『』.
- Left mixed, unclosed, or source-shape-ambiguous quote cases for manual review.

Summary:
- dialogue_inner_single_quotes_to_kakko: 358
- source_unspeakered_dialogue_wrapper_removed: 119

By file:
- `appendix/endings_and_recovery.md`: dialogue_inner_single_quotes_to_kakko=39, source_unspeakered_dialogue_wrapper_removed=9
- `appendix/internal_stories.md`: dialogue_inner_single_quotes_to_kakko=7
- `reading_order/01_prologue.md`: dialogue_inner_single_quotes_to_kakko=31, source_unspeakered_dialogue_wrapper_removed=9
- `reading_order/02_chapter1.md`: dialogue_inner_single_quotes_to_kakko=36
- `reading_order/03_chapter2.md`: dialogue_inner_single_quotes_to_kakko=27, source_unspeakered_dialogue_wrapper_removed=54
- `reading_order/04_chapter3.md`: dialogue_inner_single_quotes_to_kakko=33, source_unspeakered_dialogue_wrapper_removed=10
- `reading_order/06_chapter4_to_hinase_branch.md`: dialogue_inner_single_quotes_to_kakko=1
- `reading_order/07_hinase_chapter4_branch.md`: dialogue_inner_single_quotes_to_kakko=2
- `reading_order/08_hinase.md`: dialogue_inner_single_quotes_to_kakko=32, source_unspeakered_dialogue_wrapper_removed=12
- `reading_order/09_chapter4_after_hinase_branch.md`: dialogue_inner_single_quotes_to_kakko=48
- `reading_order/11_kirishima_chapter5_branch.md`: dialogue_inner_single_quotes_to_kakko=1
- `reading_order/12_kirishima.md`: dialogue_inner_single_quotes_to_kakko=8
- `reading_order/13_chiyo_chapter5_branch.md`: dialogue_inner_single_quotes_to_kakko=1
- `reading_order/14_chiyo_kirishima_branch.md`: dialogue_inner_single_quotes_to_kakko=8
- `reading_order/15_chiyo.md`: dialogue_inner_single_quotes_to_kakko=2
- `reading_order/16_chapter5_after_kirichiyo_branch.md`: dialogue_inner_single_quotes_to_kakko=38, source_unspeakered_dialogue_wrapper_removed=12
- `reading_order/17_chapter6.md`: source_unspeakered_dialogue_wrapper_removed=13
- `reading_order/18_kuro.md`: dialogue_inner_single_quotes_to_kakko=16
- `reading_order/19_ao.md`: dialogue_inner_single_quotes_to_kakko=19
- `reading_order/20_atogaki.md`: dialogue_inner_single_quotes_to_kakko=9

Applied changes:

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:204`
- before: 千代: 「嗯。因为，那也能证明‘并非一无所有’，不是吗？」
- after: 千代: 「嗯。因为，那也能证明『并非一无所有』，不是吗？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:207`
- before: 千代: 「是的。因为，那也能证明‘并非一无所有’吧？」
- after: 千代: 「是的。因为，那也能证明『并非一无所有』吧？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:383`
- before: 远野十夜: 「笼中鸟总是哭啼啼的。‘我想出笼去’——这是笼中鸟的口头禅」
- after: 远野十夜: 「笼中鸟总是哭啼啼的。『我想出笼去』——这是笼中鸟的口头禅」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:447`
- before: 远野十夜: 「关于‘远野十夜’的下一部新作嘛……」
- after: 远野十夜: 「关于『远野十夜』的下一部新作嘛……」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:470`
- before: 远野纱夜: 「也就是说，每个人对‘死神’都有不同的理解方式？」
- after: 远野纱夜: 「也就是说，每个人对『死神』都有不同的理解方式？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:474`
- before: 远野十夜: 「‘死神’本身，说到底只是将‘死亡’拟人化的存在」
- after: 远野十夜: 「『死神』本身，说到底只是将『死亡』拟人化的存在」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:475`
- before: 远野十夜: 「对人来说最亲近却又看不见的存在——为了让人更容易理解‘死亡’这种东西，把它具体化之后就成了‘死神’」
- after: 远野十夜: 「对人来说最亲近却又看不见的存在——为了让人更容易理解『死亡』这种东西，把它具体化之后就成了『死神』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:476`
- before: 远野十夜: 「所以，这个‘死神’究竟是什么样的存在，就像纱夜说的，取决于如何处理它的人」
- after: 远野十夜: 「所以，这个『死神』究竟是什么样的存在，就像纱夜说的，取决于如何处理它的人」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:494`
- before: 远野纱夜: 「嗯……连我自己也不太明白，不过，听到‘死神’这个词并不觉得反感，也许是因为这个吧」
- after: 远野纱夜: 「嗯……连我自己也不太明白，不过，听到『死神』这个词并不觉得反感，也许是因为这个吧」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:495`
- before: 远野纱夜: 「就像哥哥说的，如果‘死神’不一定等同于我心目中的‘恶’，如果不讨厌的话，那不就是喜欢吗……」
- after: 远野纱夜: 「就像哥哥说的，如果『死神』不一定等同于我心目中的『恶』，如果不讨厌的话，那不就是喜欢吗……」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:509`
- before: 远野十夜: 「然后，旅人少女对死神说道：‘我在寻找世界上最美的话语’」
- after: 远野十夜: 「然后，旅人少女对死神说道：『我在寻找世界上最美的话语』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:515`
- before: 远野十夜: 「嗯……确实，‘爱’、‘希望’、‘和平’，我觉得都是很好的词语」
- after: 远野十夜: 「嗯……确实，『爱』、『希望』、『和平』，我觉得都是很好的词语」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:518`
- before: 远野十夜: 「‘爱’建立在‘欲望’之上，‘希望’没有‘绝望’就无法存在」
- after: 远野十夜: 「『爱』建立在『欲望』之上，『希望』没有『绝望』就无法存在」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:519`
- before: 远野十夜: 「‘和平’也一样，如果没有比较的对象，就无法感受到那是‘和平’」
- after: 远野十夜: 「『和平』也一样，如果没有比较的对象，就无法感受到那是『和平』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:523`
- before: 远野十夜: 「只是，对于不同的人来说，什么是‘正确的事’，什么是‘错误的事’，是不一样的」
- after: 远野十夜: 「只是，对于不同的人来说，什么是『正确的事』，什么是『错误的事』，是不一样的」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:657`
- before: 远野纱夜: 「……大家说的那个‘死神’吗？」
- after: 远野纱夜: 「……大家说的那个『死神』吗？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:659`
- before: 司书: 「毕竟被起了‘死神’这样的绰号嘛。对女孩子来说尤其危险吧。而且，远野小姐又是个美人，更容易被盯上哦～！」
- after: 司书: 「毕竟被起了『死神』这样的绰号嘛。对女孩子来说尤其危险吧。而且，远野小姐又是个美人，更容易被盯上哦～！」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:806`
- before: 远野纱夜: 「不由得想…‘这座时钟为什么会停了呢’……」
- after: 远野纱夜: 「不由得想…『这座时钟为什么会停了呢』……」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:849`
- before: ？？？: 「你刚才说了‘死神’吧」
- after: ？？？: 「你刚才说了『死神』吧」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:851`
- before: ？？？: 「不错，我就是‘死神’」
- after: ？？？: 「不错，我就是『死神』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:890`
- before: 远野纱夜: 「也是啊。这样想的话，您确实是‘死神’呢？」
- after: 远野纱夜: 「也是啊。这样想的话，您确实是『死神』呢？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:917`
- before: 远野纱夜: 「一开始我不就说过了吗？对于你是否可怕的问题，我回答了‘不’」
- after: 远野纱夜: 「一开始我不就说过了吗？对于你是否可怕的问题，我回答了『不』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:926`
- before: 远野纱夜: 「我是‘纱夜’。叫‘远野纱夜’」
- after: 远野纱夜: 「我是『纱夜』。叫『远野纱夜』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:939`
- before: ？？？: 「只是，记忆中只有自己是‘死神’这一点」
- after: ？？？: 「只是，记忆中只有自己是『死神』这一点」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:965`
- before: 远野纱夜: 「……那么，‘苍’怎么样？」
- after: 远野纱夜: 「……那么，『苍』怎么样？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:969`
- before: 远野纱夜: 「原本是颜色的名字。虽然‘苍’也有好几种」
- after: 远野纱夜: 「原本是颜色的名字。虽然『苍』也有好几种」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:977`
- before: ？？？: 「所以叫‘苍’？」
- after: ？？？: 「所以叫『苍』？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:984`
- before: ？？？: 「‘苍’吗……」
- after: ？？？: 「『苍』吗……」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:988`
- before: 苍: 「好吧。从现在起，我的名字就叫‘苍’了」
- after: 苍: 「好吧。从现在起，我的名字就叫『苍』了」

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:990`
- before: 远野纱夜: 「这里是位于尽头的东之国」
- after: 这里是位于尽头的东之国

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:991`
- before: 远野纱夜: 「一片苍色的天空」
- after: 一片苍色的天空

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:992`
- before: 远野纱夜: 「金发」
- after: 金发

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:993`
- before: 远野纱夜: 「黑发」
- after: 黑发

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:994`
- before: 远野纱夜: 「黑眸」
- after: 黑眸

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:995`
- before: 远野纱夜: 「苍眸」
- after: 苍眸

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:996`
- before: 远野纱夜: 「钟塔之下」
- after: 钟塔之下

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:997`
- before: 远野纱夜: 「那，仿佛童话一般」
- after: 那，仿佛童话一般

## source_unspeakered_dialogue_wrapper_removed — `appendix/endings_and_recovery.md:998`
- before: 远野纱夜: 「死神与少女相遇了」
- after: 死神与少女相遇了

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:1154`
- before: 远野十夜: 「而且，他自称自己是‘死神’，对吧？」
- after: 远野十夜: 「而且，他自称自己是『死神』，对吧？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:1315`
- before: 苍: 「‘under the rose’」
- after: 苍: 「『under the rose』」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:1320`
- before: 苍: 「据说，原本是人们在玫瑰下制定作战计划并取得胜利，因此拉丁语的‘sub rose’这个词开始被用作‘秘密’的意思」
- after: 苍: 「据说，原本是人们在玫瑰下制定作战计划并取得胜利，因此拉丁语的『sub rose』这个词开始被用作『秘密』的意思」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:1556`
- before: 远野纱夜: 「我哥哥是位叫‘远野十夜’的作家，然后，这位路易斯先生……」
- after: 远野纱夜: 「我哥哥是位叫『远野十夜』的作家，然后，这位路易斯先生……」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:2092`
- before: 千代: 「嗯。因为，那也能证明‘并非一无所有’，不是吗？」
- after: 千代: 「嗯。因为，那也能证明『并非一无所有』，不是吗？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:2095`
- before: 千代: 「是的。因为，那也能证明‘并非一无所有’吧？」
- after: 千代: 「是的。因为，那也能证明『并非一无所有』吧？」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:2259`
- before: 日生光: 「确实。俗话说‘亲密也要讲礼仪’嘛，在这个国家」
- after: 日生光: 「确实。俗话说『亲密也要讲礼仪』嘛，在这个国家」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:2579`
- before: 远野十夜: 「不管有多少扮演者，最后这个物语里的‘日生光’只有一个人」
- after: 远野十夜: 「不管有多少扮演者，最后这个物语里的『日生光』只有一个人」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:2580`
- before: 远野十夜: 「虽然我也不清楚到底哪个才是真正的‘日生光’，但比起相信言语，更应该找出无法说谎的东西」
- after: 远野十夜: 「虽然我也不清楚到底哪个才是真正的『日生光』，但比起相信言语，更应该找出无法说谎的东西」

## dialogue_inner_single_quotes_to_kakko — `appendix/endings_and_recovery.md:2589`
- before: 苍: 「嗯，是啊。首先，如果话语不可信，那么连‘日生光有两个人’这句话本身也不该相信吧」
- after: 苍: 「嗯，是啊。首先，如果话语不可信，那么连『日生光有两个人』这句话本身也不该相信吧」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:120`
- before: 「'持续'这件事，是美丽的语言吗？」
- after: 「『持续』这件事，是美丽的语言吗？」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:122`
- before: 「不。我所寻找的美丽语言，不是'持续'」
- after: 「不。我所寻找的美丽语言，不是『持续』」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:227`
- before: 「那么，‘世界’就不是最美的词语了吧」
- after: 「那么，『世界』就不是最美的词语了吧」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:300`
- before: 「‘自由’，那是一个美丽的词语吗？」
- after: 「『自由』，那是一个美丽的词语吗？」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:347`
- before: 「‘谎言’啊。那和美丽的词语不同吧」
- after: 「『谎言』啊。那和美丽的词语不同吧」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:348`
- before: 「是的。但是，我也不觉得‘谎言’一定不美」
- after: 「是的。但是，我也不觉得『谎言』一定不美」

## dialogue_inner_single_quotes_to_kakko — `appendix/internal_stories.md:408`
- before: 「强烈地向往，这就是‘憧憬’吗」
- after: 「强烈地向往，这就是『憧憬』吗」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:36`
- before: 远野十夜: 「笼中鸟总是哭啼啼的。‘我想出笼去’——这是笼中鸟的口头禅」
- after: 远野十夜: 「笼中鸟总是哭啼啼的。『我想出笼去』——这是笼中鸟的口头禅」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:169`
- before: 远野十夜: 「关于‘远野十夜’的下一部新作嘛……」
- after: 远野十夜: 「关于『远野十夜』的下一部新作嘛……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:192`
- before: 远野纱夜: 「也就是说，每个人对‘死神’都有不同的理解方式？」
- after: 远野纱夜: 「也就是说，每个人对『死神』都有不同的理解方式？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:196`
- before: 远野十夜: 「‘死神’本身，说到底只是将‘死亡’拟人化的存在」
- after: 远野十夜: 「『死神』本身，说到底只是将『死亡』拟人化的存在」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:197`
- before: 远野十夜: 「对人来说最亲近却又看不见的存在——为了让人更容易理解‘死亡’这种东西，把它具体化之后就成了‘死神’」
- after: 远野十夜: 「对人来说最亲近却又看不见的存在——为了让人更容易理解『死亡』这种东西，把它具体化之后就成了『死神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:198`
- before: 远野十夜: 「所以，这个‘死神’究竟是什么样的存在，就像纱夜说的，取决于如何处理它的人」
- after: 远野十夜: 「所以，这个『死神』究竟是什么样的存在，就像纱夜说的，取决于如何处理它的人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:217`
- before: 远野纱夜: 「嗯……连我自己也不太明白，不过，听到‘死神’这个词并不觉得反感，也许是因为这个吧」
- after: 远野纱夜: 「嗯……连我自己也不太明白，不过，听到『死神』这个词并不觉得反感，也许是因为这个吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:218`
- before: 远野纱夜: 「就像哥哥说的，如果‘死神’不一定等同于我心目中的‘恶’，如果不讨厌的话，那不就是喜欢吗……」
- after: 远野纱夜: 「就像哥哥说的，如果『死神』不一定等同于我心目中的『恶』，如果不讨厌的话，那不就是喜欢吗……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:232`
- before: 远野十夜: 「然后，旅人少女对死神说道：‘我在寻找世界上最美的话语’」
- after: 远野十夜: 「然后，旅人少女对死神说道：『我在寻找世界上最美的话语』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:238`
- before: 远野十夜: 「嗯……确实，‘爱’、‘希望’、‘和平’，我觉得都是很好的词语」
- after: 远野十夜: 「嗯……确实，『爱』、『希望』、『和平』，我觉得都是很好的词语」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:241`
- before: 远野十夜: 「‘爱’建立在‘欲望’之上，‘希望’没有‘绝望’就无法存在」
- after: 远野十夜: 「『爱』建立在『欲望』之上，『希望』没有『绝望』就无法存在」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:242`
- before: 远野十夜: 「‘和平’也一样，如果没有比较的对象，就无法感受到那是‘和平’」
- after: 远野十夜: 「『和平』也一样，如果没有比较的对象，就无法感受到那是『和平』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:246`
- before: 远野十夜: 「只是，对于不同的人来说，什么是‘正确的事’，什么是‘错误的事’，是不一样的」
- after: 远野十夜: 「只是，对于不同的人来说，什么是『正确的事』，什么是『错误的事』，是不一样的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:505`
- before: 班主任: 「虽然大家好像觉得好玩，把那人叫做‘死神’什么的，但可疑分子就是可疑分子」
- after: 班主任: 「虽然大家好像觉得好玩，把那人叫做『死神』什么的，但可疑分子就是可疑分子」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:637`
- before: 日生光: 「‘因为我喜欢你，想看看你那漂亮的身姿’……除此之外还需要别的理由吗？」
- after: 日生光: 「『因为我喜欢你，想看看你那漂亮的身姿』……除此之外还需要别的理由吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:680`
- before: 日生光: 「第一次见到你的时候，我心想‘这里有位公主’啊」
- after: 日生光: 「第一次见到你的时候，我心想『这里有位公主』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:683`
- before: 远野纱夜: 「……所以，才叫我‘小姐’？」
- after: 远野纱夜: 「……所以，才叫我『小姐』？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:781`
- before: 远野纱夜: 「……大家说的那个‘死神’吗？」
- after: 远野纱夜: 「……大家说的那个『死神』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:783`
- before: 图书管理员: 「毕竟被起了‘死神’这样的绰号嘛。对女孩子来说尤其危险吧。而且，远野小姐又是个美人，更容易被盯上哦～！」
- after: 图书管理员: 「毕竟被起了『死神』这样的绰号嘛。对女孩子来说尤其危险吧。而且，远野小姐又是个美人，更容易被盯上哦～！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:928`
- before: 远野纱夜: 「不由得想…‘这座时钟为什么会停了呢’……」
- after: 远野纱夜: 「不由得想…『这座时钟为什么会停了呢』……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:971`
- before: ？？？: 「你刚才说了‘死神’吧」
- after: ？？？: 「你刚才说了『死神』吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:973`
- before: ？？？: 「不错，我就是‘死神’」
- after: ？？？: 「不错，我就是『死神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1021`
- before: 远野纱夜: 「也是啊。这样想的话，您确实是‘死神’呢？」
- after: 远野纱夜: 「也是啊。这样想的话，您确实是『死神』呢？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1048`
- before: 远野纱夜: 「一开始我不就说过了吗？对于你是否可怕的问题，我回答了‘不’」
- after: 远野纱夜: 「一开始我不就说过了吗？对于你是否可怕的问题，我回答了『不』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1057`
- before: 远野纱夜: 「我是‘纱夜’。叫‘远野纱夜’」
- after: 远野纱夜: 「我是『纱夜』。叫『远野纱夜』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1070`
- before: ？？？: 「只是，记忆中只有自己是‘死神’这一点」
- after: ？？？: 「只是，记忆中只有自己是『死神』这一点」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1121`
- before: 远野纱夜: 「……那么，‘苍’怎么样？」
- after: 远野纱夜: 「……那么，『苍』怎么样？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1125`
- before: 远野纱夜: 「原本是颜色的名字。虽然‘苍’也有好几种」
- after: 远野纱夜: 「原本是颜色的名字。虽然『苍』也有好几种」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1133`
- before: ？？？: 「所以叫‘苍’？」
- after: ？？？: 「所以叫『苍』？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1140`
- before: ？？？: 「‘苍’吗……」
- after: ？？？: 「『苍』吗……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/01_prologue.md:1144`
- before: 苍: 「好吧。从现在起，我的名字就叫‘苍’了」
- after: 苍: 「好吧。从现在起，我的名字就叫『苍』了」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1146`
- before: 远野纱夜: 「这里是位于尽头的东之国」
- after: 这里是位于尽头的东之国

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1147`
- before: 远野纱夜: 「一片苍色的天空」
- after: 一片苍色的天空

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1148`
- before: 远野纱夜: 「金发」
- after: 金发

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1149`
- before: 远野纱夜: 「黑发」
- after: 黑发

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1150`
- before: 远野纱夜: 「黑眸」
- after: 黑眸

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1151`
- before: 远野纱夜: 「苍眸」
- after: 苍眸

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1152`
- before: 远野纱夜: 「时钟塔之下」
- after: 时钟塔之下

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1153`
- before: 远野纱夜: 「那，仿佛童话一般」
- after: 那，仿佛童话一般

## source_unspeakered_dialogue_wrapper_removed — `reading_order/01_prologue.md:1154`
- before: 远野纱夜: 「死神与少女相遇了」
- after: 死神与少女相遇了

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:10`
- before: 苍: 「给我取名为‘苍’的不是你吗？」
- after: 苍: 「给我取名为『苍』的不是你吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:15`
- before: 苍: 「我的名字是‘苍’。……对吧？」
- after: 苍: 「我的名字是『苍』。……对吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:18`
- before: 远野纱夜: 「……那，‘苍’」
- after: 远野纱夜: 「……那，『苍』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:133`
- before: 医生: 「嗯。……你还是和以前一样，总把‘哥哥、哥哥’挂在嘴边」
- after: 医生: 「嗯。……你还是和以前一样，总把『哥哥、哥哥』挂在嘴边」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:198`
- before: 远野纱夜: 「只记得自己是个‘死神’」
- after: 远野纱夜: 「只记得自己是个『死神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:249`
- before: 远野纱夜: 「然后，他还说‘你还是老样子啊’」
- after: 远野纱夜: 「然后，他还说『你还是老样子啊』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:251`
- before: 远野纱夜: 「他说，我每次叫‘哥哥’的时候，都显得很开心」
- after: 远野纱夜: 「他说，我每次叫『哥哥』的时候，都显得很开心」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:258`
- before: 远野十夜: 「不好吗？我很开心哦。能被纱夜叫‘哥哥’」
- after: 远野十夜: 「不好吗？我很开心哦。能被纱夜叫『哥哥』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:526`
- before: 远野纱夜: 「‘对’……你这个人，还是老样子这么不可思议呢……」
- after: 远野纱夜: 「『对』……你这个人，还是老样子这么不可思议呢……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:747`
- before: 远野纱夜: 「我遇到苍也是在时钟塔前面，而且他自己也自称‘死神’」
- after: 远野纱夜: 「我遇到苍也是在时钟塔前面，而且他自己也自称『死神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:847`
- before: ？？？: 「请问，这里有位叫‘远野纱夜’的人吗？」
- after: ？？？: 「请问，这里有位叫『远野纱夜』的人吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:852`
- before: ？？？: 「……啊，说不定你就是‘远野纱夜’小姐？」
- after: ？？？: 「……啊，说不定你就是『远野纱夜』小姐？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:867`
- before: ？？？: 「我认识你。你是‘苍’先生吧？」
- after: ？？？: 「我认识你。你是『苍』先生吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:1619`
- before: 远野十夜: 「而且，他自称自己是‘死神’，对吧？」
- after: 远野十夜: 「而且，他自称自己是『死神』，对吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2039`
- before: 远野纱夜: 「……你很喜欢用'理由'这个词呢」
- after: 远野纱夜: 「……你很喜欢用『理由』这个词呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2279`
- before: 远野纱夜: 「因为他是‘死神’吗？」
- after: 远野纱夜: 「因为他是『死神』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2281`
- before: 远野十夜: 「哈哈，不是啦。……只是你们两个单独出去，也就是说那是‘约会’吧？」
- after: 远野十夜: 「哈哈，不是啦。……只是你们两个单独出去，也就是说那是『约会』吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2404`
- before: 远野纱夜: 「呵呵。像这样同时采用和式和西洋式样，我们这边称之为‘和洋合璧’」
- after: 远野纱夜: 「呵呵。像这样同时采用和式和西洋式样，我们这边称之为『和洋合璧』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2549`
- before: 远野纱夜: 「呵呵。像这样同时采用和式和西洋式样，我们这边称之为‘和洋合璧’」
- after: 远野纱夜: 「呵呵。像这样同时采用和式和西洋式样，我们这边称之为『和洋合璧』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2731`
- before: 苍: 「大概，和人们所说的那种‘出生’的概念不同吧」
- after: 苍: 「大概，和人们所说的那种『出生』的概念不同吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2740`
- before: 远野纱夜: 「说到底，根本在于‘我就是我’吧」
- after: 远野纱夜: 「说到底，根本在于『我就是我』吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2741`
- before: 远野纱夜: 「有‘我’，才有‘你’。也就是说，存在‘个人’，才存在‘他人’吧」
- after: 远野纱夜: 「有『我』，才有『你』。也就是说，存在『个人』，才存在『他人』吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2827`
- before: 远野纱夜: 「你并不是‘神’」
- after: 远野纱夜: 「你并不是『神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2828`
- before: 远野纱夜: 「你是‘死神’」
- after: 远野纱夜: 「你是『死神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2972`
- before: 远野纱夜: 「你并不是‘神’」
- after: 远野纱夜: 「你并不是『神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:2973`
- before: 远野纱夜: 「你是‘死神’」
- after: 远野纱夜: 「你是『死神』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5670`
- before: 远野纱夜: 「然后，如果可以的话，直接去问‘老师’原因不就好了吗？」
- after: 远野纱夜: 「然后，如果可以的话，直接去问『老师』原因不就好了吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5913`
- before: 苍: 「当时存在于那里的，只是‘记忆’」
- after: 苍: 「当时存在于那里的，只是『记忆』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5932`
- before: 远野纱夜: 「那么，比起‘死者的语言’，用‘死者的回忆’来形容应该更贴切呢」
- after: 远野纱夜: 「那么，比起『死者的语言』，用『死者的回忆』来形容应该更贴切呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5935`
- before: 远野纱夜: 「……但如果是这样，那千代就不是那种‘幽灵’了吧」
- after: 远野纱夜: 「……但如果是这样，那千代就不是那种『幽灵』了吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5937`
- before: 桐岛七葵: 「所以我不是说了吗？‘大概就是这样吧’。况且，我刚才说的所有话也只不过是我的推测而已」
- after: 桐岛七葵: 「所以我不是说了吗？『大概就是这样吧』。况且，我刚才说的所有话也只不过是我的推测而已」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5941`
- before: 千代: 「不知不觉间，‘我’就存在了，在那之前到底有没有，连我自己也不知道」
- after: 千代: 「不知不觉间，『我』就存在了，在那之前到底有没有，连我自己也不知道」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:5950`
- before: 远野纱夜: 「是的。‘苍’这个名字也是我临时取的，并不是真名」
- after: 远野纱夜: 「是的。『苍』这个名字也是我临时取的，并不是真名」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:6139`
- before: 图书管理员: 「你当时说了什么‘太宰同学的姐姐’之类的话，但太宰巴同学是独生女。她没有姐姐。哎呀，我总觉得哪里不对劲嘛。啊哈哈……」
- after: 图书管理员: 「你当时说了什么『太宰同学的姐姐』之类的话，但太宰巴同学是独生女。她没有姐姐。哎呀，我总觉得哪里不对劲嘛。啊哈哈……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:6199`
- before: ？？？: 「智恵不也一直叫我‘老师’吗？」
- after: ？？？: 「智恵不也一直叫我『老师』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/02_chapter1.md:6200`
- before: ？？？: 「那是两码事。因为‘老师’就是‘老师’啊」
- after: ？？？: 「那是两码事。因为『老师』就是『老师』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:63`
- before: 远野纱夜: 「啊，用‘学习’这个说法不好呢。嗯……可以说是‘获取知识’？」
- after: 远野纱夜: 「啊，用『学习』这个说法不好呢。嗯……可以说是『获取知识』？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:250`
- before: 苍: 「‘under the rose’」
- after: 苍: 「『under the rose』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:255`
- before: 苍: 「据说，原本是人们在玫瑰下制定作战计划并取得胜利，因此拉丁语的‘sub rose’这个词开始被用作‘秘密’的意思」
- after: 苍: 「据说，原本是人们在玫瑰下制定作战计划并取得胜利，因此拉丁语的『sub rose』这个词开始被用作『秘密』的意思」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1121`
- before: 远野纱夜: 「很久很久以前，在西方某个村庄里的故事」
- after: 很久很久以前，在西方某个村庄里的故事

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1122`
- before: 远野纱夜: 「在那林边的村庄里，有一个爱做梦的」
- after: 在那林边的村庄里，有一个爱做梦的

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1123`
- before: 远野纱夜: 「男人」
- after: 男人

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1124`
- before: 远野纱夜: 「他有一头棕金色的头发和翡翠般的」
- after: 他有一头棕金色的头发和翡翠般的

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1125`
- before: 远野纱夜: 「拥有眼眸的那个男人的名字是路易斯」
- after: 拥有眼眸的那个男人的名字是路易斯

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1126`
- before: 远野纱夜: 「某天，他被一位黑裙少女」
- after: 某天，他被一位黑裙少女

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1127`
- before: 远野纱夜: 「邀请，前往一个不可思议的国度」
- after: 邀请，前往一个不可思议的国度

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1128`
- before: 远野纱夜: 「并误入了那里」
- after: 并误入了那里

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1129`
- before: 远野纱夜: 「像闪闪发光的宝石一样美丽的大海」
- after: 像闪闪发光的宝石一样美丽的大海

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1130`
- before: 远野纱夜: 「被蔷薇包围的巨大城堡」
- after: 被蔷薇包围的巨大城堡

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1131`
- before: 远野纱夜: 「那里如同令人心醉神迷般」
- after: 那里如同令人心醉神迷般

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:1132`
- before: 远野纱夜: 「是一个美丽的世界」
- after: 是一个美丽的世界

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:1207`
- before: 路易斯: 「你愿意让我见‘远野十夜’吗！？」
- after: 路易斯: 「你愿意让我见『远野十夜』吗！？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:1268`
- before: 路易斯: 「你愿意让我见‘远野十夜’吗！？」
- after: 路易斯: 「你愿意让我见『远野十夜』吗！？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:1656`
- before: 路易斯: 「你能不能告诉我关于‘远野十夜’的事？」
- after: 路易斯: 「你能不能告诉我关于『远野十夜』的事？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:1659`
- before: 路易斯: 「所以，我希望你能告诉我。创造出我的‘远野十夜’是个什么样的人」
- after: 路易斯: 「所以，我希望你能告诉我。创造出我的『远野十夜』是个什么样的人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:2240`
- before: 远野纱夜: 「我哥哥是位叫‘远野十夜’的作家，然后，这位路易斯先生……」
- after: 远野纱夜: 「我哥哥是位叫『远野十夜』的作家，然后，这位路易斯先生……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:2392`
- before: 远野纱夜: 「我哥哥是位叫‘远野十夜’的作家，然后，这位路易斯先生……」
- after: 远野纱夜: 「我哥哥是位叫『远野十夜』的作家，然后，这位路易斯先生……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:3358`
- before: 远野纱夜: 「所以说，这是心理作用。我觉得它像是一种‘仪式’」
- after: 远野纱夜: 「所以说，这是心理作用。我觉得它像是一种『仪式』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:3947`
- before: 桐岛七葵: 「‘是吗’……你这也太淡定了吧？不是得去找书的作者吗？」
- after: 桐岛七葵: 「『是吗』……你这也太淡定了吧？不是得去找书的作者吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4099`
- before: 苍: 「没错。所以我不是说过吗？‘那个男人不是路易斯’」
- after: 苍: 「没错。所以我不是说过吗？『那个男人不是路易斯』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4130`
- before: 远野纱夜: 「日生前辈和苍都说‘您不是路易斯’。我也明白这一点。您的确不是路易斯」
- after: 远野纱夜: 「日生前辈和苍都说『您不是路易斯』。我也明白这一点。您的确不是路易斯」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4131`
- before: 远野纱夜: 「但是，有件事我不明白。他们两个说您是‘想成为路易斯的人’」
- after: 远野纱夜: 「但是，有件事我不明白。他们两个说您是『想成为路易斯的人』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4213`
- before: 苍: 「你从一开始就知道。知道自己成不了‘主角’」
- after: 苍: 「你从一开始就知道。知道自己成不了『主角』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4242`
- before: 路易斯: 「就说‘我虽然喜欢你的作品，但那个结尾真是糟透了’」
- after: 路易斯: 「就说『我虽然喜欢你的作品，但那个结尾真是糟透了』」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4265`
- before: 路易斯: 「逐渐下沉的身体」
- after: 逐渐下沉的身体

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4266`
- before: 路易斯: 「伸出的手徒劳地空转着，」
- after: 伸出的手徒劳地空转着，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4267`
- before: 路易斯: 「逐渐连反抗的力气也消失了，」
- after: 逐渐连反抗的力气也消失了，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4268`
- before: 路易斯: 「最终沉了下去」
- after: 最终沉了下去

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4269`
- before: 路易斯: 「即使如此，罗莎依旧微微一笑，」
- after: 即使如此，罗莎依旧微微一笑，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4270`
- before: 路易斯: 「脸上挂着僵硬的笑容，一动不动」
- after: 脸上挂着僵硬的笑容，一动不动

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4271`
- before: 路易斯: 「红色的世界」
- after: 红色的世界

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4272`
- before: 路易斯: 「将所有一切都染上了那种颜色」
- after: 将所有一切都染上了那种颜色

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4273`
- before: 路易斯: 「然而，唯有她，」
- after: 然而，唯有她，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4274`
- before: 路易斯: 「只有她没有染上颜色，依旧保持黑色」
- after: 只有她没有染上颜色，依旧保持黑色

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4275`
- before: 路易斯: 「啊，多么美丽啊」
- after: 啊，多么美丽啊

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4276`
- before: 路易斯: 「路易斯心想」
- after: 路易斯心想

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4277`
- before: 路易斯: 「他的身体此刻已完全失去力气，」
- after: 他的身体此刻已完全失去力气，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4278`
- before: 路易斯: 「海水已经逼近到他的嘴边，」
- after: 海水已经逼近到他的嘴边，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4279`
- before: 路易斯: 「涌了上来」
- after: 涌了上来

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4280`
- before: 路易斯: 「将从未沾染任何颜色的她的身影，」
- after: 将从未沾染任何颜色的她的身影，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4281`
- before: 路易斯: 「烙印在绿色的眼眸中，」
- after: 烙印在绿色的眼眸中，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4282`
- before: 路易斯: 「他的记忆如同走马灯般飞驰，」
- after: 他的记忆如同走马灯般飞驰，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4283`
- before: 路易斯: 「一一闪过」
- after: 一一闪过

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4284`
- before: 路易斯: 「第一次见到的那座大城堡」
- after: 第一次见到的那座大城堡

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4285`
- before: 路易斯: 「那些从未见过的人们」
- after: 那些从未见过的人们

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4286`
- before: 路易斯: 「和猫贵族的威廉卿跳了舞」
- after: 和猫贵族的威廉卿跳了舞

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4287`
- before: 路易斯: 「曾经救下了一只爬上树后下不来」
- after: 曾经救下了一只爬上树后下不来

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4288`
- before: 路易斯: 「的小松鼠」
- after: 的小松鼠

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4289`
- before: 路易斯: 「美丽的世界，」
- after: 美丽的世界，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4290`
- before: 路易斯: 「欢迎自己的人们，」
- after: 欢迎自己的人们，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4291`
- before: 路易斯: 「令人目眩的种种冒险」
- after: 令人目眩的种种冒险

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4292`
- before: 路易斯: 「就这样，连从未见过的」
- after: 就这样，连从未见过的

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4293`
- before: 路易斯: 「大海也能够触及了」
- after: 大海也能够触及了

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4294`
- before: 路易斯: 「还有，罗莎。我见到了你」
- after: 还有，罗莎。我见到了你

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4295`
- before: 路易斯: 「全部都是这个世界里发生的事」
- after: 全部都是这个世界里发生的事

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4296`
- before: 路易斯: 「仅仅一天」
- after: 仅仅一天

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4297`
- before: 路易斯: 「在时间长河中仅仅是一瞬间的事」
- after: 在时间长河中仅仅是一瞬间的事

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4298`
- before: 路易斯: 「那正是他一直一直渴望的事」
- after: 那正是他一直一直渴望的事

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4301`
- source: `chapter2/chapter2_24.txt:324`
- before: 路易斯: 「路易斯笑了」
- after: 路易斯笑了

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4302`
- source: `chapter2/chapter2_24.txt:325`
- before: 路易斯: 「然后，终于消失在海底」
- after: 然后，终于消失在海底

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4387`
- before: 日生光: 「真寂寞啊。要是小姐说‘好寂寞’的话，我就会把你拐走然后直接私奔的」
- after: 日生光: 「真寂寞啊。要是小姐说『好寂寞』的话，我就会把你拐走然后直接私奔的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4530`
- before: 远野十夜: 「因为主人公在做‘梦’啊」
- after: 远野十夜: 「因为主人公在做『梦』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4551`
- before: 远野十夜: 「不过，作为故事的作者，唯一能说的是‘眼睛看到的东西并不代表一切’」
- after: 远野十夜: 「不过，作为故事的作者，唯一能说的是『眼睛看到的东西并不代表一切』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4557`
- before: 远野十夜: 「那就是‘故事与我’」
- after: 远野十夜: 「那就是『故事与我』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4558`
- before: 远野十夜: 「可以说，与‘故事’成对存在的就是‘我’吧」
- after: 远野十夜: 「可以说，与『故事』成对存在的就是『我』吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4559`
- before: 远野十夜: 「因为是这样吧？‘故事’因为有某个人的存在，才能作为‘故事’存在」
- after: 远野十夜: 「因为是这样吧？『故事』因为有某个人的存在，才能作为『故事』存在」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4562`
- before: 苍: 「这和‘眼睛看到的东西并不代表一切’有什么关系？」
- after: 苍: 「这和『眼睛看到的东西并不代表一切』有什么关系？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4563`
- before: 远野十夜: 「在自己的故事里成不了‘我’。因为自己的故事里自己是主角」
- after: 远野十夜: 「在自己的故事里成不了『我』。因为自己的故事里自己是主角」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4564`
- before: 远野十夜: 「归根结底，‘故事’如果不是‘某个人’的话，是无法阅读的」
- after: 远野十夜: 「归根结底，『故事』如果不是『某个人』的话，是无法阅读的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4586`
- before: 远野十夜: 「结论！说到底还是‘个人喜好’嘛」
- after: 远野十夜: 「结论！说到底还是『个人喜好』嘛」

## dialogue_inner_single_quotes_to_kakko — `reading_order/03_chapter2.md:4625`
- before: 桐岛七葵: 「……‘那就好’？意思是如果真欺负了，你还打算做点什么吗」
- after: 桐岛七葵: 「……『那就好』？意思是如果真欺负了，你还打算做点什么吗」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4781`
- before: 猎人C: 「森林深处可见荆棘之门」
- after: 森林深处可见荆棘之门

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4782`
- before: 猎人C: 「穿过那扇门，」
- after: 穿过那扇门，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4783`
- before: 猎人C: 「就能到达隐藏于其后的城堡」
- after: 就能到达隐藏于其后的城堡

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4784`
- before: 猎人C: 「白色终将化为红色」
- after: 白色终将化为红色

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4785`
- before: 猎人C: 「不可思议又不可思议的国度」
- after: 不可思议又不可思议的国度

## source_unspeakered_dialogue_wrapper_removed — `reading_order/03_chapter2.md:4786`
- before: 猎人C: 「在那里，鲜红鲜红的美丽蔷薇盛开」
- after: 在那里，鲜红鲜红的美丽蔷薇盛开

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:836`
- before: 远野纱夜: 「……你们知道吗？那只猫叫‘维尔・猫田’哦。好像是这条商店街的吉祥物」
- after: 远野纱夜: 「……你们知道吗？那只猫叫『维尔・猫田』哦。好像是这条商店街的吉祥物」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:3300`
- before: 远野纱夜: 「那个‘那时候’，是指你想起记忆的时候？」
- after: 远野纱夜: 「那个『那时候』，是指你想起记忆的时候？」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:3443`
- before: 夏目姐姐: 「我忘了？」
- after: 我忘了？

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:3444`
- before: 夏目姐姐: 「不，我没有忘」
- after: 不，我没有忘

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:3445`
- before: 夏目姐姐: 「是忘不掉的名字」
- after: 是忘不掉的名字

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:3563`
- before: 苍: 「你说的‘温柔’，如果只是关心他人的话，那我和‘温柔’恐怕不一样」
- after: 苍: 「你说的『温柔』，如果只是关心他人的话，那我和『温柔』恐怕不一样」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:3696`
- before: 远野十夜: 「但是，存在的并不只有‘我爱你’这种漂亮的话语」
- after: 远野十夜: 「但是，存在的并不只有『我爱你』这种漂亮的话语」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:3821`
- before: 夏目悠希: 「……哈。一口一个‘纱夜酱、纱夜酱’，你傻吗？」
- after: 夏目悠希: 「……哈。一口一个『纱夜酱、纱夜酱』，你傻吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:4164`
- before: 远野纱夜: 「我是‘远野’家的孩子」
- after: 远野纱夜: 「我是『远野』家的孩子」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:4204`
- before: 宫泽夏帆: 「为什么？‘对不起’」
- after: 宫泽夏帆: 「为什么？『对不起』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:4885`
- before: 宫泽夏帆: 「既然都到这里了，不就是所谓的‘上了贼船’吗？帮帮他吧！」
- after: 宫泽夏帆: 「既然都到这里了，不就是所谓的『上了贼船』吗？帮帮他吧！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5087`
- before: 苍: 「他已经说过谢谢了。而且还说‘明天还会再来’」
- after: 苍: 「他已经说过谢谢了。而且还说『明天还会再来』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5094`
- before: 日生光: 「‘明天还会再来’啊。难不成，他打算一直来这里？」
- after: 日生光: 「『明天还会再来』啊。难不成，他打算一直来这里？」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5158`
- before: 威廉: 「那天他也是同样从图书馆」
- after: 那天他也是同样从图书馆

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5159`
- before: 威廉: 「眺望着夏目同学的身影」
- after: 眺望着夏目同学的身影

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5160`
- before: 威廉: 「然后，到快下课时」
- after: 然后，到快下课时

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5161`
- before: 威廉: 「他就不知什么时候不见了」
- after: 他就不知什么时候不见了

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5162`
- before: 威廉: 「这并非仅限于昨天和今天」
- after: 这并非仅限于昨天和今天

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5163`
- before: 威廉: 「不仅如此，第二天，再第二天，他都」
- after: 不仅如此，第二天，再第二天，他都

## source_unspeakered_dialogue_wrapper_removed — `reading_order/04_chapter3.md:5164`
- before: 威廉: 「来学校眺望夏目同学的情况」
- after: 来学校眺望夏目同学的情况

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5442`
- before: 千代: 「嗯。因为，那也能证明‘并非一无所有’，不是吗？」
- after: 千代: 「嗯。因为，那也能证明『并非一无所有』，不是吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5445`
- before: 千代: 「是的。因为，那也能证明‘并非一无所有’吧？」
- after: 千代: 「是的。因为，那也能证明『并非一无所有』吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5653`
- before: 千代: 「嗯。因为，那也能证明‘并非一无所有’，不是吗？」
- after: 千代: 「嗯。因为，那也能证明『并非一无所有』，不是吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5656`
- before: 千代: 「是的。因为，那也能证明‘并非一无所有’吧？」
- after: 千代: 「是的。因为，那也能证明『并非一无所有』吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5867`
- before: 千代: 「嗯。因为，那也能证明‘并非一无所有’，不是吗？」
- after: 千代: 「嗯。因为，那也能证明『并非一无所有』，不是吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:5870`
- before: 千代: 「是的。因为，那也能证明‘并非一无所有’吧？」
- after: 千代: 「是的。因为，那也能证明『并非一无所有』吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6360`
- before: 远野纱夜: 「说起来，‘夏目的朋友’这句话，我们也只从威廉先生那里听过……」
- after: 远野纱夜: 「说起来，『夏目的朋友』这句话，我们也只从威廉先生那里听过……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6425`
- before: 远野纱夜: 「说起来，‘夏目的朋友’这句话，我们也只从威廉先生那里听过……」
- after: 远野纱夜: 「说起来，『夏目的朋友』这句话，我们也只从威廉先生那里听过……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6640`
- before: ？？？: 「他一定很吃惊吧。没想到有个和自己一模一样的人作为‘日生光’生活着」
- after: ？？？: 「他一定很吃惊吧。没想到有个和自己一模一样的人作为『日生光』生活着」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6648`
- before: ？？？: 「但眼前如果出现一个长相相同的人，至少会让人不得不信吧？‘有个人冒充日生光’这个童话」
- after: ？？？: 「但眼前如果出现一个长相相同的人，至少会让人不得不信吧？『有个人冒充日生光』这个童话」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6652`
- before: 日生光: 「我比他更出色地演出了日生紫所期望的理想‘日生光’。这一点，他平时看着我应该也明白了」
- after: 日生光: 「我比他更出色地演出了日生紫所期望的理想『日生光』。这一点，他平时看着我应该也明白了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6811`
- before: ？？？: 「他一定很吃惊吧。没想到有个和自己一模一样的人作为‘日生光’生活着」
- after: ？？？: 「他一定很吃惊吧。没想到有个和自己一模一样的人作为『日生光』生活着」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6819`
- before: ？？？: 「但眼前如果出现一个长相相同的人，至少会让人不得不信吧？‘有个人冒充日生光’这个童话」
- after: ？？？: 「但眼前如果出现一个长相相同的人，至少会让人不得不信吧？『有个人冒充日生光』这个童话」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:6823`
- before: 日生光: 「我比他更出色地演出了日生紫所期望的理想‘日生光’。这一点，他平时看着我应该也明白了」
- after: 日生光: 「我比他更出色地演出了日生紫所期望的理想『日生光』。这一点，他平时看着我应该也明白了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7073`
- before: 远野纱夜: 「他对我说：‘我绝不原谅’」
- after: 远野纱夜: 「他对我说：『我绝不原谅』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7640`
- before: 宫泽夏帆: 「不是‘你’，是夏帆！这边是纱夜！！要好好叫名字啊～」
- after: 宫泽夏帆: 「不是『你』，是夏帆！这边是纱夜！！要好好叫名字啊～」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7641`
- before: 宫泽夏帆: 「不是‘你’，是夏帆！她叫纱夜！！要好好叫名字啊～」
- after: 宫泽夏帆: 「不是『你』，是夏帆！她叫纱夜！！要好好叫名字啊～」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7795`
- before: 苍: 「……嗯。那么，也就是说‘朋友’也是一样的吗？」
- after: 苍: 「……嗯。那么，也就是说『朋友』也是一样的吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7797`
- before: 苍: 「朋友是肯定的感情。而威廉希望夏目幸福。说白了，祝愿对方幸福不就是‘朋友’吗？」
- after: 苍: 「朋友是肯定的感情。而威廉希望夏目幸福。说白了，祝愿对方幸福不就是『朋友』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7965`
- before: 宫泽夏帆: 「不是‘你’，是夏帆！这边是纱夜！！要好好叫名字啊～」
- after: 宫泽夏帆: 「不是『你』，是夏帆！这边是纱夜！！要好好叫名字啊～」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:7966`
- before: 宫泽夏帆: 「不是‘你’，是夏帆！她叫纱夜！！要好好叫名字啊～」
- after: 宫泽夏帆: 「不是『你』，是夏帆！她叫纱夜！！要好好叫名字啊～」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:8123`
- before: 苍: 「……嗯。那么，也就是说‘朋友’也是一样的吗？」
- after: 苍: 「……嗯。那么，也就是说『朋友』也是一样的吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/04_chapter3.md:8125`
- before: 苍: 「朋友是肯定的感情。而威廉希望夏目幸福。说白了，祝愿对方幸福不就是‘朋友’吗？」
- after: 苍: 「朋友是肯定的感情。而威廉希望夏目幸福。说白了，祝愿对方幸福不就是『朋友』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/06_chapter4_to_hinase_branch.md:859`
- before: 远野纱夜: 「请您转告他：‘如果您有事，不如您亲自过来一趟？’」
- after: 远野纱夜: 「请您转告他：『如果您有事，不如您亲自过来一趟？』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/07_hinase_chapter4_branch.md:229`
- before: 日生光: 「每次被提醒、被说‘不对’的时候，都觉得像是在否定自己」
- after: 日生光: 「每次被提醒、被说『不对』的时候，都觉得像是在否定自己」

## dialogue_inner_single_quotes_to_kakko — `reading_order/07_hinase_chapter4_branch.md:461`
- before: 日生光: 「确实。俗话说‘亲密也要讲礼仪’嘛，在这个国家」
- after: 日生光: 「确实。俗话说『亲密也要讲礼仪』嘛，在这个国家」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:20`
- before: 远野纱夜: 「终于，你叫了我的名字呢。明明一直叫‘小姐’的」
- after: 远野纱夜: 「终于，你叫了我的名字呢。明明一直叫『小姐』的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:21`
- before: 日生光: 「因为我们已经正式是恋人了吧？一直叫你‘小姐’也不像样子。讨厌吗？」
- after: 日生光: 「因为我们已经正式是恋人了吧？一直叫你『小姐』也不像样子。讨厌吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:218`
- before: 日生光: 「从早上开始就被缠着问个不停呢。问我是‘怎么拿下远野纱夜的’」
- after: 日生光: 「从早上开始就被缠着问个不停呢。问我是『怎么拿下远野纱夜的』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:221`
- before: 夏目悠希: 「那我就配合着气氛勉强问一句吧，‘你是怎么拿下的？’」
- after: 夏目悠希: 「那我就配合着气氛勉强问一句吧，『你是怎么拿下的？』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:286`
- before: 日生光: 「我会让你亲口说出‘喜欢’的哦？」
- after: 日生光: 「我会让你亲口说出『喜欢』的哦？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:305`
- before: 日生光: 「‘恋人该做的事’啊」
- after: 日生光: 「『恋人该做的事』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:546`
- before: 远野纱夜: 「自己做的食物，倒没觉得有那么‘好吃’呢」
- after: 远野纱夜: 「自己做的食物，倒没觉得有那么『好吃』呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:550`
- before: 远野纱夜: 「这就是所谓的‘外国的月亮比较圆’吗？」
- after: 远野纱夜: 「这就是所谓的『外国的月亮比较圆』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:551`
- before: 宫泽夏帆: 「你至少说一句‘因为我是想着某个人才做的’嘛～……」
- after: 宫泽夏帆: 「你至少说一句『因为我是想着某个人才做的』嘛～……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:552`
- before: 宫泽夏帆: 「你看～。不是说‘爱情是调味料’嘛～？」
- after: 宫泽夏帆: 「你看～。不是说『爱情是调味料』嘛～？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:765`
- before: 远野纱夜: 「可是，他第一次吃的时候还笑着说‘好吃’呢。之后也还想继续吃……」
- after: 远野纱夜: 「可是，他第一次吃的时候还笑着说『好吃』呢。之后也还想继续吃……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1705`
- before: 远野纱夜: 「比如说，如果我不是‘远野’，你还会喜欢我吗？」
- after: 远野纱夜: 「比如说，如果我不是『远野』，你还会喜欢我吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1746`
- before: 远野纱夜: 「你称我为‘远野纱夜’……我很高兴」
- after: 远野纱夜: 「你称我为『远野纱夜』……我很高兴」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1762`
- before: 日生光: 「第一次见到你时，觉得你像难以接近、美丽但一碰就碎的‘公主’」
- after: 日生光: 「第一次见到你时，觉得你像难以接近、美丽但一碰就碎的『公主』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1763`
- before: 日生光: 「聊了一会儿后，觉得你真是个货真价实的‘大小姐’」
- after: 日生光: 「聊了一会儿后，觉得你真是个货真价实的『大小姐』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1768`
- before: 日生光: 「实际上，是吧。有很多个‘远野纱夜’，但每一个都是‘远野纱夜’」
- after: 日生光: 「实际上，是吧。有很多个『远野纱夜』，但每一个都是『远野纱夜』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1769`
- before: 日生光: 「实际上，是吧。有很多个‘远野纱夜’，但每一个都是‘远野纱夜’，没有区别」
- after: 日生光: 「实际上，是吧。有很多个『远野纱夜』，但每一个都是『远野纱夜』，没有区别」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:1855`
- before: 日生光: 「就是啊。俗话说‘挡人姻缘’什么的嘛」
- after: 日生光: 「就是啊。俗话说『挡人姻缘』什么的嘛」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2558`
- before: 日生光: 「那样子我就永远地不再是‘我’了。那家伙成了真的，我倒成了假的」
- after: 日生光: 「那样子我就永远地不再是『我』了。那家伙成了真的，我倒成了假的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2559`
- before: 日生光: 「因为我又不像那家伙那么‘完美’」
- after: 日生光: 「因为我又不像那家伙那么『完美』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2560`
- before: 远野纱夜: 「‘完美’是什么意思啊！？」
- after: 远野纱夜: 「『完美』是什么意思啊！？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2566`
- before: 日生光: 「那种家伙待在我‘家’里，装成‘我’的样子生活……！！」
- after: 日生光: 「那种家伙待在我『家』里，装成『我』的样子生活……！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2577`
- before: 日生光: 「想出现，随时都能出现。只要我现身，就会有两个相同长相的人。这样一来，大家就只能相信‘有两个日生光’这个天方夜谭了」
- after: 日生光: 「想出现，随时都能出现。只要我现身，就会有两个相同长相的人。这样一来，大家就只能相信『有两个日生光』这个天方夜谭了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2579`
- before: 日生光: 「你说对吧？因为那家伙，可是完美地扮演了大家所期望的‘日生光’啊。要是没人相信我的话，反而认定我是冒牌货，那岂不得憋屈死」
- after: 日生光: 「你说对吧？因为那家伙，可是完美地扮演了大家所期望的『日生光』啊。要是没人相信我的话，反而认定我是冒牌货，那岂不得憋屈死」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2625`
- before: 日生光: 「我才是‘日生光’！！！」
- after: 日生光: 「我才是『日生光』！！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2631`
- before: 日生光: 「………可为什么！！为什么大家都注意不到啊！！难道这么不需要‘我’吗！？」
- after: 日生光: 「………可为什么！！为什么大家都注意不到啊！！难道这么不需要『我』吗！？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2632`
- before: 日生光: 「不完美的‘我’就不是‘我’了吗！！那从一开始‘日生光’就不存在才对啊！！」
- after: 日生光: 「不完美的『我』就不是『我』了吗！！那从一开始『日生光』就不存在才对啊！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2766`
- before: 远野纱夜: 「你真的不是‘日生光’吗……？」
- after: 远野纱夜: 「你真的不是『日生光』吗……？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2775`
- before: 远野纱夜: 「……我并不怎么了解正牌的‘日生光’」
- after: 远野纱夜: 「……我并不怎么了解正牌的『日生光』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2787`
- before: 日生光: 「因为你姓‘远野’啊」
- after: 日生光: 「因为你姓『远野』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:2788`
- before: 日生光: 「我接近你，也不是对你有兴趣，只是想要你背后的‘远野’这个地位而已」
- after: 日生光: 「我接近你，也不是对你有兴趣，只是想要你背后的『远野』这个地位而已」

## dialogue_inner_single_quotes_to_kakko — `reading_order/08_hinase.md:3138`
- before: 日生光: 「而且，那时候我说过吧？‘要不要把你带出去？’」
- after: 日生光: 「而且，那时候我说过吧？『要不要把你带出去？』」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3146`
- before: 日生光: 「被困在无门高塔里的公主」
- after: 被困在无门高塔里的公主

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3147`
- before: 日生光: 「爱上公主的王子，趁着先来到塔里的盗贼分心之际，」
- after: 爱上公主的王子，趁着先来到塔里的盗贼分心之际，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3148`
- before: 日生光: 「用魔法咒语到达了公主身边」
- after: 用魔法咒语到达了公主身边

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3149`
- before: 日生光: 「就这样，成功地赢得了公主的芳心」
- after: 就这样，成功地赢得了公主的芳心

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3150`
- before: 日生光: 「王子和公主偶尔会从塔上溜出去，」
- after: 王子和公主偶尔会从塔上溜出去，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3151`
- before: 日生光: 「但最后总是两个人，」
- after: 但最后总是两个人，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3152`
- before: 日生光: 「为了寻求自由而回到那座塔」
- after: 为了寻求自由而回到那座塔

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3153`
- before: 日生光: 「从今以后，两人或许会幸福地、」
- after: 从今以后，两人或许会幸福地、

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3154`
- before: 日生光: 「和睦共度漫长的时光」
- after: 和睦共度漫长的时光

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3155`
- before: 日生光: 「这还没有人知道」
- after: 这还没有人知道

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3156`
- before: 日生光: 「把公主关起来的魔女后来怎么样了呢？」
- after: 把公主关起来的魔女后来怎么样了呢？

## source_unspeakered_dialogue_wrapper_removed — `reading_order/08_hinase.md:3157`
- before: 日生光: 「没有人知道」
- after: 没有人知道

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:408`
- before: 日生光: 「每次被提醒、被说‘不对’的时候，都觉得像是在否定自己」
- after: 日生光: 「每次被提醒、被说『不对』的时候，都觉得像是在否定自己」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:694`
- before: 日生光: 「确实。俗话说‘亲密也要讲礼仪’嘛，在这个国家」
- after: 日生光: 「确实。俗话说『亲密也要讲礼仪』嘛，在这个国家」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2020`
- before: 远野纱夜: 「‘你们和日生光关系很好吧？那家伙是个骗子。’」
- after: 远野纱夜: 「『你们和日生光关系很好吧？那家伙是个骗子。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2090`
- before: 远野纱夜: 「‘你们和日生光关系很好吧？那家伙是个骗子。’」
- after: 远野纱夜: 「『你们和日生光关系很好吧？那家伙是个骗子。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2419`
- before: 远野纱夜: 「昨天傍晚，你把我带走了，说‘有话要跟我谈’」
- after: 远野纱夜: 「昨天傍晚，你把我带走了，说『有话要跟我谈』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2435`
- before: 日生光: 「我可没打算岔开话题。你问的是昨天傍晚有没有见过你们对吧？虽然我已经说了很多遍，但结论就是‘没见过’」
- after: 日生光: 「我可没打算岔开话题。你问的是昨天傍晚有没有见过你们对吧？虽然我已经说了很多遍，但结论就是『没见过』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2438`
- before: 日生光: 「就算你问我‘你是日生光吗’，我也只能是我；问我是不是「日生光」，我也只能回答是」
- after: 日生光: 「就算你问我『你是日生光吗』，我也只能是我；问我是不是「日生光」，我也只能回答是」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2481`
- before: 桐岛七葵: 「就像那家伙说的，如果‘日生光’是个说谎的人的话」
- after: 桐岛七葵: 「就像那家伙说的，如果『日生光』是个说谎的人的话」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2540`
- before: 桐岛七葵: 「就像那家伙说的，如果‘日生光’是个说谎的人的话」
- after: 桐岛七葵: 「就像那家伙说的，如果『日生光』是个说谎的人的话」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2602`
- before: 千代: 「只是听到‘樱’这个词……」
- after: 千代: 「只是听到『樱』这个词……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:2926`
- before: 苍: 「果然如此。如果只是‘告白’还能勉强说得通，但前面加上‘爱’的话，那就另当别论了」
- after: 苍: 「果然如此。如果只是『告白』还能勉强说得通，但前面加上『爱』的话，那就另当别论了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:3027`
- before: 苍: 「果然如此。如果只是‘告白’还能勉强说得通，但前面加上‘爱’的话，那就另当别论了」
- after: 苍: 「果然如此。如果只是『告白』还能勉强说得通，但前面加上『爱』的话，那就另当别论了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:3087`
- before: 千代: 「就是啊。这也没办法吧，平时总是说‘别把别人卷进来’的不是七葵君你吗」
- after: 千代: 「就是啊。这也没办法吧，平时总是说『别把别人卷进来』的不是七葵君你吗」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:3640`
- before: 苍: 「你这是在同情'祖母'那边？」
- after: 苍: 「你这是在同情『祖母』那边？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:3643`
- before: 日生光: 「母亲的照片几乎都被扔掉了，简直像在不停地喊着'不甘心不甘心'」
- after: 日生光: 「母亲的照片几乎都被扔掉了，简直像在不停地喊着『不甘心不甘心』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5011`
- before: 桐岛七葵: 「那家伙去追日生了……追那个自称‘真货’的家伙了」
- after: 桐岛七葵: 「那家伙去追日生了……追那个自称『真货』的家伙了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5044`
- before: 远野纱夜: 「不过，我弄清了一件事。‘日生光’似乎存在三个人」
- after: 远野纱夜: 「不过，我弄清了一件事。『日生光』似乎存在三个人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5045`
- before: 远野纱夜: 「正牌的‘日生光’、冒牌的‘日生光’、理想的‘日生光’……」
- after: 远野纱夜: 「正牌的『日生光』、冒牌的『日生光』、理想的『日生光』……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5051`
- before: 远野十夜: 「理想的‘日生光’吗。那是谁心目中的理想呢？」
- after: 远野十夜: 「理想的『日生光』吗。那是谁心目中的理想呢？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5054`
- before: 远野纱夜: 「据说存在一个理想的‘日生光’，而真货和假货都在分别扮演那个理想的‘日生光’」
- after: 远野纱夜: 「据说存在一个理想的『日生光』，而真货和假货都在分别扮演那个理想的『日生光』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5064`
- before: 远野十夜: 「不管有多少扮演者，最后这个物语里的‘日生光’只有一个人」
- after: 远野十夜: 「不管有多少扮演者，最后这个物语里的『日生光』只有一个人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5065`
- before: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- after: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的『日生光』，但比起相信话语，更应该找出无法说谎的东西」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5124`
- before: 远野纱夜: 「不过，我弄清了一件事。‘日生光’似乎存在三个人」
- after: 远野纱夜: 「不过，我弄清了一件事。『日生光』似乎存在三个人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5125`
- before: 远野纱夜: 「正牌的‘日生光’、冒牌的‘日生光’、理想的‘日生光’……」
- after: 远野纱夜: 「正牌的『日生光』、冒牌的『日生光』、理想的『日生光』……」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5131`
- before: 远野十夜: 「理想的‘日生光’吗。那是谁心目中的理想呢？」
- after: 远野十夜: 「理想的『日生光』吗。那是谁心目中的理想呢？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5134`
- before: 远野纱夜: 「据说存在一个理想的‘日生光’，而真货和假货都在分别扮演那个理想的‘日生光’」
- after: 远野纱夜: 「据说存在一个理想的『日生光』，而真货和假货都在分别扮演那个理想的『日生光』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5144`
- before: 远野十夜: 「不管有多少扮演者，最后这个物语里的‘日生光’只有一个人」
- after: 远野十夜: 「不管有多少扮演者，最后这个物语里的『日生光』只有一个人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5145`
- before: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- after: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的『日生光』，但比起相信话语，更应该找出无法说谎的东西」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5210`
- before: 远野纱夜: 「像‘爸爸’一样呢」
- after: 远野纱夜: 「像『爸爸』一样呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5237`
- before: 远野纱夜: 「……那个，可是为什么这就意味着‘你会变成这样’呢？」
- after: 远野纱夜: 「……那个，可是为什么这就意味着『你会变成这样』呢？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5250`
- before: 远野纱夜: 「我们多多少少比其他人更接近‘日生光’这个人。正因如此，光前辈才会对我们说那么多吧」
- after: 远野纱夜: 「我们多多少少比其他人更接近『日生光』这个人。正因如此，光前辈才会对我们说那么多吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5363`
- before: 远野十夜: 「不管有多少扮演者，最后这个物语里的‘日生光’只有一个人」
- after: 远野十夜: 「不管有多少扮演者，最后这个物语里的『日生光』只有一个人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5364`
- before: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- after: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的『日生光』，但比起相信话语，更应该找出无法说谎的东西」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5373`
- before: 苍: 「嗯，是啊。首先，如果话语不可信，那么连‘日生光有两个人’这句话本身也不该相信吧」
- after: 苍: 「嗯，是啊。首先，如果话语不可信，那么连『日生光有两个人』这句话本身也不该相信吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5444`
- before: 远野十夜: 「不管有多少扮演者，最后这个物语里的‘日生光’只有一个人」
- after: 远野十夜: 「不管有多少扮演者，最后这个物语里的『日生光』只有一个人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5445`
- before: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的‘日生光’，但比起相信话语，更应该找出无法说谎的东西」
- after: 远野十夜: 「虽然我也不清楚到底哪个才是正牌的『日生光』，但比起相信话语，更应该找出无法说谎的东西」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5454`
- before: 苍: 「嗯，是啊。首先，如果话语不可信，那么连‘日生光有两个人’这句话本身也不该相信吧」
- after: 苍: 「嗯，是啊。首先，如果话语不可信，那么连『日生光有两个人』这句话本身也不该相信吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5541`
- before: 千代: 「不是挺好吗？‘小七’多可爱啊？」
- after: 千代: 「不是挺好吗？『小七』多可爱啊？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5563`
- before: 日生光: 「名字明明是用来区分的，可被冒用了名字的我，还能算是‘真货’吗？」
- after: 日生光: 「名字明明是用来区分的，可被冒用了名字的我，还能算是『真货』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5616`
- before: 日生光: 「桐岛君要是不喜欢‘七葵’这个名字的话，那就给我吧」
- after: 日生光: 「桐岛君要是不喜欢『七葵』这个名字的话，那就给我吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5925`
- before: 远野纱夜: 「对已经看到结局的我来说，这个‘谎言’让我觉得无比悲伤」
- after: 远野纱夜: 「对已经看到结局的我来说，这个『谎言』让我觉得无比悲伤」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5942`
- before: 远野纱夜: 「如果在谎言中生活，它有一天会变成‘真相’吗？」
- after: 远野纱夜: 「如果在谎言中生活，它有一天会变成『真相』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:5943`
- before: 苍: 「故事是‘谎言’。但同时，故事也是‘真相’。这是为什么？因为故事是独一无二的」
- after: 苍: 「故事是『谎言』。但同时，故事也是『真相』。这是为什么？因为故事是独一无二的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:6836`
- before: 日生光: 「而且，也就是在那时候我明白了。从一开始，在奶奶眼里，‘日生光’这个人啊……根本就不是‘我’」
- after: 日生光: 「而且，也就是在那时候我明白了。从一开始，在奶奶眼里，『日生光』这个人啊……根本就不是『我』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:6838`
- before: 日生光: 「想出现，随时都能出现。只要我现身，就会有两个相同长相的人。这样一来，大家就只能相信‘有两个日生光’这个天方夜谭了」
- after: 日生光: 「想出现，随时都能出现。只要我现身，就会有两个相同长相的人。这样一来，大家就只能相信『有两个日生光』这个天方夜谭了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:6840`
- before: 日生光: 「你说对吧？因为那家伙，可是完美地扮演了大家所期望的‘日生光’啊。要是没人相信我的话，反而认定我是冒牌货，那岂不得憋屈死」
- after: 日生光: 「你说对吧？因为那家伙，可是完美地扮演了大家所期望的『日生光』啊。要是没人相信我的话，反而认定我是冒牌货，那岂不得憋屈死」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:7006`
- before: 日生光: 「‘远野纱夜’。莫非是新生？」
- after: 日生光: 「『远野纱夜』。莫非是新生？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/09_chapter4_after_hinase_branch.md:7010`
- before: 日生光: 「你是说‘公主’这个称呼？」
- after: 日生光: 「你是说『公主』这个称呼？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/11_kirishima_chapter5_branch.md:62`
- before: 远野纱夜: 「……说‘还’，其实那之后也没过多久」
- after: 远野纱夜: 「……说『还』，其实那之后也没过多久」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:215`
- before: 夏目悠希: 「就是那种‘请说明登场人物此刻的心理状态’、‘这个故事作者想传达什么’之类的问题。我每次都心想，我怎么知道啊」
- after: 夏目悠希: 「就是那种『请说明登场人物此刻的心理状态』、『这个故事作者想传达什么』之类的问题。我每次都心想，我怎么知道啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:1282`
- before: 日生光: 「结果，我无论是过去还是现在，都不得不扮演‘日生光’。至少这点宽容一下吧」
- after: 日生光: 「结果，我无论是过去还是现在，都不得不扮演『日生光』。至少这点宽容一下吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:1473`
- before: ？？？: 「别给我‘诶——’！这不是理所当然的吗！笨蛋！！」
- after: ？？？: 「别给我『诶——』！这不是理所当然的吗！笨蛋！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:1908`
- before: 桐岛七葵: 「不是‘这花’。是樱花。叫樱花」
- after: 桐岛七葵: 「不是『这花』。是樱花。叫樱花」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:1981`
- before: 远野纱夜: 「桐岛前辈总是说‘别担心’，我担心您会让您困扰吗？」
- after: 远野纱夜: 「桐岛前辈总是说『别担心』，我担心您会让您困扰吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:3115`
- before: 千代: 「虽然之前也这么叫过几次，但不知为什么总是下意识喊‘小姐’呢」
- after: 千代: 「虽然之前也这么叫过几次，但不知为什么总是下意识喊『小姐』呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:3354`
- before: 桐岛七葵: 「你的真实名字，是秋天绽放的樱花。‘秋樱’。对吧？」
- after: 桐岛七葵: 「你的真实名字，是秋天绽放的樱花。『秋樱』。对吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/12_kirishima.md:3361`
- before: 千代: 「正如七葵君所说。我终于明白了，自己的真面目。我是，开在这地方的‘秋樱’」
- after: 千代: 「正如七葵君所说。我终于明白了，自己的真面目。我是，开在这地方的『秋樱』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/13_chiyo_chapter5_branch.md:62`
- before: 远野纱夜: 「……说‘还’，其实那之后也没过多久」
- after: 远野纱夜: 「……说『还』，其实那之后也没过多久」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:215`
- before: 夏目悠希: 「就是那种‘请说明登场人物此刻的心理状态’、‘这个故事作者想传达什么’之类的问题。我每次都心想，我怎么知道啊」
- after: 夏目悠希: 「就是那种『请说明登场人物此刻的心理状态』、『这个故事作者想传达什么』之类的问题。我每次都心想，我怎么知道啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:1301`
- before: 日生光: 「结果，我无论是过去还是现在，都不得不扮演‘日生光’。至少这点宽容一下吧」
- after: 日生光: 「结果，我无论是过去还是现在，都不得不扮演『日生光』。至少这点宽容一下吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:1493`
- before: ？？？: 「别给我‘诶——’！这不是理所当然的吗！笨蛋！！」
- after: ？？？: 「别给我『诶——』！这不是理所当然的吗！笨蛋！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:1927`
- before: 桐岛七葵: 「不是‘这花’。是樱花。叫樱花」
- after: 桐岛七葵: 「不是『这花』。是樱花。叫樱花」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:2000`
- before: 远野纱夜: 「桐岛前辈总是说‘别担心’，我担心您会让您困扰吗？」
- after: 远野纱夜: 「桐岛前辈总是说『别担心』，我担心您会让您困扰吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:3153`
- before: 千代: 「虽然之前也这么叫过几次，但不知为什么总是下意识喊‘小姐’呢」
- after: 千代: 「虽然之前也这么叫过几次，但不知为什么总是下意识喊『小姐』呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:3392`
- before: 桐岛七葵: 「你的真实名字，是秋天绽放的樱花。‘秋樱’。对吧？」
- after: 桐岛七葵: 「你的真实名字，是秋天绽放的樱花。『秋樱』。对吧？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/14_chiyo_kirishima_branch.md:3399`
- before: 千代: 「正如七葵君所说。我终于明白了，自己的真面目。我是，开在这地方的‘秋樱’」
- after: 千代: 「正如七葵君所说。我终于明白了，自己的真面目。我是，开在这地方的『秋樱』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/15_chiyo.md:159`
- before: 远野纱夜: 「‘某种’是指什么？」
- after: 远野纱夜: 「『某种』是指什么？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/15_chiyo.md:166`
- before: 桐岛七葵: 「我好像没有坚强到能说出‘不寂寞’这种话」
- after: 桐岛七葵: 「我好像没有坚强到能说出『不寂寞』这种话」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:71`
- before: 远野纱夜: 「……说‘还’，其实那之后也没过多久」
- after: 远野纱夜: 「……说『还』，其实那之后也没过多久」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:649`
- before: 远野十夜: 「你不应该被‘我’这个存在束缚」
- after: 远野十夜: 「你不应该被『我』这个存在束缚」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:783`
- before: 远野十夜: 「你不应该被‘我’这个存在束缚」
- after: 远野十夜: 「你不应该被『我』这个存在束缚」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1377`
- before: 苍: 「原来如此。真的是字面意义上的‘装在容器里的面’啊」
- after: 苍: 「原来如此。真的是字面意义上的『装在容器里的面』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1407`
- before: 远野纱夜: 「啊，不过呢。如果想故意把味道调浓或调淡，稍微调节一下就是所谓的‘行家’做法」
- after: 远野纱夜: 「啊，不过呢。如果想故意把味道调浓或调淡，稍微调节一下就是所谓的『行家』做法」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1507`
- before: 远野纱夜: 「为什么呢？明知只是一本书，可我的内心在尖叫说‘不能打开这本书’」
- after: 远野纱夜: 「为什么呢？明知只是一本书，可我的内心在尖叫说『不能打开这本书』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1508`
- before: 远野纱夜: 「‘打开这本书，一切就结束了。’」
- after: 远野纱夜: 「『打开这本书，一切就结束了。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1509`
- before: 苍: 「为什么打开这本书就会结束？你说的‘结束’到底是指什么？」
- after: 苍: 「为什么打开这本书就会结束？你说的『结束』到底是指什么？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1520`
- before: 苍: 「如果‘有’是从‘无’中生出来的东西，那么‘有’变成‘无’也是理所当然的吧」
- after: 苍: 「如果『有』是从『无』中生出来的东西，那么『有』变成『无』也是理所当然的吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1521`
- before: 远野纱夜: 「‘无’真的存在吗？」
- after: 远野纱夜: 「『无』真的存在吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1523`
- before: 远野纱夜: 「我认为存在。但是，我不知道什么才算是‘无’」
- after: 远野纱夜: 「我认为存在。但是，我不知道什么才算是『无』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1524`
- before: 远野纱夜: 「说到底，‘无’到底是什么呢？那是我们能看见的东西吗？能确认其存在的东西吗？」
- after: 远野纱夜: 「说到底，『无』到底是什么呢？那是我们能看见的东西吗？能确认其存在的东西吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1526`
- before: 远野纱夜: 「是啊。那么，我稍微换个问题。‘结束’就是‘无’吗？」
- after: 远野纱夜: 「是啊。那么，我稍微换个问题。『结束』就是『无』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1607`
- before: 远野纱夜: 「为什么呢？明知只是一本书，可我的内心在尖叫说‘不能打开这本书’」
- after: 远野纱夜: 「为什么呢？明知只是一本书，可我的内心在尖叫说『不能打开这本书』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1608`
- before: 远野纱夜: 「‘打开这本书，一切就结束了。’」
- after: 远野纱夜: 「『打开这本书，一切就结束了。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1609`
- before: 苍: 「为什么打开这本书就会结束？你说的‘结束’到底是指什么？」
- after: 苍: 「为什么打开这本书就会结束？你说的『结束』到底是指什么？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1620`
- before: 苍: 「如果‘有’是从‘无’中生出来的东西，那么‘有’变成‘无’也是理所当然的吧」
- after: 苍: 「如果『有』是从『无』中生出来的东西，那么『有』变成『无』也是理所当然的吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1621`
- before: 远野纱夜: 「‘无’真的存在吗？」
- after: 远野纱夜: 「『无』真的存在吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1623`
- before: 远野纱夜: 「我认为存在。但是，我不知道什么才算是‘无’」
- after: 远野纱夜: 「我认为存在。但是，我不知道什么才算是『无』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1624`
- before: 远野纱夜: 「说到底，‘无’到底是什么呢？那是我们能看见的东西吗？能确认其存在的东西吗？」
- after: 远野纱夜: 「说到底，『无』到底是什么呢？那是我们能看见的东西吗？能确认其存在的东西吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:1626`
- before: 远野纱夜: 「是啊。那么，我稍微换个问题。‘结束’就是‘无’吗？」
- after: 远野纱夜: 「是啊。那么，我稍微换个问题。『结束』就是『无』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2730`
- before: 桐岛七葵: 「……‘是’说一次就够了」
- after: 桐岛七葵: 「……『是』说一次就够了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2809`
- before: 千代: 「啊，确实呢。爱是爱，两个的话就是‘爱爱’？感觉好奇怪啊」
- after: 千代: 「啊，确实呢。爱是爱，两个的话就是『爱爱』？感觉好奇怪啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2810`
- before: 远野纱夜: 「我想‘恩爱’这个说法是稍微改造了西方语言而来的」
- after: 远野纱夜: 「我想『恩爱』这个说法是稍微改造了西方语言而来的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2811`
- before: 远野纱夜: 「两个爱组成的‘爱爱’虽然奇怪，但如果看作是爱的平方，不就意味着更深地相爱吗？」
- after: 远野纱夜: 「两个爱组成的『爱爱』虽然奇怪，但如果看作是爱的平方，不就意味着更深地相爱吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2813`
- before: 远野纱夜: 「不过，‘恩爱’这个词本身可能是因为发音的关系，变成了比较轻松的说法，所以不仅用于男女之间的爱，也可以用来形容朋友之间关系亲密等」
- after: 远野纱夜: 「不过，『恩爱』这个词本身可能是因为发音的关系，变成了比较轻松的说法，所以不仅用于男女之间的爱，也可以用来形容朋友之间关系亲密等」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2897`
- before: 远野纱夜: 「只是，我没办法坦率地说出‘我很开心’」
- after: 远野纱夜: 「只是，我没办法坦率地说出『我很开心』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2914`
- before: 千代: 「如果说‘您像樱花一样’，小姐您会坦率地高兴吗？」
- after: 千代: 「如果说『您像樱花一样』，小姐您会坦率地高兴吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:2985`
- before: 千代: 「对方不理解自己的心情，真的很伤心对吧。会感到愤慨：‘为什么就是不明白呢！’」
- after: 千代: 「对方不理解自己的心情，真的很伤心对吧。会感到愤慨：『为什么就是不明白呢！』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3006`
- before: 苍: 「千代，我再问你一次。为什么你能理解纱夜那些‘没说出口的话’？」
- after: 苍: 「千代，我再问你一次。为什么你能理解纱夜那些『没说出口的话』？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3018`
- before: 远野纱夜: 「温柔的人会为他人着想。通常这被称为‘体谅’呢」
- after: 远野纱夜: 「温柔的人会为他人着想。通常这被称为『体谅』呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3026`
- before: 远野纱夜: 「我想，应该是‘没理解’才对」
- after: 远野纱夜: 「我想，应该是『没理解』才对」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3038`
- before: 千代: 「我想，我并没有完全理解小姐。准确地说，或许应该是‘想要理解’吧」
- after: 千代: 「我想，我并没有完全理解小姐。准确地说，或许应该是『想要理解』吧」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3528`
- before: 桐岛七葵: 「……远野。‘能看见’并不等同于‘正确’」
- after: 桐岛七葵: 「……远野。『能看见』并不等同于『正确』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3529`
- before: 远野纱夜: 「‘正确’？」
- after: 远野纱夜: 「『正确』？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3530`
- before: 远野纱夜: 「您所说的‘正确’是什么？是指看不见千代这件事吗？」
- after: 远野纱夜: 「您所说的『正确』是什么？是指看不见千代这件事吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3532`
- before: 远野纱夜: 「那这个‘正确’的判断是谁下的？以什么为标准，又是如何判断对错的？」
- after: 远野纱夜: 「那这个『正确』的判断是谁下的？以什么为标准，又是如何判断对错的？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/16_chapter5_after_kirichiyo_branch.md:3563`
- before: 苍: 「但是，如果必须做出判断的时刻到来，那么大多数人的话就会成为‘正确’吧」
- after: 苍: 「但是，如果必须做出判断的时刻到来，那么大多数人的话就会成为『正确』吧」

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3956`
- source: `chapter5/chapter5_48.txt:75`
- before: 苍: 「春与秋」
- after: 春与秋

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3957`
- source: `chapter5/chapter5_48.txt:76`
- before: 苍: 「樱与 」
- after: 樱与

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3958`
- source: `chapter5/chapter5_48.txt:77`
- before: 苍: 「永远无法相会的两种花」
- after: 永远无法相会的两种花

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3959`
- source: `chapter5/chapter5_48.txt:78`
- before: 苍: 「我用无声的声音说道」
- after: 我用无声的声音说道

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3964`
- source: `chapter5/chapter5_48.txt:83`
- before: 苍: 「即便如此 的花仍摇曳着自身」
- after: 即便如此 的花仍摇曳着自身

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3965`
- source: `chapter5/chapter5_48.txt:84`
- before: 苍: 「只为哪怕一次能见到春樱，一心一意」
- after: 只为哪怕一次能见到春樱，一心一意

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3966`
- source: `chapter5/chapter5_48.txt:85`
- before: 苍: 「春与秋」
- after: 春与秋

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3967`
- source: `chapter5/chapter5_48.txt:86`
- before: 苍: 「樱与 」
- after: 樱与

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3968`
- source: `chapter5/chapter5_48.txt:87`
- before: 苍: 「纵使时光流转千代万代」
- after: 纵使时光流转千代万代

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3969`
- source: `chapter5/chapter5_48.txt:88`
- before: 苍: 「两种花也绝不相交」
- after: 两种花也绝不相交

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3970`
- source: `chapter5/chapter5_48.txt:89`
- before: 苍: 「啊。明明都是樱，为何如此不同？」
- after: 啊。明明都是樱，为何如此不同？

## source_unspeakered_dialogue_wrapper_removed — `reading_order/16_chapter5_after_kirichiyo_branch.md:3971`
- source: `chapter5/chapter5_48.txt:90`
- before: 苍: 「啊。为何这可怜之花的愿望无法实现？」
- after: 啊。为何这可怜之花的愿望无法实现？

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:553`
- before: 远野纱夜: 「啊，小小的公主在痛苦」
- after: 啊，小小的公主在痛苦

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:554`
- before: 远野纱夜: 「谁来，谁来救救她。救救这个可怜的公主」
- after: 谁来，谁来救救她。救救这个可怜的公主

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:555`
- before: 远野纱夜: 「只要能让她们幸福，不是王子也没关系」
- after: 只要能让她们幸福，不是王子也没关系

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:556`
- before: 远野纱夜: 「请把她从魔女的手中救出来吧」
- after: 请把她从魔女的手中救出来吧

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:883`
- before: 少女: 「映照出任何东西了」
- after: 映照出任何东西了

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:884`
- before: 少女: 「少女也已经不会张开那形状优美的嘴唇，」
- after: 少女也已经不会张开那形状优美的嘴唇，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:885`
- before: 少女: 「发出任何话语了」
- after: 发出任何话语了

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:886`
- before: 少女: 「少女的眼中甚至连一丝光芒，」
- after: 少女的眼中甚至连一丝光芒，

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:887`
- before: 少女: 「耳中也听不到任何声响了」
- after: 耳中也听不到任何声响了

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:888`
- before: 少女: 「少女的物语将不会再被续写下去」
- after: 少女的物语将不会再被续写下去

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:889`
- before: 少女: 「正因为被死神迷住，少女才将自己的时间」
- after: 正因为被死神迷住，少女才将自己的时间

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:890`
- before: 少女: 「停止，不让它再继续前进」
- after: 停止，不让它再继续前进

## source_unspeakered_dialogue_wrapper_removed — `reading_order/17_chapter6.md:891`
- before: 少女: 「就这样，死神与少女两人」
- after: 就这样，死神与少女两人

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:522`
- before: 远野十夜: 「老是叫着‘哥哥、哥哥’」
- after: 远野十夜: 「老是叫着『哥哥、哥哥』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:620`
- before: 远野纱夜: 「夏帆能看到‘这个’吗？」
- after: 远野纱夜: 「夏帆能看到『这个』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:623`
- before: 宫泽夏帆: 「什么～？‘这个’？‘这个’是什么？」
- after: 宫泽夏帆: 「什么～？『这个』？『这个』是什么？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:659`
- before: 桐岛七葵: 「你，能看到‘这个’吗？」
- after: 桐岛七葵: 「你，能看到『这个』吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:693`
- before: 桐岛七葵: 「……那么，是从什么时候开始的。能看到‘这个’」
- after: 桐岛七葵: 「……那么，是从什么时候开始的。能看到『这个』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:1119`
- before: 白猫: 「我只是看不惯她那副'我和你们不一样'的隔阂。好像在瞧不起人一样」
- after: 白猫: 「我只是看不惯她那副『我和你们不一样』的隔阂。好像在瞧不起人一样」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:1190`
- before: 远野纱夜: 「还有，哥哥，我可不叫'你'哦」
- after: 远野纱夜: 「还有，哥哥，我可不叫『你』哦」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2645`
- before: 苍: 「死神就是‘终结’。我想成为‘终结’。仅此而已」
- after: 苍: 「死神就是『终结』。我想成为『终结』。仅此而已」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2660`
- before: 苍: 「可‘远野纱夜’未必如此」
- after: 苍: 「可『远野纱夜』未必如此」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2661`
- before: 苍: 「即使对你来说‘远野纱夜’就是一切，也不代表‘远野纱夜’会永远需要你」
- after: 苍: 「即使对你来说『远野纱夜』就是一切，也不代表『远野纱夜』会永远需要你」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2668`
- before: 远野十夜: 「因为‘远野十夜’……我……就是为了她而存在的」
- after: 远野十夜: 「因为『远野十夜』……我……就是为了她而存在的」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2838`
- before: 远野纱夜: 「所以就叫‘十夜’吧。姓氏用我的。你的名字就是‘远野十夜’。怎么样？」
- after: 远野纱夜: 「所以就叫『十夜』吧。姓氏用我的。你的名字就是『远野十夜』。怎么样？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2842`
- before: 远野十夜: 「我是‘远野十夜’啊」
- after: 远野十夜: 「我是『远野十夜』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:2843`
- before: 远野纱夜: 「对。‘十夜哥哥’」
- after: 远野纱夜: 「对。『十夜哥哥』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:3175`
- before: 十夜: 「我发现了。我已经不再是‘死神’了」
- after: 十夜: 「我发现了。我已经不再是『死神』了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/18_kuro.md:3176`
- before: 十夜: 「嗯，我知道。而且，我也不再是‘公主’或‘少女’了」
- after: 十夜: 「嗯，我知道。而且，我也不再是『公主』或『少女』了」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:850`
- before: 远野纱夜: 「千代的真实身份，难道……就是‘秋樱’花吗？」
- after: 远野纱夜: 「千代的真实身份，难道……就是『秋樱』花吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:866`
- before: 远野纱夜: 「是啊……结果，终究还是‘终结’，这一点没有改变」
- after: 远野纱夜: 「是啊……结果，终究还是『终结』，这一点没有改变」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:879`
- before: 苍: 「我可以断言：‘不是。’」
- after: 苍: 「我可以断言：『不是。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:898`
- before: 远野纱夜: 「……你所说的‘挂心’，是指什么呢？」
- after: 远野纱夜: 「……你所说的『挂心』，是指什么呢？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1085`
- before: 远野十夜: 「关于这件事，我甚至要感谢你。‘谢谢’」
- after: 远野十夜: 「关于这件事，我甚至要感谢你。『谢谢』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1143`
- before: 卧待春夫: 「所以，你就全盘接受了那句‘不要接近她’的话吗？」
- after: 卧待春夫: 「所以，你就全盘接受了那句『不要接近她』的话吗？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1212`
- before: 远野十夜: 「……答案是‘是’」
- after: 远野十夜: 「……答案是『是』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1242`
- before: 苍: 「我可以断言：‘不是。’」
- after: 苍: 「我可以断言：『不是。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1582`
- before: 远野纱夜: 「哥哥就是哥哥。十夜哥哥。‘远野十夜’啊」
- after: 远野纱夜: 「哥哥就是哥哥。十夜哥哥。『远野十夜』啊」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1587`
- before: 父亲: 「什么相信不相信，根本就不存在什么‘远野十夜’！！」
- after: 父亲: 「什么相信不相信，根本就不存在什么『远野十夜』！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1599`
- before: 远野纱夜: 「哥哥是我的哥哥……是‘远野十夜’！！」
- after: 远野纱夜: 「哥哥是我的哥哥……是『远野十夜』！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1604`
- before: 远野纱夜: 「请说‘是的’！！！！！」
- after: 远野纱夜: 「请说『是的』！！！！！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:1620`
- before: 远野十夜: 「我是你说的‘远野十夜’！」
- after: 远野十夜: 「我是你说的『远野十夜』！」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:2084`
- before: 日生光: 「我更希望你说我‘顽强’呢」
- after: 日生光: 「我更希望你说我『顽强』呢」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:3699`
- before: 远野十夜: 「啊，是的。然后，我与你在一起的过程中，不再是作为死神，而是作为‘远野十夜’活了下来」
- after: 远野十夜: 「啊，是的。然后，我与你在一起的过程中，不再是作为死神，而是作为『远野十夜』活了下来」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:3842`
- before: 卧待春夫: 「11点是12点，直到明天来临之前，今天最后的时光。45分钟是‘四十五’，写成汉字就是‘死期’」
- after: 卧待春夫: 「11点是12点，直到明天来临之前，今天最后的时光。45分钟是『四十五』，写成汉字就是『死期』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:4496`
- before: 远野纱夜: 「我可以断言：‘不是这样的。’」
- after: 远野纱夜: 「我可以断言：『不是这样的。』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:4746`
- before: 远野纱夜: 「一开始我不就说过了吗？对于你是否可怕的问题，我回答了‘不’」
- after: 远野纱夜: 「一开始我不就说过了吗？对于你是否可怕的问题，我回答了『不』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/19_ao.md:4849`
- before: 苍: 「我一开始觉得‘那种东西不可能存在’。是极其离谱、不着边际的事」
- after: 苍: 「我一开始觉得『那种东西不可能存在』。是极其离谱、不着边际的事」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:6`
- before: 卧待春夫: 「是吗。那我现在去准备茶吧。看来这话会很长呢。……‘桐岛七葵’君？」
- after: 卧待春夫: 「是吗。那我现在去准备茶吧。看来这话会很长呢。……『桐岛七葵』君？」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:11`
- before: 桐岛七葵: 「……我注意到你的存在，是在调查‘远野纱夜’的时候」
- after: 桐岛七葵: 「……我注意到你的存在，是在调查『远野纱夜』的时候」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:15`
- before: 桐岛七葵: 「‘远野纱夜’并没有一个叫‘远野十夜’的哥哥」
- after: 桐岛七葵: 「『远野纱夜』并没有一个叫『远野十夜』的哥哥」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:17`
- before: 桐岛七葵: 「我能看到‘远野十夜’」
- after: 桐岛七葵: 「我能看到『远野十夜』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:18`
- before: 卧待春夫: 「是啊。这个世界上能看到他的，只有你、‘远野纱夜’和‘伊利亚・尼古拉耶维奇・梅什金’三人」
- after: 卧待春夫: 「是啊。这个世界上能看到他的，只有你、『远野纱夜』和『伊利亚・尼古拉耶维奇・梅什金』三人」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:26`
- before: 卧待春夫: 「那是当然。因为在她心中，‘远野十夜’是绝对存在的。她不会听你的话」
- after: 卧待春夫: 「那是当然。因为在她心中，『远野十夜』是绝对存在的。她不会听你的话」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:27`
- before: 桐岛七葵: 「但是，实际上‘远野十夜’并不存在。是她描绘的幻想」
- after: 桐岛七葵: 「但是，实际上『远野十夜』并不存在。是她描绘的幻想」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:189`
- before: 卧待春夫: 「她真是个妖女。是个人见人爱的‘公主殿下’」
- after: 卧待春夫: 「她真是个妖女。是个人见人爱的『公主殿下』」

## dialogue_inner_single_quotes_to_kakko — `reading_order/20_atogaki.md:198`
- before: 桐岛七葵: 「虽然我觉得作家‘远野十夜’的故事不怎么样，不过，倒也不坏」
- after: 桐岛七葵: 「虽然我觉得作家『远野十夜』的故事不怎么样，不过，倒也不坏」

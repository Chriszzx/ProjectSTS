import tempfile
import unittest
import shutil
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.honorific_guideline_apply import apply_honorific_guidelines


class HonorificGuidelineApplyTests(unittest.TestCase):
    def test_applies_strategy_table_with_japanese_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ja_dir = root / "bookish" / "reading_order"
            zh_dir = root / "bookish_zhcn" / "reading_order"
            ja_dir.mkdir(parents=True)
            zh_dir.mkdir(parents=True)
            ja_path = ja_dir / "sample.md"
            zh_path = zh_dir / "sample.md"

            ja_path.write_text(
                "\n".join(
                    [
                        "遠野　紗夜: 「日生先輩」",
                        "昨日、光さんは笑った。",
                        "千代: 「お嬢さん！」",
                        "千代: 「お、お嬢さん？」",
                        "遠野　紗夜: 「千代さん」",
                        "臥待 春夫: 「紗夜ちゃん」",
                        "宮沢 夏帆: 「紗夜ちゃん」",
                        "日生 光: 「お嬢」",
                        "千代: 「紗夜さん」",
                        "千代: 「紗夜、さん？」",
                        "家政婦: 「紗夜お嬢様」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            zh_path.write_text(
                "\n".join(
                    [
                        "远野纱夜: 「日生学长」",
                        "昨天，光先生笑了。",
                        "千代: 「大小姐！」",
                        "千代: 「大、大小姐？」",
                        "远野纱夜: 「千代先生」",
                        "卧待春夫: 「纱夜酱」",
                        "宫泽夏帆: 「纱夜酱」",
                        "日生光: 「大小姐」",
                        "千代: 「纱夜小姐」",
                        "千代: 「纱夜、小姐？」",
                        "家政妇: 「纱夜大小姐」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("远野纱夜: 「日生前辈」", text)
            self.assertIn("昨天，光笑了。", text)
            self.assertIn("千代: 「小姐！」", text)
            self.assertIn("千代: 「小、小姐？」", text)
            self.assertIn("远野纱夜: 「千代」", text)
            self.assertIn("卧待春夫: 「小纱夜」", text)
            self.assertIn("宫泽夏帆: 「纱夜酱」", text)
            self.assertIn("日生光: 「小姐」", text)
            self.assertIn("千代: 「纱夜」", text)
            self.assertIn("千代: 「纱夜？」", text)
            self.assertIn("家政妇: 「纱夜大小姐」", text)

            self.assertEqual(
                [change.rule_id for change in changes],
                [
                    "hinase-senpai",
                    "hikari-san-private",
                    "chiyo-ojousan",
                    "chiyo-ojousan",
                    "sayo-to-chiyo-san",
                    "gashomachi-to-sayo-chan",
                    "hikari-ojo",
                    "chiyo-sayo-san",
                    "chiyo-sayo-san",
                ],
            )

    def test_uses_speaker_anchors_when_zh_has_extra_navigation_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ja_dir = root / "bookish" / "reading_order"
            zh_dir = root / "bookish_zhcn" / "reading_order"
            ja_dir.mkdir(parents=True)
            zh_dir.mkdir(parents=True)
            ja_path = ja_dir / "sample.md"
            zh_path = zh_dir / "sample.md"

            ja_path.write_text(
                "\n".join(
                    [
                        "遠野　紗夜: 「少し待ってください」",
                        "日生先輩は、不思議そうにこちらを見る。",
                        "日生 光: 「お嬢」",
                        "宮沢 夏帆: 「あ、七葵先輩だ」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            zh_path.write_text(
                "\n".join(
                    [
                        "远野纱夜: 「请稍等一下」",
                        "> 继续阅读",
                        "日生学长一脸不可思议地看着这边。",
                        "日生光: 「大小姐」",
                        "宫泽夏帆: 「啊，是七葵前辈」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("日生前辈一脸不可思议地看着这边。", text)
            self.assertIn("日生光: 「小姐」", text)
            self.assertIn("宫泽夏帆: 「啊，是七葵前辈」", text)
            self.assertEqual(
                [change.rule_id for change in changes],
                ["hinase-senpai", "hikari-ojo"],
            )

    def test_keeps_hikari_self_instruction_and_hinase_senpai_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ja_dir = root / "bookish" / "reading_order"
            zh_dir = root / "bookish_zhcn" / "reading_order"
            ja_dir.mkdir(parents=True)
            zh_dir.mkdir(parents=True)
            ja_path = ja_dir / "sample.md"
            zh_path = zh_dir / "sample.md"

            ja_path.write_text(
                "\n".join(
                    [
                        "日生 光: 「光さん。でなきゃ、光先輩って呼んでよ」",
                        "私は光先輩の顔を見つめながら、いなくなったあの人のことを思った。",
                        "日生先輩は全て知っていたのだろうか？",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            zh_path.write_text(
                "\n".join(
                    [
                        "日生光: 「叫我光先生。不然，叫光前辈也行」",
                        "我凝视着光前辈的脸，心里想着那个消失的人。",
                        "日生学长知道这一切吗？",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("日生光: 「叫我光先生。不然，叫光前辈也行」", text)
            self.assertIn("日生前辈知道这一切吗？", text)
            self.assertEqual([change.rule_id for change in changes], ["hinase-senpai"])

    def test_ratio_fallback_only_when_no_exact_dialogue_anchor_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ja_dir = root / "bookish" / "reading_order"
            zh_dir = root / "bookish_zhcn" / "reading_order"
            ja_dir.mkdir(parents=True)
            zh_dir.mkdir(parents=True)
            ja_path = ja_dir / "sample.md"
            zh_path = zh_dir / "sample.md"

            ja_path.write_text(
                "\n".join(
                    [
                        "遠野　紗夜: 「始めましょう」",
                        "千代: 「ははっ……。お嬢さん。やはり、お嬢さんは素敵な人ですね」",
                        "そんな尤もらしいことを言うと、千代さんは腕を組みうーんと悩んだ。",
                        "遠野　紗夜: 「次へ行きましょう」",
                        "宮沢 夏帆: 「到着だよ」",
                        "千代: 「わあ、本当にお嬢様ですね」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            zh_path.write_text(
                "\n".join(
                    [
                        "远野纱夜: 「开始吧」",
                        "远野纱夜: 「去下一段吧」",
                        "千代: 「哈哈……大小姐。您果然是个很棒的人呢」",
                        "我这么一本正经地说完，千代先生抱起胳膊，嗯——地思考起来。",
                        "宫泽夏帆: 「到了哦」",
                        "千代: 「哇，真是大小姐啊」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("千代: 「哈哈……小姐。您果然是个很棒的人呢」", text)
            self.assertIn("我这么一本正经地说完，千代抱起胳膊，嗯——地思考起来。", text)
            self.assertIn("千代: 「哇，真是大小姐啊」", text)
            self.assertEqual(
                [change.rule_id for change in changes],
                ["chiyo-ojousan", "sayo-to-chiyo-san"],
            )

    def test_project_duplicate_choice_block_residue_uses_ratio_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh_dir = root / "bookish_zhcn" / "reading_order"
            zh_dir.mkdir(parents=True)
            ja_path = ROOT / "bookish" / "reading_order" / "04_chapter3.md"
            zh_path = zh_dir / "04_chapter3.md"
            shutil.copyfile(ROOT / "bookish_zhcn" / "reading_order" / "04_chapter3.md", zh_path)

            apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertNotIn("千代先生抱起胳膊", text)
            self.assertNotIn("千代先生完全不是人类", text)
            self.assertIn("千代抱起胳膊", text)
            self.assertIn("千代完全不是人类", text)

    def test_chiyo_san_new_round_cleans_identity_titles_and_topic_phrasing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ja_dir = root / "bookish" / "reading_order"
            zh_dir = root / "bookish_zhcn" / "reading_order"
            ja_dir.mkdir(parents=True)
            zh_dir.mkdir(parents=True)
            ja_path = ja_dir / "sample.md"
            zh_path = zh_dir / "sample.md"

            ja_path.write_text(
                "\n".join(
                    [
                        "遠野　紗夜: 「こんにちは、千代さん」",
                        "千代さんは手を握ってくれた。",
                        "遠野　紗夜: 「千代さんが学校に来るのには許可がいるのですか？」",
                        "遠野　紗夜: 「千代さ……」",
                        "遠野　紗夜: 「千代さん、私の所へ来ませんか？」",
                        "遠野　紗夜: 「桐島先輩が小さな頃はよく手を繋いでくれていたと」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            zh_path.write_text(
                "\n".join(
                    [
                        "远野纱夜: 「你好，千代同学」",
                        "千代女士握住了我的手。",
                        "远野纱夜: 「千代你来学校需要许可吗？」",
                        "远野纱夜: 「千代小……」",
                        "远野纱夜: 「千代，您要不要来我这边？」",
                        "远野纱夜: 「说桐岛前辈小时候经常牵着千代同学的手」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("远野纱夜: 「你好，千代」", text)
            self.assertIn("千代握住了我的手。", text)
            self.assertIn("远野纱夜: 「千代来学校需要许可吗？」", text)
            self.assertIn("远野纱夜: 「千代……」", text)
            self.assertIn("远野纱夜: 「千代，愿意到我这里来吗？」", text)
            self.assertIn("远野纱夜: 「说桐岛前辈小时候经常牵着千代的手」", text)
            self.assertEqual(
                [change.rule_id for change in changes],
                [
                    "sayo-to-chiyo-san",
                    "sayo-to-chiyo-san",
                    "sayo-to-chiyo-topic-naturalization",
                    "sayo-to-chiyo-san-truncation",
                    "sayo-to-chiyo-topic-naturalization",
                    "chiyo-address-residual-exact",
                ],
            )

    def test_ratio_fallback_does_not_borrow_hikari_senpai_from_distant_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh_dir = root / "bookish_zhcn" / "reading_order"
            zh_dir.mkdir(parents=True)
            ja_path = ROOT / "bookish" / "reading_order" / "11_kirishima_chapter5_branch.md"
            zh_path = zh_dir / "11_kirishima_chapter5_branch.md"
            shutil.copyfile(ROOT / "bookish_zhcn" / "reading_order" / "11_kirishima_chapter5_branch.md", zh_path)

            apply_honorific_guidelines([ja_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("光先生像开玩笑一样轻易说出了『喜欢』。", text)
            self.assertNotIn("光前辈像开玩笑一样轻易说出了『喜欢』。", text)


if __name__ == "__main__":
    unittest.main()

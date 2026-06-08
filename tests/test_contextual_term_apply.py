import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.contextual_term_apply import apply_contextual_terms, collect_review_findings


class ContextualTermApplyTests(unittest.TestCase):
    def test_applies_contextual_kotoba_and_honmono_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh_dir = root / "bookish_zhcn" / "reading_order"
            zh_dir.mkdir(parents=True)
            zh_path = zh_dir / "sample.md"
            zh_path.write_text(
                "\n".join(
                    [
                        "这个国家的语言真复杂。",
                        "远野纱夜: 「我在寻找世界上最美的语言」",
                        "远野纱夜: 「是语言」",
                        "苍: 「语言？」",
                        "远野纱夜: 「描绘这景色的语言就有这么多，超出我现在能想到的语言吧」",
                        "苍: 「然后，在某个时候，人们开始赋予花语言」",
                        "远野纱夜教会了我语言。",
                        "在『Depth（深层的言叶）』画面生效的组合。",
                        "日生光: 「真正的『日生光』、假货‘日生光’、理想的‘日生光’」",
                        "日生光: 「称呼起来不方便吧？真品也好赝品也好，都叫日生光的话」",
                        "苍: 「本尊和冒牌货，甚至还出现了理想的『日生光』吗」",
                        "远野纱夜: 「于是，真正的母亲变成了赝品，而赝品的母亲变成了真正的母亲」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_contextual_terms([zh_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("这个国家的语言真复杂。", text)
            self.assertIn("远野纱夜: 「我在寻找世界上最美的话语」", text)
            self.assertIn("远野纱夜: 「是话语」", text)
            self.assertIn("苍: 「话语？」", text)
            self.assertIn("描绘这景色的词语就有这么多，超出我现在能想到的词语吧", text)
            self.assertIn("苍: 「然后，在某个时候，人们开始把话语寄托在花上」", text)
            self.assertIn("远野纱夜教会了我词语。", text)
            self.assertIn("在『Depth（深层之语）』画面生效的组合。", text)
            self.assertIn("日生光: 「正牌的『日生光』、冒牌的‘日生光’、理想的‘日生光’」", text)
            self.assertIn("正牌也好冒牌也好", text)
            self.assertIn("本人和冒牌货", text)
            self.assertIn("真正的母亲成了假的母亲，而假的母亲成了真正的母亲", text)
            self.assertGreaterEqual(len(changes), 8)

    def test_collects_remaining_review_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh_dir = root / "bookish_zhcn" / "reading_order"
            zh_dir.mkdir(parents=True)
            zh_path = zh_dir / "sample.md"
            zh_path.write_text(
                "\n".join(
                    [
                        "苍: 「这个国家的语言真复杂」",
                        "日生光: 「这样我就是真货了」",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            findings = collect_review_findings([zh_path], zh_dir=zh_dir, root=root)
            rule_ids = [finding.rule_id for finding in findings]

            self.assertIn("kotoba-remaining-review", rule_ids)
            self.assertIn("honmono-remaining-review", rule_ids)


if __name__ == "__main__":
    unittest.main()

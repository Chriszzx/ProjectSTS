import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.terminology_guideline_apply import apply_terminology, collect_review_findings


class TerminologyGuidelineApplyTests(unittest.TestCase):
    def test_applies_deterministic_terminology_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh_dir = root / "bookish_zhcn" / "reading_order"
            zh_dir.mkdir(parents=True)
            zh_path = zh_dir / "sample.md"
            zh_path.write_text(
                "\n".join(
                    [
                        "我站在时计塔前，看见远处的钟塔和旧钟楼。",
                        "司书: 「请在图书馆内保持安静」",
                        "我们寻找世界上最美的语言，也收集美丽的语言。",
                        "那是美丽的话语。",
                        "现在要讲述的是您的幻想故事。",
                        "千代的真名是秋樱花。那里有大波斯菊和樱花花。",
                        "日生光: 「真货和假货的区别」",
                        "真正的『日生光』与冒牌货『日生光』。",
                        "路易斯: 「您就是那家书店的真正主人了！」",
                        "日生光: 「称呼起来不方便吧？真品也好赝品也好，都叫日生光的话」",
                        "日生光: 「但是，我是真的。正牌『日生光』。那家伙，不是我」",
                        "于是，真正的母亲变成了赝品，而赝品的母亲变成了真正的母亲。",
                        "《笼里的鸟》",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_terminology([zh_path], zh_dir=zh_dir, root=root)
            text = zh_path.read_text(encoding="utf-8")

            self.assertIn("我站在时钟塔前，看见远处的时钟塔和旧时钟塔。", text)
            self.assertIn("图书管理员: 「请在图书馆内保持安静」", text)
            self.assertIn("我们寻找世界上最美的语言，也收集美丽的语言。", text)
            self.assertIn("那是美丽的话语。", text)
            self.assertIn("现在要讲述的是您的幻想物语。", text)
            self.assertIn("千代的真名是秋樱。那里有波斯菊和樱花。", text)
            self.assertIn("日生光: 「真货和假货的区别」", text)
            self.assertIn("真正的『日生光』与冒牌货『日生光』。", text)
            self.assertIn("路易斯: 「您就是那家书店的真正主人了！」", text)
            self.assertIn("日生光: 「称呼起来不方便吧？真品也好赝品也好，都叫日生光的话」", text)
            self.assertIn("日生光: 「但是，我是真的。正牌『日生光』。那家伙，不是我」", text)
            self.assertIn("于是，真正的母亲变成了赝品，而赝品的母亲变成了真正的母亲。", text)
            self.assertIn("《笼中鸟》", text)
            self.assertGreaterEqual(len(changes), 5)

    def test_collects_review_findings_after_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh_dir = root / "bookish_zhcn" / "reading_order"
            zh_dir.mkdir(parents=True)
            zh_path = zh_dir / "sample.md"
            zh_path.write_text(
                "\n".join(
                    [
                        "这是一个故事。",
                        "这个国家的语言很复杂。",
                        "那是深邃的青色天空。",
                        "他真的不是假的。",
                        "这，就是正主。",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            findings = collect_review_findings([zh_path], zh_dir=zh_dir, root=root)
            rule_ids = [finding.rule_id for finding in findings]

            self.assertIn("monogatari-review", rule_ids)
            self.assertIn("kotoba-language-review", rule_ids)
            self.assertIn("ao-color-review", rule_ids)
            self.assertIn("honmono-review", rule_ids)


if __name__ == "__main__":
    unittest.main()

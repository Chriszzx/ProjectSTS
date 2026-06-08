import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.translation_cleanup_audit import apply_auto_corrections, scan_paths


class TranslationCleanupAuditTests(unittest.TestCase):
    def test_scan_marks_auto_and_review_only_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh = root / "bookish_zhcn" / "reading_order"
            zh.mkdir(parents=True)
            sample = zh / "sample.md"
            sample.write_text(
                "\n".join(
                    [
                        '日生光: 「什么够不够？」',
                        "女学生A: 「呐呐，听说了吗？　钟楼的传闻」",
                        "今天他应该和光先生在一起才对。",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            findings = scan_paths([sample], root=root)

            by_rule = {finding.rule_id for finding in findings}
            self.assertIn("hard-misread-naniga", by_rule)
            self.assertIn("term-clocktower-variant", by_rule)
            self.assertIn("honorific-hikari-sensei", by_rule)

            auto_modes = {finding.rule_id: finding.mode for finding in findings}
            self.assertEqual(auto_modes["hard-misread-naniga"], "auto")
            self.assertEqual(auto_modes["term-clocktower-variant"], "review")
            self.assertEqual(auto_modes["honorific-hikari-sensei"], "review")

    def test_apply_only_changes_auto_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zh = root / "bookish_zhcn" / "reading_order"
            zh.mkdir(parents=True)
            sample = zh / "sample.md"
            sample.write_text(
                "\n".join(
                    [
                        '日生光: 「什么够不够？」',
                        "面对我的问题，他露出一副意外（或不以为然）的表情。",
                        "女学生A: 「呐呐，听说了吗？　钟楼的传闻」",
                        "今天他应该和光先生在一起才对。",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changes = apply_auto_corrections([sample], root=root)
            text = sample.read_text(encoding="utf-8")

            self.assertIn('日生光: 「什么？」', text)
            self.assertIn("面对我的问题，他露出一副不服气的表情。", text)
            self.assertIn("钟楼的传闻", text)
            self.assertIn("光先生", text)
            self.assertEqual([change.rule_id for change in changes], ["hard-misread-naniga", "hard-translator-note-shingai"])


if __name__ == "__main__":
    unittest.main()

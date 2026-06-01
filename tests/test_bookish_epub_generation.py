import tempfile
import unittest
import zipfile
from pathlib import Path

from branch_explore_arc.parse_arc import write_bookish_epub


class BookishEpubGenerationTests(unittest.TestCase):
    def test_frontmatter_and_cover_are_written_before_chapters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_dir = root / "bookish_zhcn"
            epub_dir = base_dir / "epub"
            complete_markdown = base_dir / "complete_epub.md"
            epub_file = base_dir / "book.epub"
            cover_image = base_dir / "cover.jpg"

            (base_dir / "reading_order").mkdir(parents=True)
            (base_dir / "reader_manual.md").write_text("# 中文版读本说明\n\n说明正文。\n", encoding="utf-8")
            (base_dir / "reading_order" / "00_hajimari.md").write_text("# 名字\n\n正文。\n", encoding="utf-8")
            cover_image.write_bytes(b"\xff\xd8\xff\xd9")

            outputs = write_bookish_epub(
                {"meta": {"sha256": "abc123"}},
                ["reading_order/00_hajimari.md"],
                base_dir=base_dir,
                epub_dir=epub_dir,
                epub_file=epub_file,
                complete_markdown=complete_markdown,
                title="死神与少女",
                language="zh-CN",
                author="ProjectSTS",
                identifier_suffix="bookish-complete-zhcn",
                frontmatter_files=["reader_manual.md"],
                cover_image=cover_image,
            )

            complete_text = complete_markdown.read_text(encoding="utf-8")
            self.assertLess(
                complete_text.index("<!-- source: reader_manual.md -->"),
                complete_text.index("<!-- source: reading_order/00_hajimari.md -->"),
            )

            nav_text = (epub_dir / "OEBPS" / "nav.xhtml").read_text(encoding="utf-8")
            self.assertLess(
                nav_text.index('href="text/reader_manual.xhtml"'),
                nav_text.index('href="text/reading_order_00_hajimari.xhtml"'),
            )

            opf_text = (epub_dir / "OEBPS" / "content.opf").read_text(encoding="utf-8")
            self.assertIn('<meta name="cover" content="cover-image" />', opf_text)
            self.assertIn('href="images/cover.jpg"', opf_text)
            self.assertIn('properties="cover-image"', opf_text)
            self.assertIn('href="text/cover.xhtml"', opf_text)
            self.assertLess(opf_text.index('idref="cover-page"'), opf_text.index('idref="chapter-1"'))

            with zipfile.ZipFile(epub_file) as archive:
                names = set(archive.namelist())
            self.assertIn("OEBPS/images/cover.jpg", names)
            self.assertIn("OEBPS/text/cover.xhtml", names)
            self.assertIn("OEBPS/text/reader_manual.xhtml", names)

            self.assertEqual(outputs["cover_image"], "epub/OEBPS/images/cover.jpg")
            self.assertEqual(outputs["frontmatter_files"], ["reader_manual.md"])


if __name__ == "__main__":
    unittest.main()

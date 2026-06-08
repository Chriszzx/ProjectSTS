import tempfile
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from branch_explore_arc.parse_arc import (
    BOOKISH_ZHCN_EPUB_FILE,
    BOOKISH_ZHCN_REFERENCE_EPUB_FILE,
    BookishTranslator,
    apply_bookish_fine_navigation,
    clean_dialogue_content,
    markdown_to_epub_xhtml,
    sanitize_translation_text,
    write_bookish_epub,
)


class BookishEpubGenerationTests(unittest.TestCase):
    def test_zhcn_generation_uses_distinct_filename_from_frozen_reference(self):
        self.assertEqual(BOOKISH_ZHCN_REFERENCE_EPUB_FILE.name, "bookish_complete.zh.epub")
        self.assertEqual(BOOKISH_ZHCN_EPUB_FILE.name, "死神与少女_中文完整剧本.epub")

    def write_authoritative_epub(
        self,
        path: Path,
        pairs: list[tuple[str, str]],
        xhtml_name: str = "OEBPS/text/sample.xhtml",
    ) -> None:
        paragraphs = []
        for jp, zh in pairs:
            paragraphs.append(f'<p style="opacity:0.50;">{jp}</p>')
            paragraphs.append(f"<p>{zh}</p>")
        xhtml = "\n".join(
            [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<html xmlns="http://www.w3.org/1999/xhtml">',
                "<body>",
                *paragraphs,
                "</body>",
                "</html>",
            ]
        )
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(xhtml_name, xhtml)

    def test_translator_uses_authoritative_epub_over_manual_defaults_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            epub = root / "authoritative.epub"
            self.write_authoritative_epub(
                epub,
                [
                    (
                        "ええ、そうでしたね。遠野紗夜。それが、貴方のお名前……",
                        "啊，说得对呢。远野纱夜。那就是，你的名字……",
                    )
                ],
            )

            translator = BookishTranslator(
                processed_dir=root / "missing_processed",
                translated_dir=root / "missing_translated",
                authoritative_epub=epub,
            )

            self.assertEqual(
                translator.lookup("ええ、そうでしたね。遠野紗夜。それが、貴方のお名前……"),
                "啊，说得对呢。远野纱夜。那就是，你的名字……",
            )

    def test_translator_does_not_load_legacy_processed_translations_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed = root / "processed"
            translated = root / "translated"
            (processed / "chapter").mkdir(parents=True)
            (translated / "chapter").mkdir(parents=True)
            (processed / "chapter" / "scene.txt").write_text("古い原文\n", encoding="utf-8")
            (translated / "chapter" / "scene_translated.txt").write_text("旧翻译\n", encoding="utf-8")

            translator = BookishTranslator(
                processed_dir=processed,
                translated_dir=translated,
                authoritative_epub=root / "missing.epub",
            )

            self.assertIsNone(translator.lookup("古い原文"))

            legacy_translator = BookishTranslator(
                processed_dir=processed,
                translated_dir=translated,
                authoritative_epub=root / "missing.epub",
                allow_legacy_fallbacks=True,
            )

            self.assertEqual(legacy_translator.lookup("古い原文"), "旧翻译")

    def test_missing_translation_keeps_source_content_unmodified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            translator = BookishTranslator(
                processed_dir=root / "missing_processed",
                translated_dir=root / "missing_translated",
                authoritative_epub=root / "missing.epub",
            )

            self.assertEqual(
                translator.translate_line("遠野 十夜: 「こんな夜遅くまで何をしていたんだい？」"),
                "远野十夜: 「こんな夜遅くまで何をしていたんだい？」",
            )
            self.assertEqual(translator.translate_line("夜の空は黒ばかり"), "夜の空は黒ばかり")

    def test_short_authoritative_lines_do_not_cross_chapter_when_source_file_misses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            epub = root / "authoritative.epub"
            self.write_authoritative_epub(
                epub,
                [("遠野　紗夜: 「ありがとうございます」", "远野纱夜: 「谢谢你们」")],
                "OEBPS/text/01_prologue.xhtml",
            )
            translator = BookishTranslator(
                processed_dir=root / "missing_processed",
                translated_dir=root / "missing_translated",
                authoritative_epub=epub,
            )

            self.assertEqual(
                translator.translate_line("遠野　紗夜: 「ありがとうございます」", "prologue/hajimari.txt"),
                "远野纱夜: 「ありがとうございます」",
            )
            self.assertEqual(
                translator.translate_line("遠野　紗夜: 「ありがとうございます」", "prologue/prologue_1.txt"),
                "远野纱夜: 「谢谢你们」",
            )

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

    def test_translation_cleanup_removes_stray_ascii_quotes_at_dialogue_edges(self):
        self.assertEqual(clean_dialogue_content('"…………'), "…………")
        self.assertEqual(sanitize_translation_text('远野纱夜: 「"…………」'), "远野纱夜: 「…………」")
        self.assertEqual(sanitize_translation_text('他说: 「"啊哈哈。"」'), "他说: 「啊哈哈」")

    def test_fine_navigation_adds_route_skip_links_and_epub_anchors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.md"
            path.write_text(
                "\n".join(
                    [
                        "# 一章",
                        "",
                        "共通段。",
                        "",
                        "---",
                        "",
                        "## 日生光・桐岛七葵",
                        "",
                        "日生桐岛段。",
                        "",
                        "---",
                        "",
                        "## 苍",
                        "",
                        "苍段。",
                        "",
                        "---",
                        "",
                        "## 全员共通",
                        "",
                        "回到共通。",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            apply_bookish_fine_navigation(path, "reading_order/02_chapter1.md")
            markdown = path.read_text(encoding="utf-8")

            self.assertIn("<!-- anchor: route-block-001 -->", markdown)
            self.assertIn("> 沿千代・远野十夜线继续：[下一段](#route-block-004)", markdown)
            self.assertIn("> 沿苍线继续：[下一段](#route-block-003)", markdown)

            xhtml = markdown_to_epub_xhtml(markdown, "一章", "zh-CN")
            self.assertIn('<span id="route-block-004" class="route-anchor"></span>', xhtml)
            self.assertIn('<a href="#route-block-004">下一段</a>', xhtml)

    def test_navigation_ended_scene_break_forces_next_scene_to_new_page(self):
        xhtml = markdown_to_epub_xhtml(
            "\n".join(
                [
                    "# 四章",
                    "",
                    "路线段。",
                    "",
                    "> 沿日生光线继续：[下一段](#route-block-002)",
                    "",
                    "---",
                    "",
                    "顺序下一段。",
                ]
            ),
            "四章",
            "zh-CN",
        )

        self.assertIn('<hr class="scene-break scene-page-break" />', xhtml)

    def test_navigation_followed_by_content_forces_new_page_without_scene_break(self):
        xhtml = markdown_to_epub_xhtml(
            "\n".join(
                [
                    "# 一章",
                    "",
                    "> 选择：答应",
                    "> 跳至：[一章-终](#badend-ch1-054)（选择「不答应」）",
                    "",
                    "远野纱夜: 「这样真的好吗」",
                    "",
                    "## 下一段",
                    "",
                    "正文。",
                ]
            ),
            "一章",
            "zh-CN",
        )

        page_break = '<hr class="scene-break scene-page-break" />'
        self.assertIn(page_break, xhtml)
        self.assertLess(xhtml.index(page_break), xhtml.index("远野纱夜"))
        self.assertEqual(xhtml.count(page_break), 1)

    def test_navigation_followed_by_anchor_places_anchor_on_new_page(self):
        xhtml = markdown_to_epub_xhtml(
            "\n".join(
                [
                    "# 六章",
                    "",
                    "> 跳至：[六章-终](#badend-ch6-340)（选择「放弃」）",
                    "",
                    "<!-- anchor: badend-ch6-340 -->",
                    "## 六章-终",
                    "",
                    "终局正文。",
                ]
            ),
            "六章",
            "zh-CN",
        )

        page_break = '<hr class="scene-break scene-page-break" />'
        anchor = '<span id="badend-ch6-340" class="route-anchor"></span>'
        heading = xhtml.index("<h2", xhtml.index(anchor))
        self.assertLess(xhtml.index(page_break), xhtml.index(anchor))
        self.assertLess(xhtml.index(anchor), heading)

    def test_japanese_navigation_followed_by_anchor_places_anchor_on_new_page(self):
        xhtml = markdown_to_epub_xhtml(
            "\n".join(
                [
                    "# 六章",
                    "",
                    "> 飛ぶ：[六章-終](#badend-ch6-340)（選択「諦める」）",
                    "",
                    "<!-- anchor: badend-ch6-340 -->",
                    "## 六章-終",
                    "",
                    "終局本文。",
                ]
            ),
            "六章",
            "ja",
        )

        page_break = '<hr class="scene-break scene-page-break" />'
        anchor = '<span id="badend-ch6-340" class="route-anchor"></span>'
        heading = xhtml.index("<h2", xhtml.index(anchor))
        self.assertLess(xhtml.index(page_break), xhtml.index(anchor))
        self.assertLess(xhtml.index(anchor), heading)


if __name__ == "__main__":
    unittest.main()

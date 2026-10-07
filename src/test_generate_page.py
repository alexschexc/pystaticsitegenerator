import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from generate_page import generate_page


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.markdown = self.root / "index.md"
        self.template = self.root / "template.html"
        self.destination = self.root / "public" / "nested" / "index.html"
        self.markdown.write_text("# Hello\n\nA **bold** paragraph.", encoding="utf-8")
        self.template.write_text(
            "<title>{{ Title }}</title><article>{{ Content }}</article>",
            encoding="utf-8",
        )

    def generate(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            generate_page(str(self.markdown), str(self.template), str(self.destination))
        return output.getvalue()

    def test_generates_html_and_creates_parent_directories(self):
        self.generate()
        self.assertEqual(self.destination.read_text(encoding="utf-8"),
            "<title>Hello</title><article><div><h1>Hello</h1>"
            "<p>A <b>bold</b> paragraph.</p></div></article>")

    def test_logs_source_template_and_destination(self):
        output = self.generate()
        for path in (self.markdown, self.template, self.destination):
            self.assertIn(str(path), output)

    def test_overwrites_existing_output(self):
        self.destination.parent.mkdir(parents=True)
        self.destination.write_text("stale", encoding="utf-8")
        self.generate()
        self.assertNotIn("stale", self.destination.read_text(encoding="utf-8"))

    def test_unicode_content(self):
        self.markdown.write_text("# Café\n\nこんにちは", encoding="utf-8")
        self.generate()
        self.assertEqual(self.destination.read_text(encoding="utf-8"),
            "<title>Café</title><article><div><h1>Café</h1><p>こんにちは</p></div></article>")

    def test_missing_title_does_not_write_output(self):
        self.markdown.write_text("No heading here.", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no h1"):
            self.generate()
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()

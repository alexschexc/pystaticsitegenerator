import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from generate_pages_recursive import generate_pages_recursive


class TestGeneratePagesRecursive(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.content = self.root / "content"
        self.content.mkdir()
        self.destination = self.root / "public"
        self.template = self.root / "template.html"
        self.template.write_text("<title>{{ Title }}</title>{{ Content }}", encoding="utf-8")

    def generate(self):
        with contextlib.redirect_stdout(io.StringIO()):
            generate_pages_recursive(str(self.content), str(self.template), str(self.destination))

    def test_root_and_nested_pages(self):
        (self.content / "index.md").write_text("# Home", encoding="utf-8")
        nested = self.content / "blog" / "post"
        nested.mkdir(parents=True)
        (nested / "index.md").write_text("# Post", encoding="utf-8")
        self.generate()
        self.assertEqual(
            self.destination.joinpath("index.html").read_text(encoding="utf-8"),
            "<title>Home</title><div><h1>Home</h1></div>",
        )
        self.assertEqual(
            self.destination.joinpath("blog/post/index.html").read_text(encoding="utf-8"),
            "<title>Post</title><div><h1>Post</h1></div>",
        )
        self.assertEqual(
            {p.relative_to(self.destination).as_posix() for p in self.destination.rglob("*.html")},
            {"index.html", "blog/post/index.html"},
        )

    def test_non_markdown_files_are_ignored(self):
        (self.content / "notes.txt").write_text("Not Markdown", encoding="utf-8")
        (self.content / "index.md").write_text("# Home", encoding="utf-8")
        self.generate()
        self.assertEqual(
            [p.name for p in self.destination.iterdir()], ["index.html"],
        )

    def test_only_final_extension_is_replaced(self):
        (self.content / "notes.v2.md").write_text("# Notes", encoding="utf-8")
        self.generate()
        self.assertTrue((self.destination / "notes.v2.html").is_file())

    def test_empty_content_directory(self):
        self.generate()
        self.assertFalse(self.destination.exists())

    def test_regeneration_overwrites_page(self):
        source = self.content / "index.md"
        source.write_text("# Old", encoding="utf-8")
        self.generate()
        source.write_text("# New", encoding="utf-8")
        self.generate()
        self.assertEqual(
            (self.destination / "index.html").read_text(encoding="utf-8"),
            "<title>New</title><div><h1>New</h1></div>",
        )


if __name__ == "__main__":
    unittest.main()

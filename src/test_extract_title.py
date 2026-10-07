import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_title_whitespace(self):
        self.assertEqual(extract_title("#   Hello world  "), "Hello world")

    def test_title_after_other_content(self):
        self.assertEqual(extract_title("Intro\n\n## Subtitle\n\n# Title"), "Title")

    def test_first_h1_is_used(self):
        self.assertEqual(extract_title("# First\n\n# Second"), "First")

    def test_missing_h1_raises(self):
        for markdown in ("", "Paragraph", "## Subtitle", "#No space"):
            with self.subTest(markdown=markdown):
                with self.assertRaisesRegex(ValueError, "no h1"):
                    extract_title(markdown)


if __name__ == "__main__":
    unittest.main()

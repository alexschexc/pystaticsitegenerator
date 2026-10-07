import unittest
from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_image(self):
        text = "Before ![a cat](https://example.com/cat.png) after"
        expected = [("a cat", "https://example.com/cat.png")]

        actual = extract_markdown_images(text)

        self.assertEqual(actual, expected)

    def test_links_excludes_images(self):
        text = (
            "![a cat](https://example.com/cat.png) "
            "[a website](https://example.com)"
        )
        expected = [("a website", "https://example.com")]

        actual = extract_markdown_links(text)

        self.assertEqual(actual, expected)


    def test_multiple_images_preserve_order(self):
        text = (
            "![first](https://example.com/first.png) and "
            "![second](https://example.com/second.png)"
        )
        expected = [
            ("first", "https://example.com/first.png"),
            ("second", "https://example.com/second.png"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_links_preserve_order(self):
        text = (
            "[first](https://example.com/first) and "
            "[second](https://example.com/second)"
        )
        expected = [
            ("first", "https://example.com/first"),
            ("second", "https://example.com/second"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_images_with_no_matches(self):
        for text in ("", "Just plain text.", "[link](https://example.com)"):
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_images(text), [])

    def test_links_with_no_matches(self):
        for text in ("", "Just plain text.", "![image](https://example.com/image.png)"):
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_links(text), [])

    def test_image_with_empty_alt_text(self):
        text = "![](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://example.com/image.png")],
        )

    def test_link_with_empty_anchor_text(self):
        text = "[](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("", "https://example.com")],
        )


if __name__ == "__main__":
    unittest.main()

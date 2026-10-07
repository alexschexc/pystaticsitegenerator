import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_assignment_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_heading_paragraph_and_list(self):
        md = "# Heading\n\nA paragraph.\n\n- first\n- second"
        self.assertEqual(markdown_to_blocks(md), [
            "# Heading",
            "A paragraph.",
            "- first\n- second",
        ])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("A paragraph."), ["A paragraph."])

    def test_single_newline_stays_inside_block(self):
        self.assertEqual(
            markdown_to_blocks("First line\nSecond line"),
            ["First line\nSecond line"],
        )

    def test_strips_each_block(self):
        md = " \tFirst paragraph. \t\n\n\t Second paragraph.  "
        self.assertEqual(markdown_to_blocks(md), [
            "First paragraph.",
            "Second paragraph.",
        ])

    def test_excessive_newlines_do_not_create_empty_blocks(self):
        for count in (3, 4, 5, 6):
            with self.subTest(newline_count=count):
                md = "First" + "\n" * count + "Second"
                self.assertEqual(markdown_to_blocks(md), ["First", "Second"])

    def test_leading_and_trailing_blank_lines(self):
        self.assertEqual(markdown_to_blocks("\n\n\nFirst\n\nSecond\n\n\n"), [
            "First",
            "Second",
        ])

    def test_whitespace_only_blocks_are_removed(self):
        md = "First\n\n \t \n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"])

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_whitespace_only_input(self):
        for md in ("   ", "\t", "\n", "\n\n\n", " \t\n\n \t "):
            with self.subTest(markdown=md):
                self.assertEqual(markdown_to_blocks(md), [])

    def test_internal_whitespace_is_preserved(self):
        md = "  First  line\n    indented line\nlast\tline  "
        self.assertEqual(markdown_to_blocks(md), [
            "First  line\n    indented line\nlast\tline",
        ])

    def test_inline_markdown_is_not_interpreted(self):
        md = "**bold** _italic_ `code` ![image](image.png) [link](https://example.com)"
        self.assertEqual(markdown_to_blocks(md), [md])


if __name__ == "__main__":
    unittest.main()

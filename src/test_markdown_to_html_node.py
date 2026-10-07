import unittest
from markdown_to_html_node import markdown_to_html_node
from parentnode import ParentNode


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = (
            "This is **bolded** paragraph\ntext in a p\ntag here\n\n"
            "This is another paragraph with _italic_ text and `code` here"
        )
        expected = (
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>"
        )
        node = markdown_to_html_node(md)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
        assert node.children is not None
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.to_html(), expected)

    def test_codeblock(self):
        fence = "`" * 3
        md = (
            fence + "\nThis is text that _should_ remain\n"
            "the **same** even with inline stuff\n" + fence
        )
        expected = (
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre></div>"
        )
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_heading_levels(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                md = "#" * level + " A **heading**"
                expected = f"<div><h{level}>A <b>heading</b></h{level}></div>"
                self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_quote_with_blank_quote_line(self):
        md = "> **first**\n>\n>second"
        expected = "<div><blockquote><b>first</b>  second</blockquote></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_unordered_list_with_inline_formatting(self):
        md = "- **first**\n- _second_"
        expected = "<div><ul><li><b>first</b></li><li><i>second</i></li></ul></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_ordered_list_with_two_digit_item(self):
        md = "\n".join(f"{number}. item {number}" for number in range(1, 12))
        items = "".join(f"<li>item {number}</li>" for number in range(1, 12))
        self.assertEqual(markdown_to_html_node(md).to_html(), "<div><ol>" + items + "</ol></div>")

    def test_link_and_image_in_paragraph(self):
        md = "![cat](cat.png) and [site](https://example.com)"
        expected = (
            '<div><p><img src="cat.png" alt="cat"> and '
            '<a href="https://example.com">site</a></p></div>'
        )
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_mixed_blocks_preserve_order(self):
        md = "# Title\n\nParagraph.\n\n> Quote\n\n- item\n\n1. first"
        expected = (
            "<div><h1>Title</h1><p>Paragraph.</p><blockquote>Quote</blockquote>"
            "<ul><li>item</li></ul><ol><li>first</li></ol></div>"
        )
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_empty_document(self):
        self.assertEqual(markdown_to_html_node(" \n\n ").to_html(), "<div></div>")

    def test_invalid_inline_markdown_raises(self):
        with self.assertRaises(ValueError):
            markdown_to_html_node("Unmatched **bold")


if __name__ == "__main__":
    unittest.main()

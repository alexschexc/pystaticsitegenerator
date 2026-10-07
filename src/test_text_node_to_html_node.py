import unittest
from leafnode import LeafNode
from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_and_formatting_types(self):
        cases = [
            (TextType.TEXT, None, "hello"),
            (TextType.BOLD, "b", "<b>hello</b>"),
            (TextType.ITALIC, "i", "<i>hello</i>"),
            (TextType.CODE, "code", "<code>hello</code>"),
        ]
        for text_type, tag, html in cases:
            with self.subTest(text_type=text_type):
                actual = text_node_to_html_node(TextNode("hello", text_type))
                self.assertIsInstance(actual, LeafNode)
                self.assertEqual(actual.tag, tag)
                self.assertEqual(actual.value, "hello")
                self.assertEqual(actual.to_html(), html)

    def test_link(self):
        actual = text_node_to_html_node(TextNode("site", TextType.LINK, "https://example.com"))
        self.assertEqual(actual.props, {"href": "https://example.com"})
        self.assertEqual(actual.to_html(), '<a href="https://example.com">site</a>')

    def test_image(self):
        actual = text_node_to_html_node(TextNode("a cat", TextType.IMAGE, "cat.png"))
        self.assertEqual(actual.tag, "img")
        self.assertEqual(actual.value, "")
        self.assertEqual(actual.props, {"src": "cat.png", "alt": "a cat"})
        self.assertEqual(actual.to_html(), '<img src="cat.png" alt="a cat">')

    def test_image_with_empty_alt_text(self):
        actual = text_node_to_html_node(TextNode("", TextType.IMAGE, "cat.png"))
        self.assertEqual(actual.to_html(), '<img src="cat.png" alt="">')

    def test_empty_plain_text(self):
        self.assertEqual(text_node_to_html_node(TextNode("", TextType.TEXT)).to_html(), "")

    def test_unsupported_type_raises(self):
        with self.assertRaisesRegex(ValueError, "Unsupported text type"):
            # Deliberately violate the input type to exercise runtime validation.
            text_node_to_html_node(TextNode("hello", "unsupported"))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

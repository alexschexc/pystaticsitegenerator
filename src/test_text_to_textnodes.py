import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_assignment_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_plain_text(self):
        self.assertEqual(
            text_to_textnodes("Just plain text."),
            [TextNode("Just plain text.", TextType.TEXT)],
        )

    def test_empty_text(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_each_syntax_on_its_own(self):
        cases = [
            ("**bold**", TextNode("bold", TextType.BOLD)),
            ("_italic_", TextNode("italic", TextType.ITALIC)),
            ("`code`", TextNode("code", TextType.CODE)),
            ("![image](https://example.com/image.png)",
             TextNode("image", TextType.IMAGE, "https://example.com/image.png")),
            ("[link](https://example.com)",
             TextNode("link", TextType.LINK, "https://example.com")),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(text_to_textnodes(text), [expected])

    def test_adjacent_formatted_sections(self):
        text = "**bold**_italic_`code`![image](image.png)[link](https://example.com)"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("image", TextType.IMAGE, "image.png"),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_repeated_images_and_links_with_identical_labels_and_urls(self):
        text = (
            "![site](https://example.com) [site](https://example.com) "
            "![site](https://example.com) [site](https://example.com)"
        )
        expected = [
            TextNode("site", TextType.IMAGE, "https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("site", TextType.LINK, "https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("site", TextType.IMAGE, "https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("site", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_syntax_inside_classified_nodes_stays_literal(self):
        # The simplified pipeline does not support nested inline elements.
        cases = [
            ("**bold _literal_**", TextNode("bold _literal_", TextType.BOLD)),
            ("_italic `literal`_", TextNode("italic `literal`", TextType.ITALIC)),
            ("`[literal](https://example.com)`",
             TextNode("[literal](https://example.com)", TextType.CODE)),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(text_to_textnodes(text), [expected])

    def test_whitespace_is_preserved(self):
        text = "  **bold**\n_italic_\t"
        expected = [
            TextNode("  ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("\n", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("\t", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_unmatched_delimiter_propagates_error(self):
        for text in ("Before **unfinished", "Before _unfinished", "Before `unfinished"):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "unmatched delimiter"):
                    text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()

import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word.", TextType.TEXT)
        actual_list = split_nodes_delimiter([node],"`", TextType.CODE)
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word.", TextType.TEXT)]
        self.assertEqual(actual_list, expected_list)

    def test_split_bold(self):
        node = TextNode("Before **bold** after", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_split_italic(self):
        node = TextNode("Before _italic_ after", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_no_delimiter_preserves_text(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual, [TextNode("Just plain text.", TextType.TEXT)])

    def test_multiple_formatted_sections(self):
        node = TextNode("Before **one** between **two** after", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode(" between ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_formatting_at_start(self):
        node = TextNode("**bold** after", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual, [
            TextNode("bold", TextType.BOLD),
            TextNode(" after", TextType.TEXT),
        ])

    def test_formatting_at_end(self):
        node = TextNode("Before **bold**", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual, [
            TextNode("Before ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    def test_entire_text_formatted(self):
        node = TextNode("**bold**", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual, [TextNode("bold", TextType.BOLD)])

    def test_non_text_nodes_pass_through_unchanged(self):
        nodes = [
            TextNode("**already bold", TextType.BOLD),
            TextNode("**already italic", TextType.ITALIC),
            TextNode("**already code", TextType.CODE),
            TextNode("**link", TextType.LINK, "https://example.com"),
            TextNode("**image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        actual = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(actual, nodes)
        for original, result in zip(nodes, actual):
            self.assertIs(result, original)

    def test_multiple_input_nodes_preserve_order(self):
        nodes = [
            TextNode("First **bold**", TextType.TEXT),
            TextNode("untouched", TextType.CODE),
            TextNode("_italic_ last", TextType.TEXT),
        ]
        actual = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("untouched", TextType.CODE),
            TextNode("_italic_ last", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD), [])

    def test_unmatched_delimiter_raises_helpful_error(self):
        cases = [
            ("Before **unfinished", "**", TextType.BOLD),
            ("Before _unfinished", "_", TextType.ITALIC),
            ("Before `unfinished", "`", TextType.CODE),
            ("**valid** then **unfinished", "**", TextType.BOLD),
        ]
        for text, delimiter, text_type in cases:
            with self.subTest(text=text, delimiter=delimiter):
                node = TextNode(text, TextType.TEXT)
                with self.assertRaisesRegex(ValueError, "unmatched delimiter") as caught:
                    split_nodes_delimiter([node], delimiter, text_type)
                self.assertIn(delimiter, str(caught.exception))

    def test_successive_delimiter_passes(self):
        nodes = [TextNode("**bold** and _italic_ with `code`", TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        actual = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

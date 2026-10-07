import unittest
from textnode import TextNode, TextType
from split_nodes_image import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_split_with_surrounding_text(self):
        node = TextNode("Before ![first](https://example.com/one) after", TextType.TEXT)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_multiple_matches(self):
        node = TextNode(
            "Before ![first](https://example.com/one) between "
            "![second](https://example.com/two) after", TextType.TEXT,
        )
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
            TextNode(" between ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "https://example.com/two"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_match_at_start(self):
        node = TextNode("![first](https://example.com/one) after", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_match_at_end(self):
        node = TextNode("Before ![first](https://example.com/one)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("Before ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
        ])

    def test_entire_text_is_match(self):
        node = TextNode("![first](https://example.com/one)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
        ])

    def test_adjacent_identical_matches(self):
        node = TextNode(
            "![first](https://example.com/one)![first](https://example.com/one)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
        ])

    def test_no_matches_preserves_original_node(self):
        for text in ("Plain text", "", "![unfinished](url"):
            with self.subTest(text=text):
                node = TextNode(text, TextType.TEXT)
                actual = split_nodes_image([node])
                self.assertEqual(actual, [node])
                self.assertIs(actual[0], node)

    def test_non_text_nodes_pass_through(self):
        for text_type in (TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE):
            with self.subTest(text_type=text_type):
                node = TextNode("![first](https://example.com/one)", text_type, "original-url")
                actual = split_nodes_image([node])
                self.assertEqual(actual, [node])
                self.assertIs(actual[0], node)

    def test_multiple_input_nodes_preserve_order(self):
        plain = TextNode("plain", TextType.TEXT)
        formatted = TextNode("untouched", TextType.CODE)
        nodes = [
            plain,
            TextNode("![first](https://example.com/one)", TextType.TEXT),
            formatted,
            TextNode("![second](https://example.com/two)", TextType.TEXT),
        ]
        expected = [
            plain,
            TextNode("first", TextType.IMAGE, "https://example.com/one"),
            formatted,
            TextNode("second", TextType.IMAGE, "https://example.com/two"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_does_not_mutate_input(self):
        node = TextNode("Before ![first](https://example.com/one) after", TextType.TEXT)
        nodes = [node]
        split_nodes_image(nodes)
        self.assertEqual(nodes, [
            TextNode("Before ![first](https://example.com/one) after", TextType.TEXT),
        ])
        self.assertIs(nodes[0], node)

    def test_regular_link_is_not_an_image(self):
        node = TextNode("[site](https://example.com)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])


if __name__ == "__main__":
    unittest.main()

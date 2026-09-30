import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_sameness(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC,  "https://boot.dev")
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is not a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_same_but_diff_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC,  "https://boot.dev/hi")
        self.assertNotEqual(node, node2)
    def test_same_but_diff_text_label(self):
        node = TextNode("This is a text noder", TextType.ITALIC, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC,  "https://boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

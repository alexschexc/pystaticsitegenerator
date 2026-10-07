import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        # init(tag=?, value=?, props=?)
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.orthodox.net"})
        self.assertEqual(node.to_html(), '<a href="https://www.orthodox.net">Click me!</a>')
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_missing_value_raises(self):
        with self.assertRaisesRegex(ValueError, "requires a value"):
            LeafNode("p", None).to_html()

    def test_empty_plain_text_is_allowed(self):
        self.assertEqual(LeafNode(None, "").to_html(), "")

    def test_empty_tagged_text_is_allowed(self):
        self.assertEqual(LeafNode("p", "").to_html(), "<p></p>")

    def test_image_has_no_closing_tag(self):
        node = LeafNode("img", "", {"src": "cat.png", "alt": "cat"})
        self.assertEqual(node.to_html(), '<img src="cat.png" alt="cat">')


if __name__ == "__main__":
    unittest.main()

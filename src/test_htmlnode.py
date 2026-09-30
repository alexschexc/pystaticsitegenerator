import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        # init(tag=?, value=?, children=?, props=?)
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    def test_one_prop(self):
        node = HTMLNode(props={"role": "button"})
        self.assertEqual(node.props_to_html(), ' role="button"')
    def test_many_prop(self):
        node = HTMLNode(props={"role": "button", "basecamp": "hey"})
        self.assertEqual(node.props_to_html(), ' role="button" basecamp="hey"')

if __name__ == "__main__":
    unittest.main()

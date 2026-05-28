import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Me!", {"href": "http://google.com"})
        self.assertEqual(node.to_html(), '<a href="http://google.com">Click Me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "No tags")
        self.assertEqual(node.to_html(), "No tags")

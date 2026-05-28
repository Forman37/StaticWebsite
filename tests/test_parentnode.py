import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_mult_children(self):
        child_node1 = LeafNode("b", "child_1")
        child_node2 = LeafNode("b", "child_2")
        child_node3 = LeafNode("b", "child_3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])

        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child_1</b><b>child_2</b><b>child_3</b></div>",
        )

    def test_to_html_mult_grandchildren(self):
        grandchild_node1 = LeafNode("b", "child_1")
        grandchild_node2 = LeafNode("b", "child_2")
        grandchild_node3 = LeafNode("b", "child_3")
        child_node = ParentNode(
            "div", [grandchild_node1, grandchild_node2, grandchild_node3]
        )

        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><div><b>child_1</b><b>child_2</b><b>child_3</b></div></div>",
        )

    def test_to_html_mult_child_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "child_1")
        grandchild_node2 = LeafNode("b", "child_2")
        grandchild_node3 = LeafNode("b", "child_3")
        child_node1 = ParentNode(
            "div", [grandchild_node1, grandchild_node2, grandchild_node3]
        )
        child_node2 = ParentNode(
            "div", [grandchild_node1, grandchild_node2, grandchild_node3]
        )
        child_node3 = ParentNode(
            "div", [grandchild_node1, grandchild_node2, grandchild_node3]
        )

        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])

        self.assertEqual(
            parent_node.to_html(),
            "<div><div><b>child_1</b><b>child_2</b><b>child_3</b></div><div><b>child_1</b><b>child_2</b><b>child_3</b></div><div><b>child_1</b><b>child_2</b><b>child_3</b></div></div>",
        )

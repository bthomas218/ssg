import sys
import os
import unittest

# Ensure local src directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", children=[grandchild_node])
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
        )

    def test_props_on_parent(self):
        child = LeafNode("i", "x")
        parent = ParentNode("section", children=[child])
        parent.props = {"id": "main", "class": "c"}
        html = parent.to_html()
        # both attributes must be present
        self.assertIn('id="main"', html)
        self.assertIn('class="c"', html)

    def test_missing_tag_raises(self):
        child = LeafNode("p", "x")
        # Create parent with empty tag
        parent = ParentNode(children=[child], tag=None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_missing_children_raises(self):
        parent = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_repr_includes_children(self):
        child = LeafNode("em", "x")
        parent = ParentNode("div", children=[child])
        r = repr(parent)
        self.assertIn("em", r)
        self.assertIn("x", r)
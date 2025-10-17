import sys
import os
import unittest

# Ensure local src directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "click", )
        node.props = {"href": "https://example.com"}
        html = node.to_html()
        self.assertEqual(html, '<a href="https://example.com">click</a>')

    def test_children_is_none(self):
        node = LeafNode("span", "x")
        self.assertIsNone(node.children)

    def test_repr_contains_tag_and_value(self):
        node = LeafNode("strong", "bold")
        r = repr(node)
        self.assertIn("strong", r)
        self.assertIn("bold", r)

    def test_different_tags(self):
        p = LeafNode("p", "para")
        img = LeafNode("img", "alt-text")
        self.assertIn("<p>", p.to_html())
        self.assertIn("<img>", img.to_html())
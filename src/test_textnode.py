import sys
import os
import unittest

# Ensure the workspace `src` directory is importable when running this file
sys.path.insert(0, os.path.dirname(__file__))

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node = TextNode("one", TextType.PLAIN)
        node2 = TextNode("two", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_type(self):
        node = TextNode("same", TextType.PLAIN)
        node2 = TextNode("same", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_field_and_repr(self):
        node = TextNode("link", TextType.LINK, url="https://example.com")
        node2 = TextNode("link", TextType.LINK, url="https://example.com")
        self.assertEqual(node, node2)
        # repr should include the URL string
        self.assertIn('https://example.com', repr(node))
    
    def test_url_none(self):
        node = TextNode("no url", TextType.PLAIN)
        node2 = TextNode("no url", TextType.PLAIN, url=None)
        self.assertEqual(node, node2)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
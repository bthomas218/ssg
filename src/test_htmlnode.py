import sys
import os
import unittest

# Ensure local src directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
	def test_props_to_html_none(self):
		node = HtmlNode(tag="div", value="x")
		# No props should produce empty string
		self.assertEqual(node.props_to_html(), "")

	def test_props_to_html_single(self):
		node = HtmlNode(tag="a", props={"href": "https://example.com"})
		html = node.props_to_html()
		# ordering in dicts is deterministic for insertion order, but we only need to
		# ensure the attribute is present in correct format
		self.assertIn('href="https://example.com"', html)

	def test_props_to_html_multiple(self):
		node = HtmlNode(tag="img", props={"src": "img.png", "alt": "pic"})
		html = node.props_to_html()
		# both attrs should appear
		self.assertIn('src="img.png"', html)
		self.assertIn('alt="pic"', html)

	def test_to_html_raises(self):
		# Base class should raise NotImplementedError for to_html
		with self.assertRaises(NotImplementedError):
			node = HtmlNode()
			node.to_html()

	def test_repr_and_children(self):
		child = HtmlNode(tag="span", value="child")
		parent = HtmlNode(tag="div", children=[child], props={"id": "p"})
		r = repr(parent)
		# repr should contain the tag and its value
		self.assertIn("tag='div'", r)
		# repr should include child's repr
		self.assertIn("span", r)


if __name__ == "__main__":
	unittest.main()
import sys
import os
import unittest

# Ensure the workspace `src` directory is importable when running this file
sys.path.insert(0, os.path.dirname(__file__))

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes
)


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

    # Tests for conversion to HTML
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_conversion(self):
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")

    def test_italic_conversion(self):
        node = TextNode("it", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "it")

    def test_code_conversion(self):
        node = TextNode("x=1", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "x=1")

    def test_link_conversion(self):
        node = TextNode("click", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_conversion(self):
        node = TextNode("alt text", TextType.IMAGE, url="/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        # images store alt in props and value may be None
        self.assertEqual(html_node.props, {"src": "/img.png", "alt": "alt text"})

    def test_unsupported_type_raises(self):
        class FakeType:
            pass
        node = TextNode("x", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
    def test_split_code_block_single(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_multiple_code_blocks(self):
        node = TextNode("pre `a` mid `b` end", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected = [
            TextNode("pre ", TextType.PLAIN),
            TextNode("a", TextType.CODE_TEXT),
            TextNode(" mid ", TextType.PLAIN),
            TextNode("b", TextType.CODE_TEXT),
            TextNode(" end", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("this has `unmatched", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_non_plain_nodes_are_preserved(self):
        # Non-PLAIN nodes should be passed through unchanged
        bold = TextNode("bold", TextType.BOLD)
        result = split_nodes_delimiter([bold], "`", TextType.CODE_TEXT)
        self.assertEqual(result, [bold])

    def test_empty_between_delimiters_skipped(self):
        node = TextNode("start``end", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        # The empty part between the two delimiters should be skipped
        expected = [TextNode("start", TextType.PLAIN), TextNode("end", TextType.PLAIN)]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_with_multiple_chars(self):
        node = TextNode("a **b** c", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("a ", TextType.PLAIN), TextNode("b", TextType.BOLD), TextNode(" c", TextType.PLAIN)]
        self.assertEqual(new_nodes, expected)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )

    def test_split_images_empty_alt(self):
        node = TextNode("before ![](img.png) after", TextType.PLAIN)
        new_nodes = split_nodes_images([node])
        self.assertEqual(
            new_nodes,
            [TextNode("before ", TextType.PLAIN), TextNode("", TextType.IMAGE, "img.png"), TextNode(" after", TextType.PLAIN)],
        )

    def test_split_links(self):
        node = TextNode("See [here](http://a) and [there](http://b)", TextType.PLAIN)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("See ", TextType.PLAIN),
                TextNode("here", TextType.LINK, "http://a"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("there", TextType.LINK, "http://b"),
            ],
        )

    def test_split_links_no_match(self):
        node = TextNode("no links here", TextType.PLAIN)
        self.assertEqual(split_nodes_links([node]), [node])

    def test_split_links_non_plain_preserved(self):
        node = TextNode("x", TextType.BOLD)
        self.assertEqual(split_nodes_links([node]), [node])
    
    def test_text_to_textnodes(self):
        text = "This is **bold** and `code` with a [link](http://example.com) and an ![image](img.png)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" with a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_underscores_and_adjacent(self):
        text = "_u1_**b**`c``d`"
        nodes = text_to_textnodes(text)
        # expected: u1 as bold (underscore), b as bold (double star), c as code, then d as code with empty plain in between handled
        self.assertTrue(any(n.text == "u1" and n.text_type == TextType.ITALIC for n in nodes))
        self.assertTrue(any(n.text == "b" and n.text_type == TextType.BOLD for n in nodes))
        self.assertTrue(any(n.text == "c" and n.text_type == TextType.CODE_TEXT for n in nodes))

    def test_text_to_textnodes_only_image_or_link(self):
        text = "![alt](i.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("alt", TextType.IMAGE, "i.png")])

        text2 = "[t](u)"
        nodes2 = text_to_textnodes(text2)
        self.assertEqual(nodes2, [TextNode("t", TextType.LINK, "u")])

    def test_text_to_textnodes_empty(self):
        # Current implementation returns an empty list for empty input
        self.assertEqual(text_to_textnodes("") , [])

if __name__ == "__main__":
    unittest.main()
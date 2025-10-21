import sys
import os
import unittest

# Ensure local src directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from markdown_to_html import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            )

        def test_markdown_multiple_blank_lines_and_whitespace(self):
            md = """
            
            First block


            
            Second block with  
            trailing spaces

            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["First block", "Second block with\ntrailing spaces"])

        def test_markdown_code_fence_preserved(self):
            md = """
            Here is code:

            ```py
            def f():
                return 1
            ```

            End
            """
            blocks = markdown_to_blocks(md)
            # Current implementation strips leading indentation from lines
            self.assertEqual(blocks, ["Here is code:", "```py\ndef f():\nreturn 1\n```", "End"])

        def test_markdown_empty_input(self):
            self.assertEqual(markdown_to_blocks(""), [])

            def test_markdown_to_html_node_heading_and_paragraph(self):
                md = "# Hello\n\nThis is a paragraph"
                root = markdown_to_html_node(md)
                # root should be a div with two children: h1 and p
                self.assertEqual(root.tag, "div")
                self.assertEqual(len(root.children), 2)
                self.assertEqual(root.children[0].tag, "h1")
                self.assertEqual(root.children[1].tag, "p")

            def test_markdown_to_html_node_code_block(self):
                md = "```py\ndef f():\n    return 1\n```"
                root = markdown_to_html_node(md)
                self.assertEqual(root.children[0].tag, "pre")
                # pre should contain a single code leaf
                code_child = root.children[0].children[0]
                self.assertEqual(code_child.tag, "code")

            def test_markdown_to_html_node_quote(self):
                md = "> Quote line 1\n> Quote line 2"
                root = markdown_to_html_node(md)
                self.assertEqual(root.children[0].tag, "blockquote")

            def test_markdown_to_html_node_lists(self):
                md = "- a\n- b\n\n1. one\n2. two"
                root = markdown_to_html_node(md)
                # first child is ul, second is ol
                self.assertEqual(root.children[0].tag, "ul")
                self.assertEqual(root.children[1].tag, "ol")

        def test_block_to_block_type_heading(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(block_to_block_type("## Sub"), BlockType.HEADING)

        def test_block_to_block_type_code(self):
            code = "```py\ndef f():\n    return 1\n```"
            self.assertEqual(block_to_block_type(code), BlockType.CODE)

        def test_block_to_block_type_quote(self):
            quote = "> line1\n> line2"
            self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

        def test_block_to_block_type_unordered_and_ordered(self):
            ul = "- item1\n- item2"
            ol = "1. one\n2. two"
            self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)
            self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

        def test_block_to_block_type_paragraph(self):
            self.assertEqual(block_to_block_type("Just a line."), BlockType.PARAGRAPH)

        def test_paragraphs(self):
            md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )
        
        def test_codeblock(self):
            md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
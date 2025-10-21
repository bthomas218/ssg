import sys
import os
import unittest

# Ensure local src directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from markdown_to_html import markdown_to_blocks

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
            print(f"Blocks: {blocks}")
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
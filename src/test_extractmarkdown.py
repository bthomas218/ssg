import sys
import os
import unittest

# Ensure local src directory is importable
sys.path.insert(0, os.path.dirname(__file__))

from extract_markdown import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        txt = "Link to [example](https://example.com) and another [doc](http://doc.local)"
        matches = extract_markdown_links(txt)
        self.assertListEqual([("example", "https://example.com"), ("doc", "http://doc.local")], matches)

    def test_image_with_empty_alt(self):
        txt = "Here is an image: ![](http://img.png)"
        matches = extract_markdown_images(txt)
        self.assertListEqual([("", "http://img.png")], matches)

    def test_multiple_images_and_links(self):
        txt = "![a](1.png) text [b](http://b) ![c](2.png) [d](http://d)"
        imgs = extract_markdown_images(txt)
        links = extract_markdown_links(txt)
        self.assertListEqual([("a", "1.png"), ("c", "2.png")], imgs)
        self.assertListEqual([("b", "http://b"), ("d", "http://d")], links)

    def test_link_not_catching_image(self):
        txt = "![img](i.png) and [link](l.com)"
        links = extract_markdown_links(txt)
        # link extractor should not return the image
        self.assertListEqual([("link", "l.com")], links)

    def test_links_with_spaces_and_titles(self):
        txt = '[text with space](http://x.com "title") and ![alt text](img.png "imgtitle")'
        links = extract_markdown_links(txt)
        imgs = extract_markdown_images(txt)
        # URLs include the title portion in our simple regex, so verify capturing behavior
        self.assertTrue(len(links) == 1)
        self.assertTrue(len(imgs) == 1)

    def test_extract_title_basic(self):
        md = "# My Title\n\nContent"
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_strips_and_first_header(self):
        md = "   #   Spaced Title   \n# Other\n"
        self.assertEqual(extract_title(md), "Spaced Title")

    def test_extract_title_trailing_hashes(self):
        md = "# Title ###\n"
        self.assertEqual(extract_title(md), "Title ###")

    def test_extract_title_no_header_raises(self):
        with self.assertRaises(ValueError):
            extract_title("No headings here\nJust text")
    
    
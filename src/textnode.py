from enum import Enum
from dataclasses import dataclass
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE_TEXT = "code_text"
    LINK = "link"
    IMAGE = "image"


"""Representation of a piece of text with a type and optional URL.
@text: The text content or alt text
@text_type: The type of text (from TextType).
@url: Optional URL associated with the text (for links/images).
"""
@dataclass
class TextNode:
    
    text: str
    text_type: TextType
    url: str = None

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"

# Convert a TextNode to an HtmlNode (LeafNode)
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")
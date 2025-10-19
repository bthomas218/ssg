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



@dataclass
class TextNode:
    """Representation of a piece of text with a type and optional URL.
    @text: The text content or alt text
    @text_type: The type of text (from TextType).
    @url: Optional URL associated with the text (for links/images).
    """
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
        

def split_nodes_delimiter(old_nodes: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    """Splits a TextNode into multiple TextNodes based on the given markdown delimiter
    @Old_nodes: The original TextNodes to split
    @delimiter: The delimiter string to split on
    @Text_type: The TextType for the delimiter
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN: # Only attempt to split plain text nodes
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0: # Even number of parts means unmatched delimiter
            raise Exception(f"Unmatched delimiter {delimiter} in text: {node.text}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0: # Even index: normal text
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else: # Odd index: delimiter text
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


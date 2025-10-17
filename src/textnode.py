from enum import Enum
from dataclasses import dataclass


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE_TEXT = "cod_text"
    LINK = "link"
    IMAGE = "image"


"""Representation of a piece of text with a type and optional URL.
@text: The text content.
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
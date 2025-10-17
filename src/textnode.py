from enum import Enum
from dataclasses import dataclass

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE_TEXT = "cod_text"
    LINK = "link"
    IMAGE = "image"

@dataclass
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str= None):
        self.text = text
        self.text_type = text_type
        self.url = url  # Used for links and images
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
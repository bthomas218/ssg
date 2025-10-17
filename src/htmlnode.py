from dataclasses import dataclass, field

"""Representation of a node in an HTML document tree
@tag: The HTML tag (e.g., 'div', 'p', etc.).
@value: The text value inside the HTML tag.
@children: List of child HtmlNode objects.
@props: Dictionary of HTML properties/attributes for the tag.
"""
@dataclass
class HtmlNode:
    tag: str | None = None
    value: str | None = None
    children: list["HtmlNode"] | None = None
    props: dict[str, str] | None = None

    
    # Child classes will overwrite this method to render themselves as HTML
    def to_html(self):
        raise NotImplementedError("Must be overwritten in subclass")
    
    # Return HTML attributes as a string
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " ".join([f'{k}="{v}"' for k, v in self.props.items()])
    
    def __repr__(self):
        return f"HtmlNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

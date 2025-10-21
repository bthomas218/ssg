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

"""Representation of a Leaf Node in an HTML document tree
@tag: The HTML tag (e.g., 'div', 'p', etc.).
@value: Text value inside the HTML tag.
@children: Cannot have children (always None).
@props: Dictionary of HTML properties/attributes for the tag.
"""
@dataclass
class LeafNode(HtmlNode):
    value: str = None
    tag: str = None
    children: None = None

    # Renders the leaf node as HTML
    def to_html(self):
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        elif self.tag:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return self.value

"""Representation of a Parent Node in an HTML document tree
@tag: Required HTML tag (e.g., 'div', 'p', etc.).
@value: Cannot have a value (always None).
@children: Required List of child HtmlNode objects.
@props: Dictionary of HTML properties/attributes for the tag.
"""  
@dataclass
class ParentNode(HtmlNode):
    children: list["HtmlNode"]
    tag: str
    value: None = None

    # Renders the parent node and its children as HTML
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to render HTML")
        if not self.children:
            raise ValueError("ParentNode must have children to render HTML")
        props_str = self.props_to_html()
        children_html = "".join([child.to_html() for child in self.children])
        if props_str:
            return f"<{self.tag} {props_str}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"

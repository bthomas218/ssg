from enum import Enum
import re
from htmlnode import HtmlNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_images, split_nodes_links, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown_text: str) -> list[str]:
    """Converts markdown text into a list of "block strings"
    @markdown_text: The markdown text to convert
    """
    blocks = markdown_text.split("\n\n")
    to_remove = set()
    for i, block in enumerate(blocks):
        stripped = "\n".join([line.strip() for line in block.split("\n")]).strip()
        if stripped == "":
            to_remove.add(i)
            continue
        blocks[i] = stripped
    # Remove empty blocks in reverse order to avoid index shifting
    for i in sorted(to_remove, reverse=True):
        del blocks[i]
    return blocks

def block_to_block_type(block: str) -> BlockType:
    """Determines the BlockType of a given markdown block string
    @block: The markdown block string
    """
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
    if block.startswith(("- ")):
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    if block.startswith("1. "):
        if all(line.lstrip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> HtmlNode:
    """Converts a markdown string to HtmlNodes under a single ParentNode
    which is a div
    @markdown: The markdown string to convert
    """
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                # Count leading '#' characters to determine heading level
                hash_match = block.split(" ", 1)[0]
                heading_number = len(hash_match)
                # Extract the heading text after the leading hashes and space
                heading_text = block[len(hash_match):].strip()
                node = ParentNode(tag=f"h{heading_number}", children=text_to_children(heading_text))
                nodes.append(node)

            case BlockType.CODE: # Should not do inline markdown parsing of children
                lines = block.splitlines()
                code_content = "\n".join(lines[1:-1])  # Strip the ```
                if not code_content.endswith("\n"):
                    code_content = code_content + "\n"
                node = ParentNode(tag="pre", children=[
                    LeafNode(tag="code", value=code_content)
                ])
                nodes.append(node)

            case BlockType.QUOTE:
                # Remove leading '> ' from each line for the quote content
                quote_text = "\n".join([line[1:].lstrip() if line.startswith(">") else line for line in block.split("\n")])
                node = ParentNode(tag="blockquote", children=text_to_children(quote_text))
                nodes.append(node)

            case BlockType.UNORDERED_LIST:
                node = ParentNode(tag="ul", children=[
                    ParentNode(tag="li", children=text_to_children(line[2:])) for line in block.split("\n")
                ])
                nodes.append(node)
            case BlockType.ORDERED_LIST:
                # Remove the leading 'N. ' prefix from ordered list items
                def strip_order_prefix(line: str) -> str:
                    return re.sub(r"^\s*\d+\.\s+", "", line)

                node = ParentNode(tag="ol", children=[
                    ParentNode(tag="li", children=text_to_children(strip_order_prefix(line))) for line in block.split("\n")
                ])
                nodes.append(node)

            case BlockType.PARAGRAPH:
                para_text = " ".join(line.strip() for line in block.split("\n") if line.strip() != "")
                node = ParentNode(tag="p", children=text_to_children(para_text))
                nodes.append(node)

    # For simplicity, we will just wrap the entire markdown in a <div> tag
    return ParentNode(tag="div", children=nodes)

def text_to_children(text: str) -> list[LeafNode]:
    """Converts a markdown text string into a list of TextNodes,
    handling splitting for code, images, and links.
    @text: The markdown text to convert
    """
    nodes = text_to_textnodes(text)
    leaves = []
    for node in nodes:
        leaves.append(text_node_to_html_node(node))
    return leaves



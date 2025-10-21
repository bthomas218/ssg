from enum import Enum


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




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

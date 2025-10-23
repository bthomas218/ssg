import re

def extract_markdown_images(text):
    """Extracts markdown image links from the given text.
    @text: The input text containing markdown image links.
    Returns a list of tuples (alt_text, url).
    """
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """Extracts markdown links from the given text.
    @text: The input text containing markdown links.
    Returns a list of tuples (link_text, url).
    """
    pattern = r"(?<!!)\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_title(text):
    """Extracts the first markdown header 1 (#) from the given text.
    @text: The input text in markdown syntax
    Returns the title text without markdown syntax, or raises an error if none is found
    """
    pattern = r"^(#+)\s*(.+)$"
    for line in text.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            return match.group(2).strip()
    raise ValueError("No header 1 found in the provided markdown text.")
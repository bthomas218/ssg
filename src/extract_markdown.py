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
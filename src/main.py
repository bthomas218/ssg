import shutil
from pathlib import Path
from markdown_to_html import markdown_to_html_node
from extract_markdown import extract_title

def rm_cp_files(src: Path, dest: Path):
    """Removes files at dest and copies files from src to dest.
    Args:
        src (Path): Source directory path.
        dest (str): Destination directory path.
    """
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    # Doing without copytree for practice 
    def recurse_copy(s: Path, d: Path):
        for item in s.iterdir():
            target = d / item.name
            if item.is_file():
                print(f"Copying: {item} -> {target}")
                shutil.copy(item, target)
            elif item.is_dir():
                target.mkdir()
                recurse_copy(item, target)
                
    recurse_copy(src, dest)

def generate_page(src: Path, template_path: Path, dest: Path, ):
    print(f"Generating page from {src} using template {template_path} to {dest}")
    markdown, template = None, None
    with src.open("r", encoding="utf-8") as f:
        markdown = f.read()
    with template_path.open("r", encoding="utf-8") as f:
        template = f.read()
    if markdown is None or template is None:
        raise ValueError("Markdown or template content is None")
    root = markdown_to_html_node(markdown)
    html_content = root.to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Content }}", html_content).replace("{{ Title }}", title)
    with dest.open("w", encoding="utf-8") as f:
        f.write(final_html)

def main():
    rm_cp_files(Path("static"), Path("public"))
    generate_page(
        src=Path("content/index.md"),
        template_path=Path("template.html"),
        dest=Path("public/index.html"),
    )
if __name__ == "__main__":
    main()
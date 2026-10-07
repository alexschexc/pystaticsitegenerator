import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )

    with open(from_path, encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, encoding="utf-8") as file:
        template = file.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)

    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(page)

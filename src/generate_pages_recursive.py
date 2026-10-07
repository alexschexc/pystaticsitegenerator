import os

from generate_page import generate_page

def generate_pages_recursive(
        dir_path_content,
        template_path,
        dest_dir_path,
):
    for name in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, name)

        if os.path.isfile(source_path):
            if name.endswith(".md"):
                html_name = os.path.splitext(name)[0] + ".html"
                destination_path = os.path.join(dest_dir_path, html_name)

                generate_page(
                    source_path,
                    template_path,
                    destination_path,
                )
        else:
            destination_directory = os.path.join(dest_dir_path, name)

            generate_pages_recursive(
                source_path,
                template_path,
                destination_directory,
            )

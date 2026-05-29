import os

from blocks import markdown_to_html_node


def extract_title(markdown):
    markdown = markdown.strip()
    split_md = markdown.split("\n")

    title = split_md[0]
    if title[0] != "#":
        raise Exception("You must have an h1 title")
    else:
        title = title.strip("# ")

    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if os.path.isfile(from_path):
        with open(from_path, "r") as f:
            content = f.read()
    else:
        return f'Error : "{from_path}" is not a file'

    if os.path.isfile(template_path):
        with open(template_path, "r") as f:
            template_content = f.read()
    else:
        return f'Error : "{template_path}" is not a file'

    nodes = markdown_to_html_node(content)
    html_str = nodes.to_html()

    title = extract_title(content)

    new_content = template_content.replace("{{ Title }}", title)
    new_content = new_content.replace("{{ Content }}", html_str)

    if os.path.isfile(dest_path):
        with open(dest_path, "w") as f:
            f.write(new_content)
    else:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "x") as f:
            f.write(new_content)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for _, dirs, files in os.walk(dir_path_content):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".md":
                file_path = os.path.join(dir_path_content, file)
                dest_path = os.path.join(dest_dir_path, name + ".html")
                generate_page(file_path, template_path, dest_path)

        for dir in dirs:
            new_dir_path = os.path.join(dir_path_content, dir)
            new_dest_dir = os.path.join(dest_dir_path, dir)

            generate_page_recursive(new_dir_path, template_path, new_dest_dir)

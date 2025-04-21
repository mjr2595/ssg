import os
import shutil

from block_markdown import extract_title, markdown_to_html_node


def copy_directory(src_dir, dest_dir):
    # Remove destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        # Calculate the corresponding destination path
        dest_root = os.path.join(dest_dir, os.path.relpath(root, src_dir))

        # Create directories in destination
        for dir_name in dirs:
            dest_path = os.path.join(dest_root, dir_name)
            os.makedirs(dest_path, exist_ok=True)

        # Copy files
        for file_name in files:
            src_path = os.path.join(root, file_name)
            dest_path = os.path.join(dest_root, file_name)
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_path} -> {dest_path}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # Read template
    with open(template_path, "r") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", str(html_content))

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file_name in files:
            if file_name.endswith(".md"):
                src_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(src_path, dir_path_content)
                dest_path = os.path.join(
                    dest_dir_path, rel_path.replace(".md", ".html")
                )
                generate_page(src_path, template_path, dest_path)


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    # Copy static files
    copy_directory("static", "public")

    # Generate index page
    # generate_page("content/index.md", "template.html", "public/index.html")

    # Generate pages recursively
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()

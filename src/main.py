from textnode import TextNode, TextType, text_node_to_html_node
import os
import shutil
from markdown_blocks import *
import sys


def main():
    basepath = sys.argv[0]
    static = "./static"
    public = "./public"

    print("Cleaning public dir....")
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    static_to_public(public, static)
    generate_pages_recursive("content", "template.html", "docs")

def static_to_public(public, static):
    contents = os.listdir(static)
    for item in contents:
        if os.path.isfile(os.path.join(static,item)):
            shutil.copy(os.path.join(static, item), os.path.join(public, item))
        else:
            os.mkdir(os.path.join(public, item))
            static_to_public(os.path.join(public, item), os.path.join(static, item))

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line
            return title[2:].strip()
    raise Exception
    
def generate_page(from_path, template_path, dest_path, basepath = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r")
    markdown_contents = markdown.read()
    template = open(template_path, "r")
    template_contents = template.read()
    html = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    template_contents = template_contents.replace('href="/', f'href="{basepath}' )
    template_contents = template_contents.replace('src="/', f'src="{basepath}')
    directory = os.path.dirname(dest_path)
    if directory != "":
        os.makedirs(directory, exist_ok=True)
    file = open(dest_path, "w")
    file.write(template_contents)
    file.close()
    markdown.close()
    template.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath = "/"):
    from pathlib import Path
    contents = os.listdir(dir_path_content)
    for item in contents:
        if os.path.isfile(os.path.join(dir_path_content, item)):
            if os.path.join(dir_path_content, item).endswith(".md"):
                md = Path(os.path.join(dest_dir_path, item))
                html = md.with_suffix(".html")
                generate_page(os.path.join(dir_path_content, item), template_path, html)
        else:
            os.mkdir(os.path.join(dest_dir_path, item))
            generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))

main()
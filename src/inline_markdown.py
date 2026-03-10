from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    if len(old_nodes) == 0:
        return None
    for i in old_nodes:
        if i.text_type != TextType.plain_text:
            new_node_list.append(i)
        elif delimiter in i.text:
            if len(i.text.split(delimiter)) % 2 == 0:
                raise Exception ("Invalid Markdown syntax: delimiter not in text")
            else:
                split_text = i.text.split(delimiter)
                for j in range(len(split_text)):
                    if j % 2 == 0:
                        new_node_list.append(TextNode(split_text[j], TextType.plain_text))
                    else:
                        new_node_list.append(TextNode(split_text[j], text_type))               
        else:
            new_node_list.append(i)
    return new_node_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_node_list = []
    if len(old_nodes) == 0:
        return []
    for i in old_nodes:
        if i.text_type != TextType.plain_text:
            new_node_list.append(i)
            continue
        remaining_text = i.text
        images = extract_markdown_images(i.text)
        if len(images) == 0:
            new_node_list.append(i)
            continue
        for alt, url in images:
            split_text = remaining_text.split(f"![{alt}]({url})", 1)
            if split_text[0] != "":
                new_node_list.append(TextNode(split_text[0], TextType.plain_text))
            new_node_list.append(TextNode(alt, TextType.image, url))
            remaining_text = split_text[1]
        if remaining_text != "":
            new_node_list.append(TextNode(remaining_text, TextType.plain_text))
    return new_node_list

def split_nodes_link(old_nodes):
    new_node_list = []
    if len(old_nodes) == 0:
        return []
    for i in old_nodes:
        if i.text_type != TextType.plain_text:
            new_node_list.append(i)
            continue
        remaining_text = i.text
        links = extract_markdown_links(i.text)
        if len(links) == 0:
            new_node_list.append(i)
            continue
        for alt, url in links:
            split_text = remaining_text.split(f"[{alt}]({url})", 1)
            if split_text[0] != "":
                new_node_list.append(TextNode(split_text[0], TextType.plain_text))
            new_node_list.append(TextNode(alt, TextType.link, url))
            remaining_text = split_text[1]
        if remaining_text != "":
            new_node_list.append(TextNode(remaining_text, TextType.plain_text))
    return new_node_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.plain_text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold_text)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic_text)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code_text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
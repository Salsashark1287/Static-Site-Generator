from htmlnode import *
from textnode import *
from inline_markdown import *


def markdown_to_html_node(markdown):

    def text_to_children(text):
        nodes = text_to_textnodes(text)
        children = []
        for node in nodes:
            html_node = text_node_to_html_node(node)
            children.append(html_node)
        return children

    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.heading:
            h = 0
            for i in block:
                if i == "#":
                    h += 1
                else:
                    break
            text = block[h + 1:]
            tag = f"h{h}"
            block_nodes.append(ParentNode(tag, text_to_children(text)))
        elif block_type == BlockType.paragraph:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.strip())
                paragraph = " ".join(cleaned_lines)
            block_nodes.append(ParentNode("p", text_to_children(paragraph)))
        elif block_type == BlockType.code:
            text = block[3:-3].strip()
            lines = text.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.strip())
            content = "\n".join(cleaned_lines)
            content += "\n"
            code_node = ParentNode("code", [LeafNode(None, content)])
            block_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.ordered_list:
            list_nodes = []
            lines = block.split("\n")
            for item in lines:
                space_index = item.find(" ")
                item = item[space_index + 1:]
                list_nodes.append(ParentNode("li", text_to_children(item)))
            block_nodes.append(ParentNode("ol", list_nodes))
        elif block_type == BlockType.unordered_list:
            list_nodes = []
            lines = block.split("\n")
            for item in lines:
                item = item[2:]
                list_nodes.append(ParentNode("li", text_to_children(item)))
            block_nodes.append(ParentNode("ul", list_nodes))
        elif block_type == BlockType.quote:
            list_nodes = []
            lines = block.split("\n")
            cleaned_list = []
            for line in lines:
                cleaned_list.append(line[2:])
            text = " ".join(cleaned_list)
            block_nodes.append(ParentNode("blockquote", text_to_children(text)))
    return ParentNode("div",block_nodes)

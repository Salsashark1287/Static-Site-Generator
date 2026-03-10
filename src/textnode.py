from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode

class TextType(Enum):
    plain_text = "text"
    bold_text = "bold"
    italic_text = "italic"
    code_text = "code"
    link = "link"
    image = "image"

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type.value}, {self.url})")

def text_node_to_html_node(text_node):
    from htmlnode import LeafNode
    if text_node.text_type == TextType.plain_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.bold_text:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.italic_text:
        return LeafNode("i", text_node.text)
    elif text_node.text_type ==  TextType.code_text:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.image:
        return LeafNode("img", "", {"src": text_node.url,"alt": text_node.text})
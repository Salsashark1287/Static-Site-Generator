import unittest

from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold_text)
        node2 = TextNode("This is a text node", TextType.bold_text)
        node3 = TextNode("This is test node", TextType.bold_text)
        node4 = TextNode("this is a test node", TextType.bold_text)
        node5 = TextNode("This is a text node", TextType.italic_text)
        node6 = TextNode("This is a text node", TextType.bold_text, "www.google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node3, node6)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.plain_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node") 

if __name__ == "__main__":
    unittest.main()
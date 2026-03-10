import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Paragraph Text", None, {"href": "https://www.facebook.com"})
        node2 = HTMLNode("p", "Paragraph Text", None, {"href": "https://www.facebook.com"})
        node3 = HTMLNode("h1", "Header Text", None, {"href": "https://www.facemasher.co.uk", "target": "_blank"})
        node4 = HTMLNode("a")
        node5 = HTMLNode("a", "Link Text")
        node6 = HTMLNode("h2", "Header Text")
        node7 = LeafNode("b", "This is BOLD", {"href": "https://www.BeBold.com"})
        node8 = LeafNode("i", "Look at my Italics!", {"href": "https://www.Italicsaresexy.com"})
        node9 = LeafNode(None, "Watch me Link, Watch me Nae Nae", {"href": "https://www.Cringefest.com"})
        node.props_to_html()
        node2.props_to_html()
        node3.props_to_html()
        self.assertEqual(node7.to_html(), '<b href="https://www.BeBold.com">This is BOLD</b>')
        self.assertNotEqual(node8.to_html(), "Look at my Italics")
        self.assertEqual(node9.to_html(), "Watch me Link, Watch me Nae Nae")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
if __name__ == "__main__":
    unittest.main()
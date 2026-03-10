import unittest
from inline_markdown import *
from textnode import *

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node1 = [TextNode("Test `code` Test", TextType.plain_text)]
        node2 = [TextNode("This text is **bold** and so is **this**", TextType.plain_text)]
        node3 = [TextNode("This text is _Italic_, see?", TextType.plain_text)]

        answer1 = split_nodes_delimiter(node1, "`", TextType.code_text)
        answer2 = split_nodes_delimiter(node2, "**", TextType.bold_text)
        answer3 = split_nodes_delimiter(node3, "_", TextType.italic_text)

        expected1 = [
            TextNode("Test ", TextType.plain_text),
            TextNode("code", TextType.code_text),
            TextNode(" Test", TextType.plain_text),
        ]

        expected2 = [
            TextNode("This text is ", TextType.plain_text),
            TextNode("bold", TextType.bold_text),
            TextNode(" and so is ", TextType.plain_text),
            TextNode("this", TextType.bold_text),
            TextNode("", TextType.plain_text),
        ]

        expected3 = [
            TextNode("This text is ", TextType.plain_text),
            TextNode("Italic", TextType.italic_text),
            TextNode(", see?", TextType.plain_text),
        ]

        self.assertEqual(answer1, expected1)
        self.assertEqual(answer2, expected2)
        self.assertEqual(answer3, expected3)
        self.assertNotEqual(answer1, expected3)
        self.assertNotEqual(answer3, expected1)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertNotEqual([("img", "https://i.IMGUR.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This text has a [link](https://www.wazup.com)"
        )
        self.assertListEqual([("link", "https://www.wazup.com")], matches)
        self.assertNotEqual([("link", "(https://www.wazup.com)")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.plain_text),
            TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.plain_text),
            TextNode(
                "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertNotEqual(
        [
            TextNode("This is text with an ", TextType.plain_text),
            TextNode(" and another ", TextType.plain_text),
            TextNode(
                "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.plain_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.plain_text),
            TextNode("link", TextType.link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.plain_text),
            TextNode(
                "second link", TextType.link, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )










if __name__ == "__main__":
    unittest.main()
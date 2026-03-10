import unittest
from block_markdown import *
from htmlnode import *
from textnode import *

class TestBlockMarkdown(unittest.TestCase):
    def test_block_markdown(self):
        markdown1 = """###This is an _italic_ header

This is a body paragraph and it is **bold**

This is the footer, a good place for links like [this one](https://www.whatupwiththat.com)"""

        markdown2 = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

        blocks2 = markdown_to_blocks(markdown2)
        self.assertEqual(
            blocks2,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        blocks1 = markdown_to_blocks(markdown1)
        self.assertEqual(
            blocks1,
            [
                "###This is an _italic_ header",
                "This is a body paragraph and it is **bold**",
                "This is the footer, a good place for links like [this one](https://www.whatupwiththat.com)",
            ],
        )

    def test_blocktype(self):
        block1 = "- This is a list\n- with items"
        block2 = "1. One \n2. Two\n3. Three"
        block3 = "### This is an _italic_ header"
        block4 = "```\npi=3.14159\n```"

        blocktype1 = block_to_block_type(block1)
        blocktype2 = block_to_block_type(block2)
        blocktype3 = block_to_block_type(block3)
        blocktype4 = block_to_block_type(block4)
        
        self.assertEqual(
            blocktype1,
            BlockType.unordered_list
        )

        self.assertEqual(
            blocktype2,
            BlockType.ordered_list
        )

        self.assertEqual(
            blocktype3,
            BlockType.heading
        )

        self.assertEqual(
            blocktype4,
            BlockType.code
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
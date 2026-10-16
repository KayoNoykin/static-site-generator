import unittest
from functions import *
from textnode import TextNode, TextType, BlockType

class TestSplitFuncs(unittest.TestCase):
    def test_bold(self):
        test = split_nodes_delimiter([TextNode("this is **bold** text", TextType.TEXT)], "**", TextType.BOLD)
        expected = [TextNode("this is ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT)]
        self.assertEqual(test, expected)
        
    def test_italic(self):
        test = split_nodes_delimiter([TextNode("this is _italic_ text", TextType.TEXT)], "_", TextType.ITALIC)
        expected = [TextNode("this is ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.TEXT)]

    def test_code(self):
        test = split_nodes_delimiter([TextNode("this is `code` text", TextType.TEXT)], "`", TextType.CODE)
        expected = [TextNode("this is ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" text", TextType.TEXT)]

    def test_error(self):
        with self.assertRaises(Exception):
            test = split_nodes_delimiter([TextNode("this is `invalid text", TextType.TEXT)], "`", TextType.CODE)
        
    def test_list(self):
            test = split_nodes_delimiter([TextNode("this is **bold** text", TextType.TEXT), 
                                          TextNode("this is **also bold** text", TextType.TEXT), 
                                          TextNode("this is _italic_ text", TextType.TEXT)], "**", TextType.BOLD)
            expected = [TextNode("this is ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT),
                        TextNode("this is ", TextType.TEXT), TextNode("also bold", TextType.BOLD), TextNode(" text", TextType.TEXT),
                        TextNode("this is _italic_ text", TextType.TEXT)]
            self.assertEqual(test, expected)
            
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        
    def test_split_images_error(self):
        node = TextNode(
            "This is text with an ![image(https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        with self.assertRaises(Exception, msg="invalid markdown syntax"):
            split_nodes_image([node])        
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )
        
    def test_split_links_error(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link(https://www.youtube.com)",
            TextType.TEXT,
        )
        with self.assertRaises(Exception, msg="invalid markdown syntax"):
            split_nodes_link([node])

    def test_split_images_with_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_links_with_image(self):
        node = TextNode(
            "This is text with an ![image(https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )
        
    def test_split_image_with_both(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://www.boot.dev)", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_link_with_both(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes,
        )

    def test_split_image_mult(self):
        node1 = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        node2 = TextNode(
                    "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
                    TextType.TEXT,
                )
        node3 = TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
                    TextType.TEXT,
                )
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://www.boot.dev)", TextType.TEXT)
            ],
            new_nodes
        )
        
    def test_split_link_mult(self):
        node1 = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        node2 = TextNode(
                    "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
                    TextType.TEXT,
                )
        node3 = TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
                    TextType.TEXT,
                )
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.youtube.com"),
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )
           
class TestExtractFuncs(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ![second_image](https://i.imgur.com/zffcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("second_image", "https://i.imgur.com/zffcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
        
    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev) and a [second_link](https://www.youtube.com)"
        )
        self.assertListEqual([("link", "https://www.boot.dev"), ("second_link", "https://www.youtube.com")], matches)
        
class TestTextToNode(unittest.TestCase):
    def test_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )
        
    def test_error(self):
        text = "This is **text* with an _italic_ word and a `code block and an ![obi wan image]https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        with self.assertRaises(Exception, msg="invalid markdown syntax"):
            text_to_textnodes(text)
            
class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )
        
    def test_BlockType_HEADING(self):
        block = "###### This is a heading block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_BlockType_CODE(self):
        block = "```\nThis is a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_BlockType_QUOTE(self):
        block = ">this is a quote\n> this is also a quote but with a space\n>this is a third quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_BlockType_UNORDERED_LIST(self):
        block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_BlockType_ORDERED_LIST(self):
        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        
    def test_BlockType_PARAGRAPH(self):
        block = "- This is the first list item in a list block\n This is not a list item\n- This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
class TestBlockToHTML(unittest.TestCase):
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
        
    def test_heading(self):
        md = """
###### This is a heading
This is text that should be _italic_, **bold** and `code` respectively.

### This is a smaller heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a heading\nThis is text that should be <i>italic</i>, <b>bold</b> and <code>code</code> respectively.</h6><h3>This is a smaller heading</h3></div>",
        )
        
    def test_unordered_list(self):
        md = """
- this is a **bold** list item
- this is an _italic_ list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is a <b>bold</b> list item</li><li>this is an <i>italic</i> list item</li></ul></div>",
        )
        
    def test_ordered_list(self):
        md = """
1. this is the **first** list item
2. this is the _second_ list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is the <b>first</b> list item</li><li>this is the <i>second</i> list item</li></ol></div>",
        )
        
    def test_quote(self):
        md = """
>this is a **bold** quote
> this is an _italic_ quote

>this is a seperate blockquote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a <b>bold</b> quote\nthis is an <i>italic</i> quote</blockquote><blockquote>this is a seperate blockquote</blockquote></div>",
        )
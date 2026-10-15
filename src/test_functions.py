import unittest
from functions import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitFunc(unittest.TestCase):
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
        
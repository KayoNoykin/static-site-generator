import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import *

#TextNode tests
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Ut eleifend tempus vulputate. Vivamus.", TextType.ITALIC)
        node2 = TextNode("Lorem ipsum dolor sit amet.", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_eq_type(self):
        node = TextNode("Lorem ipsum dolor sit amet.", TextType.TEXT)
        node2 = TextNode("Lorem ipsum dolor sit amet.", "text")
        self.assertEqual(node, node2)
       
    def test_not_eq_type(self):
        node = TextNode("Lorem ipsum dolor sit amet.", TextType.TEXT)
        node2 = TextNode("Lorem ipsum dolor sit amet.", TextType.CODE)
        self.assertNotEqual(node, node2)
        
    def test_eq_url(self):
        node = TextNode("Lorem ipsum dolor sit amet.", "text", url=None)
        node2 = TextNode("Lorem ipsum dolor sit amet.", "text")
        self.assertEqual(node, node2)
        
    def test_not_eq_url(self):
        node = TextNode("This is a link to boot.dev", TextType.LINK, "http://boot.dev")
        node2 = TextNode("This is a link to boot.dev", TextType.LINK, "http://bootdev")
        self.assertNotEqual(node, node2)

#tests for text_note_to_html_node (add more)      
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is anchor text", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is anchor text")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        
    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, url="generic.image.link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "generic.image.link", "alt": "This is alt text"})
                
        
if __name__ == "__main__":
    unittest.main()
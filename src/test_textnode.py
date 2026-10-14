import unittest
from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
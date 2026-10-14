import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode()
        test = node.props_to_html()
        expected = ""
        self.assertEqual(test, expected)
        
    def test_props_1(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        test = node.props_to_html()
        expected = ' href="https://www.google.com"'
        self.assertEqual(test, expected)
        
    def test_props_2(self):
        node = HTMLNode(props={
    "href": "https://www.google.com",
    "target": "_blank",
})
        test = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(test, expected)
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)
        
    def test_leaf_error(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()
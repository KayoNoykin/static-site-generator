import unittest
from htmlnode import HTMLNode

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
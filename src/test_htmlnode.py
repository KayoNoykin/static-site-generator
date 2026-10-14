import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

#HTMLNode tests
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
        
# LeadNode tests
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
            
#ParentNode tests (add more)
class TestParentNode(unittest.TestCase):
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
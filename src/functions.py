from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
        split = node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise Exception("invalid markdown syntax")
        for i in range(0, len(split)):
            if i % 2 == 0:
                output.append(TextNode(split[i], TextType.TEXT))
            if i % 2 != 0:
                output.append(TextNode(split[i], text_type))
    return output

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
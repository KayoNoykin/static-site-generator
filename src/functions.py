from textnode import TextNode, TextType
import re

def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
        elif "![" not in node.text:
            output.append(node)
        else:
            split = re.split(r"(!\[.*?\))", node.text)
            if len(re.split(r"[!\[]|\]|\(|\)", node.text)) % 2 == 0:
                raise Exception("invalid markdown syntax")
            args: list[tuple] = extract_markdown_images(node.text)
            for i in range(0, len(split)):
                if i % 2 == 0:
                    if split[i] != "":
                        output.append(TextNode(split[i], TextType.TEXT))
                if i % 2 != 0:
                    output.append(TextNode(args[i // 2][0], TextType.IMAGE, args[i // 2][1]))
    return output

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
        elif " [" not in node.text:
            output.append(node)
        else:
            split = re.split(r"(\[.*?\))", node.text)
            if len(re.split(r"\[|\]|\(|\)", node.text)) % 2 == 0:
                raise Exception("invalid markdown syntax")
            args: list[tuple] = extract_markdown_links(node.text)
            for i in range(0, len(split)):
                if i % 2 == 0:
                    if split[i] != "":
                        output.append(TextNode(split[i], TextType.TEXT))
                if i % 2 != 0:
                    output.append(TextNode(args[i // 2][0], TextType.LINK, args[i // 2][1]))
    return output
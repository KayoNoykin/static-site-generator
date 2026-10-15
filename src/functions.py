from textnode import TextNode, TextType, BlockType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
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
        else:
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
            if len(re.split(r"!\[|\[|\]|\(|\)", node.text)) % 2 == 0:
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
            split = re.split(r"(?<!!)(\[.*?\))", node.text)
            if len(re.split(r"!\[|\[|\]|\(|\)", node.text)) % 2 == 0:
                raise Exception("invalid markdown syntax")
            args: list[tuple] = extract_markdown_links(node.text)
            for i in range(0, len(split)):
                if i % 2 == 0:
                    if split[i] != "":
                        output.append(TextNode(split[i], TextType.TEXT))
                if i % 2 != 0:
                    output.append(TextNode(args[i // 2][0], TextType.LINK, args[i // 2][1]))
    return output

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_image(code)
    link = split_nodes_link(image)
    return link

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    while "" in blocks:
        blocks.remove("")
    stripped = list(map(str.strip, blocks))
    return stripped

def block_to_block_type(block: str) -> BlockType:
    if any(block.startswith(f"{'#' * i} ") for i in range(1,7)):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    else:
        lines = block.split("\n")
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        elif all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
        elif all(lines[i - 1].startswith(f"{i}. ") for i in range(1, len(lines))):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[LeafNode]:
    textnodes = text_to_textnodes(text)
    leafnodes = []
    for node in textnodes:
        leafnodes.append(text_node_to_html_node(node))
    return leafnodes
    
def block_to_html_node(block: str) -> ParentNode:
    type = block_to_block_type(block)
    match type:
        case BlockType.PARAGRAPH:
            tag = "p"
            text = block #edit this to change "\n" -> " "?
            children = text_to_children(text)
        case BlockType.HEADING:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.UNORDERED_LIST:
            pass
        case BlockType.ORDERED_LIST:
            pass
        case BlockType.CODE:
            pass
        case _:
            raise Exception("invalid block type")
    return ParentNode(tag, children)
            

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        
        
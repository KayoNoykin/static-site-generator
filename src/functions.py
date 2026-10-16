from textnode import TextNode, TextType, BlockType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import re, os, shutil

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
        elif all(lines[i - 1].startswith(f"{i}. ") for i in range(1, len(lines) + 1)):
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
            text = block.replace("\n", " ")
            children = text_to_children(text)
        case BlockType.HEADING:
            for i in range(1,7):
                if block.startswith(f"{'#' * i} "):
                    tag = f"h{i}"
            text = block.strip("# ")
            children = text_to_children(text)
        case BlockType.QUOTE:
            lines = block.split("\n")
            stripped = []
            for line in lines:
                stripped.append(line.lstrip("> "))
            text = "\n".join(stripped)
            children = text_to_children(text)
            tag = "blockquote"
        case BlockType.UNORDERED_LIST:
            tag = "ul"
            lines = block.split("\n")
            stripped = []
            children = []
            for line in lines:
                stripped.append(line.lstrip("- "))
            for line in stripped:
                grandchildren = text_to_children(line)
                child = ParentNode("li", grandchildren)
                children.append(child)
        case BlockType.ORDERED_LIST:
            tag = "ol"
            lines = block.split("\n")
            stripped = []
            children = []
            for i in range(1, len(lines) + 1):
                stripped.append(lines[i - 1].lstrip(f"{i}. "))
            for line in stripped:
                grandchildren = text_to_children(line)
                child = ParentNode("li", grandchildren)
                children.append(child)
        case BlockType.CODE:
            text = block.lstrip("```\n").rstrip("```")
            text_node = TextNode(text, TextType.CODE)
            children = [text_node_to_html_node(text_node)]
            tag = "pre"
        case _:
            raise Exception("invalid block type")
    return ParentNode(tag, children)
            

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        node = block_to_html_node(block)
        block_nodes.append(node)
    div_node = ParentNode("div", block_nodes)
    return div_node

def copy_directory(source: str, destination: str) -> None:
    if os.path.exists(source) == False:
        raise Exception("invalid source path")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    dir_contents = os.listdir(source)
    for item in dir_contents:
        path = os.path.join(source, item)
        if os.path.isfile(path):
            # print(path)
            shutil.copy(path, destination)
        if os.path.isdir(path):
            new_dst = os.path.join(destination, item)
            # print(new_dst)
            copy_directory(path, new_dst)
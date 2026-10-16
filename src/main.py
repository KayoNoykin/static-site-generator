from textnode import TextNode, TextType
from functions import copy_directory, generate_page
import os

def main():
    copy_directory("./static", "./public") 
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()
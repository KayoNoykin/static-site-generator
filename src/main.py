from textnode import TextNode, TextType
from functions import copy_directory, generate_pages_recursive
import os

def main():
    copy_directory("./static", "./public") 
    generate_pages_recursive("./content", "./template.html", "./public")


main()
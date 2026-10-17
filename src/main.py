from textnode import TextNode, TextType
from functions import copy_directory, generate_pages_recursive
import sys

def main():
    basepath = sys.argv
    copy_directory("./static", "./docs") 
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


main()
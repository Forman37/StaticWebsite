from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("The text type is not a supported type")

    tag = ""
    props = {}
    match text_node.text_type.value:
        case "text":
            tag = None
        case "bold":
            tag = "b"
        case "italic":
            tag = "i"
        case "code":
            tag = "code"
        case "link":
            tag = "a"
            props["href"] = text_node.url
        case "image":
            tag = "img"
            props["src"] = text_node.url
            props["alt"] = text_node.text
            text_node.text = ""
        case _:
            tag = "error"

    return LeafNode(tag, text_node.text, props)

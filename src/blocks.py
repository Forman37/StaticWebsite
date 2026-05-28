from enum import Enum
from re import split
from typing import Text

from htmlnode import HTMLNode, LeafNode, ParentNode
from parser import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    returnBlocks = []
    for block in blocks:
        if block == "":
            continue
        returnBlocks.append(block.strip())
    return returnBlocks


def block_to_block_type(block):
    if block[0] == "#":
        return BlockType.HEADING
    if (
        block[0] == block[1] == block[2] == "`"
        and block[3] == "\n"
        and block[len(block) - 1]
        == block[len(block) - 2]
        == block[len(block) - 3]
        == "`"
    ):
        return BlockType.CODE

    splitBlock = block.split("\n")
    quote = False
    uoList = False
    oList = False
    incrementor = 0
    for part in splitBlock:
        if part[0] == ">":
            if not uoList or not oList:
                quote = True
            else:
                return BlockType.PARAGRAPH
        elif part[0] == "-" and part[1] == " ":
            if not quote or not oList:
                uoList = True
            else:
                return BlockType.PARAGRAPH
        elif part[0].isdigit() and part[1] == "." and part[2] == " ":
            if not quote or uoList:
                incrementor += 1
                if int(part[0]) == incrementor:
                    oList = True
            else:
                return BlockType.PARAGRAPH
        else:
            return BlockType.PARAGRAPH

    if quote:
        return BlockType.QUOTE
    elif uoList:
        return BlockType.ULIST
    elif oList:
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parentHTMLNode = ParentNode("div", [])
    for block in blocks:
        if block == "":
            continue
        block_type = block_to_block_type(block)
        match block_type.value:
            case "paragraph":
                children_nodes = text_to_children(block)
                parent_node = ParentNode("p", children_nodes)
                parentHTMLNode.children.append(parent_node)
            case "heading":
                h_num = count_header(block)
                block = block.strip("# ")
                children_nodes = text_to_children(block)
                parent_node = ParentNode(h_num, children_nodes)
                parentHTMLNode.children.append(parent_node)
            case "code":
                splitText = block.split("```")
                text = splitText[1]
                text = text.lstrip("\n ")
                t_node = TextNode(text, TextType.CODE)
                c_node = text_node_to_html_node(t_node)
                parent_node = ParentNode("pre", [c_node])
                parentHTMLNode.children.append(parent_node)
            case "unordered_list":
                split_list = block.split("\n")
                children_nodes = divide_list(split_list)

                parent_node = ParentNode("ul", children_nodes)
                parentHTMLNode.children.append(parent_node)
            case "ordered_list":
                split_list = block.split("\n")
                children_nodes = divide_list(split_list)

                parent_node = ParentNode("ol", children_nodes)
                parentHTMLNode.children.append(parent_node)

            case "quote":
                block_text = block.split("> ")
                text_to_send = ""
                for text in block_text:
                    text_to_send += " " + text.strip()

                text_to_send = text_to_send.replace("\n", " ")
                text_to_send = text_to_send.strip()
                children_nodes = text_to_children(text_to_send)
                parent_node = ParentNode("blockquote", children_nodes)
                parentHTMLNode.children.append(parent_node)

    # print("\n\n\n\n\n\n")
    # print("\n\n\nPRINTING!!")
    # print(parentHTMLNode)
    # print("\n\n\n")
    # print(parentHTMLNode.to_html())
    # print("\n\n\n")

    return parentHTMLNode


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        new_node = text_node_to_html_node(node)
        html_nodes.append(new_node)
    return html_nodes


def divide_list(texts):
    return_nodes = []
    for text in texts:
        if text[1] == " ":
            text = text[2:]
        elif text[1] == ".":
            if text[2] == " ":
                text = text[3:]
            else:
                text = text[2:]
        else:
            text = text[1:]
        text_node = text_to_textnodes(text)

        html_nodes = []
        for node in text_node:
            new_node = text_node_to_html_node(node)
            html_nodes.append(new_node)
        return_nodes.append(ParentNode("li", html_nodes))

    return return_nodes


def count_header(text):
    count = 0
    for char in text:
        if char == "#":
            count += 1
        else:
            break

    return "h" + str(count)

from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue

        splitVals = node.text.split(delimiter)
        if len(splitVals) % 2 <= 0:
            raise Exception("There is no closing part for that text type")

        active = False
        for val in splitVals:
            if val == "":
                active = True
            else:
                if active:
                    node = TextNode(val, text_type)
                    return_nodes.append(node)
                    active = False
                else:
                    node = TextNode(val, TextType.TEXT)
                    return_nodes.append(node)
                    active = True
    return return_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    retNodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            retNodes.append(node)
            continue
        image_matches = extract_markdown_images(node.text)
        if len(image_matches) == 0:
            retNodes.append(TextNode(node.text, TextType.TEXT))
            continue

        leftoverStr = node.text
        splits = []
        for alt, image in image_matches:
            splits = leftoverStr.split(f"![{alt}]({image})", 1)
            leftoverStr = ""
            firstDone = False
            for split in splits:
                if firstDone:
                    leftoverStr += split
                else:
                    if split != "":
                        retNodes.append(TextNode(split, TextType.TEXT))
                    retNodes.append(TextNode(alt, TextType.IMAGE, image))
                    firstDone = True

        if splits[len(splits) - 1] != "":
            retNodes.append(TextNode(splits[len(splits) - 1], TextType.TEXT))
    return retNodes


def split_nodes_link(old_nodes):
    retNodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            retNodes.append(node)
            continue
        link_matches = extract_markdown_links(node.text)
        if len(link_matches) == 0:
            retNodes.append(TextNode(node.text, TextType.TEXT))
            continue

        leftoverStr = node.text
        splits = []
        for alt, link in link_matches:
            splits = leftoverStr.split(f"[{alt}]({link})", 1)
            leftoverStr = ""
            firstDone = False
            for split in splits:
                if firstDone:
                    leftoverStr += split
                else:
                    if split != "":
                        retNodes.append(TextNode(split, TextType.TEXT))
                    retNodes.append(TextNode(alt, TextType.LINK, link))
                    firstDone = True

        if splits[len(splits) - 1] != "":
            retNodes.append(TextNode(splits[len(splits) - 1], TextType.TEXT))
    return retNodes


def text_to_textnodes(text):
    node_iter_1 = TextNode(text, TextType.TEXT)
    node_iter_2 = split_nodes_delimiter([node_iter_1], "**", TextType.BOLD)
    node_iter_3 = split_nodes_delimiter(node_iter_2, "_", TextType.ITALIC)
    node_iter_4 = split_nodes_delimiter(node_iter_3, "`", TextType.CODE)
    node_iter_5 = split_nodes_image(node_iter_4)
    node_iter_6 = split_nodes_link(node_iter_5)

    return node_iter_6

from block_to_block_type import BlockType, block_to_block_type
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node

def text_to_children(text):
    return [
        text_node_to_html_node(node)
        for node in text_to_textnodes(text)
    ]

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        text = block.replace("\n", " ")
        return ParentNode("p", text_to_children(text))

    if block_type == BlockType.HEADING:
        hashes, text = block.split(" ", 1)
        return ParentNode(f"h{len(hashes)}", text_to_children(text))

    if block_type == BlockType.CODE:
        fence = "`" * 3
        text = block[len(fence) + 1:-len(fence)]
        code_node = text_node_to_html_node(
            TextNode(text, TextType.CODE)
        )
        return ParentNode("pre", [code_node])

    if block_type == BlockType.QUOTE:
        text = " ".join(
            line[1:].strip()
            for line in block.split("\n")
        )
        return ParentNode("blockquote", text_to_children(text))

    if block_type == BlockType.UNORDERED_LIST:
        items = [
            ParentNode("li", text_to_children(line[2:]))
            for line in block.split("\n")
        ]
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        items = [
            ParentNode("li", text_to_children(line.split(". ", 1)[1]))
            for line in block.split("\n")
        ]
        return ParentNode("ol", items)

    raise ValueError(f"Unsupported block type: {block_type}")

def markdown_to_html_node(markdown):
    children = [
        block_to_html_node(block)
        for block in markdown_to_blocks(markdown)
    ]
    return ParentNode("div", children)

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    for level in range(1, 7):
        if block.startswith("#" * level + " "):
            return BlockType.HEADING

    fence = "`" * 3
    if block.startswith(fence + "\n") and block.endswith(fence):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{number}. ") for number, line in enumerate(lines, start = 1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = []

    for block in markdown.split("\n\n"):
        stripped_block = block.strip()

        if stripped_block:
            blocks.append(stripped_block)

    return blocks

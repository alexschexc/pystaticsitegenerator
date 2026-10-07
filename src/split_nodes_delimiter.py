from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown: unmatched delimiter {delimiter!r}")

        for idx, section in enumerate(sections):
            if section == "":
                continue
            if idx % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))


    return new_nodes

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None , children: list["HTMLNode"] | None, props: dict[str, str] | None = None):
        super().__init__(tag,None,children,props)

    def __repr__(self):
        return f'##########\ntag: {self.tag} \nchildren: {self.children} \nprops: {self.props} \n############'

    def to_html(self):
        if not self.tag:
            raise ValueError()

        if self.children is None:
            raise ValueError("Where's me baby back ribs! (no children declared)")
        children_html = ""

        for child in self.children:
            children_html += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None , value: str | None, props: dict[str, str] | None = None):
        super().__init__(tag,value,None,props)

    def __repr__(self):
        return f'##########\ntag: {self.tag} \nvalue: {self.value} \nprops: {self.props} \n############'

    def to_html(self):
        if not self.value:
            raise ValueError()

        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

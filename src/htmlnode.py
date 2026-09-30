
class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f'##########\ntag: {self.tag} \nvalue: {self.value} \nchildren: {self.children} \nprops: {self.props} \n############'

    def to_html(self):
        raise NotImplementedError()


    def props_to_html(self):
        result = ""

        if not self.props:
            return result

        for name, setting in self.props.items():
            result +=f' {name}="{setting}"'
        return result

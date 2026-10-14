class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        output = f""
        for key in self.props.keys():
            output = output + f' {key}="{self.props[key]}"'
        return output
    
    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"
    
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict = None):
        super().__init__(tag, value, props=props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("leaf nodes must have a value")
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
            return f"HTMLNode(tag = {self.tag}, value = {self.value}, props = {self.props})"
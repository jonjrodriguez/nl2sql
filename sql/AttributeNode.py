from SQLNodeType import SQLNodeType
from SQLNodeMultiChild import SQLNodeMultiChild


class AttributeNode(SQLNodeMultiChild):
    """
    Could have multiple children. Part of a larger tree.

    attribute_node = AttributeNode()
    attribute_node.to_sql()
    => *

    attribute_node = AttributeNode('names')
    attribute_node.to_sql()
    => names

    """
    def __init__(self, label = "*", child = None):
        super(AttributeNode,self).__init__(SQLNodeType.ATTRIBUTE_NODE, label)
        self.add_child(child)

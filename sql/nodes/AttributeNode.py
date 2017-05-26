from sql.nodes.SQLNodeType import SQLNodeType
from sql.nodes.SQLNode import SQLNode


class AttributeNode(SQLNode):
    """
    Could have multiple children. Part of a larger tree.

    attribute_node = AttributeNode()
    attribute_node.to_sql()
    => *

    attribute_node = AttributeNode('names')
    attribute_node.to_sql()
    => names

    """
    def __init__(self, label="*", child=None, parent=None):
        super(AttributeNode, self).__init__(SQLNodeType.ATTRIBUTE_NODE, label, "select")

        self.add_child(child)
        self.add_parent(parent)

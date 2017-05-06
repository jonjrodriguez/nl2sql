from SQLNode import SQLNode
from SQLNodeType import SQLNodeType


class AttributeNode(SQLNode):
    """
    Should only have one child (belongs to one table). Part of a larger tree.

    attribute_node = AttributeNode()
    attribute_node.to_sql()
    => *

    attribute_node = AttributeNode('names')
    attribute_node.to_sql()
    => names

    """
    def __init__(self, label = "*", child = None):
        SQLNode.__init__(self, SQLNodeType.ATTRIBUTE_NODE, label, child)

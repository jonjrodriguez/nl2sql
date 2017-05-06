from SQLNode import SQLNode
from SQLNodeType import SQLNodeType


class ValueNode(SQLNode):
    """
    Can only have one child, does not require a label.

    value_node = ValueNode('hannan')
    value_node.to_sql()
    => hannan

    value_node = ValueNode()
    value_node.to_sql()
    => 

    """
    def __init__(self, label = "", child = None):
        SQLNode.__init__(self, SQLNodeType.VALUE_NODE, label, child)


print ValueNode("students").to_sql()

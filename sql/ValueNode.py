from sql.SQLNode import SQLNode
from sql.SQLNodeType import SQLNodeType


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
    def __init__(self, label="", child=None, parent=None):
        super(ValueNode, self).__init__(SQLNodeType.VALUE_NODE, label)

        self.add_child(child)
        self.add_parent(parent)

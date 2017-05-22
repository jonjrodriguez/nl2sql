from sql import SQLNode
from sql import SQLNodeType


class LimitNode(SQLNode):
    """
    Requires the label be an integer.

    limit_node = LimitNode(3)
    limit_node.to_sql()
    => LIMIT 3

    limit_node = LimitNode()
    => throws error

    """
    def __init__(self, label, child=None, parent=None):
        try:
            label = int(label)
        except ValueError:
            raise Exception("Limit node label must be a number")

        super(LimitNode, self).__init__(SQLNodeType.LIMIT_NODE, label)

        self.add_child(child)
        self.add_parent(parent)


    def to_sql(self):
        return "LIMIT %s" % self.label

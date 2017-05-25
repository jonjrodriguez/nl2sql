from sql.nodes.SQLNode import SQLNode
from sql.nodes.SQLNodeType import SQLNodeType


class FunctionNode(SQLNode):
    def __init__(self, child=None, func_type=None, parent=None):
        super(FunctionNode, self).__init__(SQLNodeType.FUNCTION_NODE, "COUNT(*)", "select")

        self.add_child(child)
        self.add_parent(parent)

        self.func_type = func_type


    def __repr__(self):
        return "%s['%s']" % (type(self).__name__, self.func_type)

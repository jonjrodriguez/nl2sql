from sql.SQLNode import SQLNode
from sql.SQLNodeType import SQLNodeType


class FunctionNode(SQLNode):
    def __init__(self, child=None, func_type=None, parent=None):
        super(FunctionNode, self).__init__(SQLNodeType.FUNCTION_NODE, "function")

        self.add_child(child)
        self.add_parent(parent)

        self.func_type = func_type

    def to_sql(self):
        column_name = "*"
        if self.child is not None and self.child.type is SQLNodeType.ATTRIBUTE_NODE:
            column_name = self.child.to_sql()

        if self.func_type is None:
            return column_name

        return self.func_type + "(" + column_name + ")"

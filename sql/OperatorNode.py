from sql.SQLNode import SQLNode
from sql.SQLNodeType import SQLNodeType
from sql.OperatorNodeType import OperatorNodeType


class OperatorNode(SQLNode):
    def __init__(self, child=None, parent=None, operator_type=OperatorNodeType.EQUAL):
        super(OperatorNode, self).__init__(SQLNodeType.OPERATOR_NODE, "operator")

        self.add_child(child)
        self.add_parent(parent)

        self.operator_type = operator_type


    def to_sql(self):
        return self.operator_type

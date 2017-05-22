from sql import SQLNode
from sql import SQLNodeType
from sql import OperatorNodeType


class OperatorNode(SQLNode):
    def __init__(self, child=None, operator_type=OperatorNodeType.EQUAL):
        super(OperatorNode, self).__init__(SQLNodeType.OPERATOR_NODE, "operator")
        self.add_child(child)
        self.operator_type = operator_type


    def to_sql(self):
        return self.operator_type

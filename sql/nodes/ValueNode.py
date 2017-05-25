from sql.nodes.SQLNode import SQLNode
from sql.nodes.SQLNodeType import SQLNodeType
from sql.nodes.OperatorNodeType import OperatorNodeType


class ValueNode(SQLNode):
    """
    Can have multiple children, requires value and table.
    Default Operator is =

    value_node = ValueNode('hannan', 'students.first_name')
    value_node.to_sql()
    => students.first_name = 'hannan'

    value_node = ValueNode('2014', 'terms.year', OperatorNodeType.GREATER_THAN)
    value_node.to_sql()
    => terms.year > 2014

    """
    def __init__(self, label, attribute, operator=OperatorNodeType.EQUAL, child=None, parent=None):
        super(ValueNode, self).__init__(SQLNodeType.VALUE_NODE, label, "where")

        self.add_child(child)
        self.add_parent(parent)

        self.attribute = attribute
        self.operator = operator


    def __repr__(self):
        return "%s['%s','%s','%s']" % (type(self).__name__, self.label,
                                       self.operator, self.attribute)

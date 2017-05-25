from sql.nodes.SQLNodeType import SQLNodeType
from sql.nodes.SQLNode import SQLNode


class TableNode(SQLNode):
    """
    Can have multiple children. Requires a label.

    table_node = TableNode('students')
    table_node.to_sql()
    => students

    """
    def __init__(self, label, child=None, parent=None):
        super(TableNode, self).__init__(SQLNodeType.TABLE_NODE, label, "tables")

        self.add_child(child)
        self.add_parent(parent)

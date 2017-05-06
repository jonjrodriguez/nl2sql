from SQLNodeType import SQLNodeType
from SQLNodeMultiChild import SQLNodeMultiChild


class TableNode(SQLNodeMultiChild):
    """
    Can have multiple children. Requires a label.

    table_node = TableNode('students')
    table_node.to_sql()
    => students

    """
    def __init__(self, label, child = None):
        SQLNodeMultiChild.__init__(self, SQLNodeType.TABLE_NODE, label)
        self.add_child(child)

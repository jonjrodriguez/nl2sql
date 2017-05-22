from sql.SQLNodeMultiChild import SQLNodeMultiChild
from sql.SQLNodeType import SQLNodeType

class SelectNode(SQLNodeMultiChild):
    """
    Usually the root node, this is a node of type select. Start with
    this node, and add children nodes to it (one at a time).

    root = SelectNode()
    attribute_node = AttributeNode()
    table_node = TableNode("students")

    attribute_node.add_child(table_node)
    root.add_child(attribute_node)

    SQLTree.get_sql(root)

    => SELECT * FROM 'students';

    """
    def __init__(self, label="SELECT", child=None, parent=None):
        super(SelectNode, self).__init__(SQLNodeType.SELECT_NODE, label)

        self.add_child(child)
        self.add_parent(parent)


    def to_sql(self):
        return "SELECT"

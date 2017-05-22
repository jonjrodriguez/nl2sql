from sql.SQLNode import SQLNode

class SQLNodeMultiChild(SQLNode):
    """
    This class enforces a list as a child. Children nodes are added to this list
    """
    def __init__(self, node_type, label, child=[], parent=None):
        super(SQLNodeMultiChild, self).__init__(node_type, label, child, parent)


    def add_child(self, child):
        if child is not None:
            self.child.append(child)

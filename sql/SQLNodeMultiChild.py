from SQLNode import SQLNode

class SQLNodeMultiChild(SQLNode):
    """
    This class enforces a list as a child. Children nodes are added to this list
    """
    def __init__(self, type, label, child = None):
        SQLNode.__init__(self, type,label)
        if child is None:
            self.child = []


    def add_child(self,child):
        if child is not None:
            self.child.append(child)

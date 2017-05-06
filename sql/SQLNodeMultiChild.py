from SQLNode import SQLNode

class SQLNodeMultiChild(SQLNode):
    def __init__(self, type, label, child = []):
        SQLNode.__init__(self, type,label, child)


    def add_child(self,child):
        if child is not None:
            self.child.append(child)

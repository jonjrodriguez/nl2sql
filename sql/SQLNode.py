class SQLNode(object):
    """
    The base SQL node, this doesn't have a type, this is inherited by all other
    classes. This doesnt assume anything on the child, could be one or many.
    """
    def __init__(self, node_type, label, child=None, parent=None):
        self.type = node_type
        self.label = label
        self.child = child
        self.parent = parent


    def add_child(self, child):
        self.child = child


    def get_child(self):
        return self.child


    def add_parent(self, parent):
        self.parent = parent


    def get_parent(self):
        return self.parent


    def to_sql(self):
        return self.label

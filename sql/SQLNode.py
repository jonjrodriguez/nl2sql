class SQLNode(object):
    """
    The base SQL node, this doesn't have a type, this is inherited by all other
    classes. This doesnt assume anything on the child, could be one or many.
    """
    def __init__(self, node_type, label, child=None):
        self.type = node_type
        self.label = label
        self.child = child


    def add_child(self, child):
        self.child = child


    def get_child(self):
        return self.child


    def to_sql(self):
        return self.label

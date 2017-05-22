from nltk import Tree

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


    def pretty_print(self):
        tree = Tree.fromstring(str(self))
        tree.pretty_print(maxwidth=32)


    def __repr__(self):
        return "%s['%s']" % (type(self).__name__, self.label)


    def __str__(self):
        childstrs = []
        children = self.child if isinstance(self.child, list) else [self.child]

        for child in children:
            childstrs.append(str(child))

        if not childstrs:
            return '%s' % (repr(self))

        return '(%s %s)' % (repr(self), " ".join(childstrs))

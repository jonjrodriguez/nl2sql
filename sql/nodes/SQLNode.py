from nltk import Tree

class SQLNode(object):
    """
    The base SQL node, this doesn't have a type, this is inherited by all other
    classes. This doesnt assume anything on the child, could be one or many.
    """
    def __init__(self, node_type, label, sql_lbl, children=None, parent=None):
        self.type = node_type
        self.label = label
        self.parent = parent
        self.sql_label = sql_lbl

        self.children = [] if children is None else children


    def add_child(self, child):
        if child is None:
            return

        if isinstance(child, list):
            self.children += child
        else:
            self.children.append(child)


    def get_children(self):
        return self.children


    def add_parent(self, parent):
        self.parent = parent


    def get_parent(self):
        return self.parent


    def pretty_print(self):
        tree = Tree.fromstring(str(self))
        tree.pretty_print(maxwidth=100)


    def __repr__(self):
        return "%s['%s']" % (type(self).__name__, self.label)


    def __str__(self):
        childstrs = []

        for child in self.children:
            if child.children:
                childstrs.append(str(child))
            else:
                childstrs.append('%s' % (repr(child)))

        if not childstrs:
            return '(%s)' % (repr(self))

        return '(%s %s)' % (repr(self), " ".join(childstrs))

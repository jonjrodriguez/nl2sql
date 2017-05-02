class NodeType(object):
    TABLE = 1
    ATTRIBUTE = 2


class Node(object):
    def __init__(self, table, attribute=None):
        self.table = table
        self.attribute = attribute

        if attribute is None:
            self.type = NodeType.TABLE
            self.label = self.table
        else:
            self.type = NodeType.ATTRIBUTE
            self.label = "%s.%s" % (self.table, self.attribute)

        self.attributes = []
        self.relations = []


    def add_attribute(self, node):
        self.attributes.append(node.label)


    def add_relation(self, node, self_key, foreign_key):
        self.relations.append((node.label, self_key, foreign_key))

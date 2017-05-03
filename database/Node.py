class NodeType(object):
    TABLE = 1
    ATTRIBUTE = 2


class Node(object):
    def __init__(self, table, attribute=None):
        self.table = table

        if attribute is None:
            self.type = NodeType.TABLE
            self.label = self.table
            self.attributes = []
            self.relations = []
        else:
            self.attribute = attribute
            self.type = NodeType.ATTRIBUTE
            self.label = "%s.%s" % (self.table, self.attribute)


    def add_attribute(self, node):
        if self.type is not NodeType.TABLE:
            raise TypeError("Attribute Node does not contain attributes")

        self.attributes.append(node.label)


    def add_relation(self, node, self_key, foreign_key):
        if self.type is not NodeType.TABLE:
            raise TypeError("Attribute Node does not contain relations")

        self.relations.append((node.label, self_key, foreign_key))

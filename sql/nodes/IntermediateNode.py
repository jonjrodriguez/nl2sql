from sql.nodes.SQLNodeType import SQLNodeType
from sql.nodes.SQLNode import SQLNode


class IntermediateNode(SQLNode):
    def __init__(self, node_type, label, choices, child=None, parent=None):
        super(IntermediateNode, self).__init__(SQLNodeType.INTERMEDIATE_NODE, label, 'intermediate')

        self.type = node_type
        self.choices = choices
        self.add_child(child)
        self.add_parent(parent)


    def __repr__(self):
        return "%s%s[%s:'%s']" % (self.type.title(), type(self).__name__, self.label,
                                  ",".join([tag[0] for tag in self.choices]))

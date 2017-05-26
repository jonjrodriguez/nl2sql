from sql.nodes.ValueNode import ValueNode


class NodeReducer(object):
    def __init__(self):
        self.tree = None


    def __call__(self, tree):
        self.tree = tree

        self.reduce_tree(self.tree)

        return self.tree


    def reduce_tree(self, node):
        if isinstance(node, ValueNode):
            self.check_child(node)

        for child in node.children:
            self.reduce_tree(child)


    def check_child(self, node):
        for child in node.children:
            if not isinstance(child, ValueNode):
                continue

            if node.attribute == child.attribute:
                node.label = "%s %s" % (child.label, node.label)
                self.remove_node(child)


    def remove_node(self, node):
        parent = node.parent
        children = node.children

        parent.children = [child for child in parent.children if child != node]
        parent.children += children

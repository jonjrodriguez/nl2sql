from sql import AttributeNode, SelectNode, TableNode, SQLTree, FunctionNode, FunctionNodeType

class NodeGenerator(object):
    def __init__(self):
        pass

    def __call__(self, doc):
        self.tree = SelectNode()
        for parse in doc['parse']:
            self.tree.add_child(self.parseTuple(tuple(parse)))

        print SQLTree(self.tree).get_sql()

    def parseTuple(self, tpl):
        if (type(tpl) == tuple):
            k, v = tpl
            new_node = self.parseTuple(k)
            if new_node:
                new_node.add_child(self.parseTuple(v))

            return new_node
        else:
            return self.getNodeType(tpl)


    def getNodeType(self, node):
        if node:
            if (node[0] == "LIST"):
                return AttributeNode()

            if (node[0] == "COUNT"):
                return FunctionNode(None, FunctionNodeType.COUNT)

            # Sections would have been identified as a table
            # And not hardcoded like this
            if (node[0]) == "sections":
                return TableNode("Sections")
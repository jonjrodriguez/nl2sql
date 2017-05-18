from sql import AttributeNode, SelectNode, TableNode, SQLTree, FunctionNode, FunctionNodeType
from utils import *
from nltk.tree import Tree

class NodeGenerator(object):
    def __init__(self):
        pass

    def __call__(self, doc):
        self.tree = SelectNode()
        self.db_results = doc['db_schema']

        parse = doc['parse']

        if (type(parse) == Tree):
            print "Printing element " + str(parse) + " With length of " + str(len(parse))

            for i in range(0, len(parse)):
                if parse[i]:
                    if (type(parse[i]) == Tree):
                        result = self.parseTree(parse[i])
                    else:
                        result = self.getNodeType(parse[i])

                    if result:
                        self.tree.add_child(result)

# How many students are registered for Constitutional Law?
# How many students are in Constitutional Law?

        print SQLTree(self.tree).get_sql()

    def parseTree(self, tpl):
        print "Called Parse for: " + str(tpl) + " With type of: " + str(type(tpl))
        if (type(tpl) == Tree):
            print "Printing element " + str(tpl) + " With length of " + str(len(tpl))

            new_tree = None
            for i in range(0, len(tpl)):
                print "Index " + str(i) + r"\r\n"
                if tpl[i]:
                    result = self.parseTree(tpl[i])

                    if new_tree:
                        print "Adding result of type: " + str(type(result)) + " to existing new tree object"
                        new_tree.add_child(result)
                    else:
                        print "Creating new_tree object with type: " + str(type(result))
                        new_tree = result

            return new_tree

        else:
            print "Getting node type for " + str(tpl)
            result = self.getNodeType(tpl)
            print "Found a type object of: " + str(type(result))
            return result



    def getNodeType(self, node):
        token = node

        if node:
            if (token == LIST_TYPE_NAME):
                return AttributeNode()

            elif (token == COUNT_TYPE_NAME):
                return FunctionNode(None, FunctionNodeType.COUNT)

            else:
                for result in self.db_results:
                    word, values = result
                    if (word == token):
                        for value in values:
                            term, score = value
                            if "." in term:
                                # This could be a value node or an attribute node
                                # If attribute node, find the
                                return AttributeNode(term)
                            else:
                                return TableNode(term)
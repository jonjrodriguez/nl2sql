from sql.AttributeNode import AttributeNode
from sql.FunctionNode import FunctionNode
from sql.FunctionNodeType import FunctionNodeType
from sql.SelectNode import SelectNode
from sql.TableNode import TableNode
from sql.ValueNode import ValueNode
from communicate import Communicator
from nltk.tree import ParentedTree

class NodeGenerator(object):
    def __init__(self):
        self.communicator = Communicator()
        self.threshold = 0.6

    def __call__(self, doc):
        self.tags = doc['tagged']
        doc['tree'] = self.generateTree(doc['dep_parse'].root, doc)

    def generateTree(self, node, doc):
        tree = self.getNodeType(node['word'])

        for key in node['deps'].items():
            tag, dep_index = key
            idx = int(dep_index[0])

            if doc['dep_parse'].nodes[idx]:
                result = self.generateTree(doc['dep_parse'].nodes[idx], doc)
                if result:
                    if tree:
                        tree.add_child(result)
                    else:
                        tree == result

        return tree

    def getNodeType(self, node):
        if (type(node) == ParentedTree):
            return None

        # Node will be passed in as a Unicode type
        token = str(node)

        # First check is to see if the token has been tagged
        # By any of our classifiers. If it hasn't we can ignore
        # The token
        if not node in self.tags:
            return None

        nodeType = self.tags[token]['type']
        nodeTag = self.tags[token]['tags']

        # This next check is to if the tag that was given to the token
        # Is part of a larger tag. (i.e. 'How many' would be 2 tokens where
        # The tag for 'How' would be null and the tag for 'many' would be COUNT)
        # We want to ignore all null node tags
        if (str(nodeTag) == "IGN"):
            return None

        if ((nodeType == "schema") or (nodeType == "corpus")):
            return self.getDbNode(nodeType, nodeTag, token)

        elif (nodeType == "grammar"):
            return self.getGrammarNode(nodeType, nodeTag)

        # This is where the operator node will also be generated

        else:
            return None

    def getGrammarNode(self, nodeType, nodeTag):
        if not nodeType == "grammar":
            return None

        tag = str(nodeTag)
        if tag == "SELECT":
            return SelectNode()
        elif tag == "LIST":
            return AttributeNode()
        elif tag == "COUNT":
            return FunctionNode(None, FunctionNodeType.COUNT)

    def getDbNode(self, nodeType, nodeTag, token):

        if not ((nodeType == "schema") or (nodeType == "corpus")):
            return None

        selected_term = 0

        # Because the Node Type for this object is either Schema or Corpus
        # We can safely make the assumption that the Node Tag will be a list
        term, score = nodeTag[0]

        # For tags that come back with a very low score, this will be used
        # To interact with the user to confirm what the query is referring to
        if (score <= self.threshold):
            self.communicator.refineResult(token, nodeTag)

        term, score = nodeTag[int(selected_term)]

        if (nodeType == "corpus"):
            attributes = term.split(".")
            table = attributes[0]
            vn = ValueNode(term)
            vn.add_child(TableNode(table))
            return vn

        if (nodeType == "schema"):
            if "." in term:
                attributes = term.split(".")
                table = attributes[0]
                an = AttributeNode(term)
                an.add_child(TableNode(table))
                return an
            else:
                return TableNode(term)
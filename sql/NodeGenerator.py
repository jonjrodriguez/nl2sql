from sql.AttributeNode import AttributeNode
from sql.FunctionNode import FunctionNode
from sql.FunctionNodeType import FunctionNodeType
from sql.SelectNode import SelectNode
from sql.TableNode import TableNode
from sql.ValueNode import ValueNode
from sql.LimitNode import LimitNode
from nltk.tree import ParentedTree
from sql.OperatorNode import OperatorNode
from sql.OperatorNodeType import OperatorNodeType

class NodeGenerator(object):
    def __init__(self, communicator, threshold=0.6):
        self.communicator = communicator
        self.threshold = threshold
        self.tagged = {}


    def __call__(self, doc):
        self.tagged = doc['tagged']
        return self.generate_tree(doc['dep_parse'].root, doc)


    def generate_tree(self, node, doc):
        tree = self.get_node_type(node['word'])

        for key in node['deps'].items():
            _, dep_index = key
            idx = int(dep_index[0])

            if doc['dep_parse'].nodes[idx]:
                result = self.generate_tree(doc['dep_parse'].nodes[idx], doc)
                if result:
                    if tree:
                        tree.add_child(result)
                    else:
                        tree = result

        return tree


    def get_node_type(self, node):
        if isinstance(node, ParentedTree):
            return None

        # Node will be passed in as a Unicode type
        token = str(node)

        # First check is to see if the token has been tagged
        # By any of our classifiers. If it hasn't we can ignore
        # The token
        if not node in self.tagged:
            return None

        node_type = self.tagged[token]['type']
        node_tag = self.tagged[token]['tags']

        # This next check is to if the tag that was given to the token
        # Is part of a larger tag. (i.e. 'How many' would be 2 tokens where
        # The tag for 'How' would be null and the tag for 'many' would be COUNT)
        # We want to ignore all null node tags
        if str(node_tag) == "IGN":
            return None

        if (node_type == "schema") or (node_type == "corpus"):
            return self.get_db_node(node_type, node_tag, token)

        if node_type == "grammar":
            return self.get_grammar_node(node_type, node_tag, token)

        # This is where the operator node will also be generated
        return None


    @staticmethod
    def get_grammar_node(node_type, node_tag, token):
        if not node_type == "grammar":
            return None

        tag = str(node_tag)
        if tag == "SELECT":
            return SelectNode()
        elif tag == "LIST":
            return AttributeNode()
        elif tag == "COUNT":
            return FunctionNode(None, FunctionNodeType.COUNT)
        elif tag == "LIMIT":
            limit = 0
            if token.lower() == "all":
                limit = 1000 # Assuming this is all we want to return for 'All'
            else:
                if token.isdigit():
                    limit = int(token)
            return LimitNode(limit)
        elif tag == "EQUAL":
            return OperatorNode()
        elif tag == "LESS_THAN":
            return OperatorNode(OperatorNodeType.LESS_THAN)
        elif tag == "GREATER_THAN":
            return OperatorNode(OperatorNodeType.GREATER_THAN)


    def get_db_node(self, node_type, node_tag, token):
        if not ((node_type == "schema") or (node_type == "corpus")):
            return None

        # Because the Node Type for this object is either Schema or Corpus
        # We can safely make the assumption that the Node Tag will be a list
        term, score = node_tag[0]

        # For tags that come back with a very low score, this will be used
        # To interact with the user to confirm what the query is referring to
        selected = 0 if score > self.threshold else self.communicator.choose(token, node_tag)

        term, score = node_tag[int(selected)]

        if node_type == "corpus":
            attribute_node = AttributeNode(term)
            attribute_node.add_child(ValueNode(token))
            return attribute_node


        if node_type == "schema":
            if "." in term:
                return AttributeNode(term)
            else:
                return TableNode(term)

from sql.nodes.AttributeNode import AttributeNode
from sql.nodes.FunctionNode import FunctionNode
from sql.nodes.FunctionNodeType import FunctionNodeType
from sql.nodes.SelectNode import SelectNode
from sql.nodes.TableNode import TableNode
from sql.nodes.ValueNode import ValueNode
from sql.nodes.LimitNode import LimitNode
from sql.nodes.IntermediateNode import IntermediateNode
from sql.NodeSelector import NodeSelector
from sql.NodeReducer import NodeReducer


class NodeGenerator(object):
    def __init__(self, communicator):
        self.communicator = communicator

        self.tagged = {}
        self.parse = None

        selector = NodeSelector(communicator)
        reducer = NodeReducer()

        self.pipeline = [selector, reducer]


    def __call__(self, doc):
        self.tagged = doc['tagged']
        self.parse = doc['dep_parse']

        tree = self.generate_tree(self.parse.root)

        for process in self.pipeline:
            tree = process(tree)

        return tree


    def generate_tree(self, node):
        tree = self.get_node_type(node)

        for _, key in node['deps'].items():
            idx = int(key[0])

            result = self.generate_tree(self.parse.nodes[idx])
            if not result:
                continue

            if tree:
                tree.add_child(result)
                result.add_parent(tree)
            else:
                tree = result

        return tree


    def get_node_type(self, node):
        token = node['word']

        # First check is to see if the token has been tagged
        # By any of our classifiers. If it hasn't we can ignore
        # The token
        if not token in self.tagged:
            return None

        node_type = self.tagged[token]['type']
        node_tag = self.tagged[token]['tags']

        # Ignore tokens tagged as IGN
        if node_tag == "IGN":
            return None

        # Dynamically create method to call
        method_name = "get_%s_node" % node_type
        try:
            method = getattr(self, method_name)
        except AttributeError:
            self.communicator.error("No method for node type: %s" % node_type)

        return method(node, node_tag)


    def get_grammar_node(self, node, tag):
        token = node['word']

        if tag == "SELECT":
            return SelectNode()

        if tag == "COUNT":
            return FunctionNode(func_type=FunctionNodeType.COUNT)

        if tag == "LIMIT":
            return LimitNode(token)

        self.communicator.error("Not handling grammar tag: %s" % tag)


    @staticmethod
    def get_schema_node(node, tags):
        token = node['word']

        # Because the Node Type for this object is either Schema or Corpus
        # We can safely make the assumption that the Node Tag will be a list
        tag, score = tags[0]

        if score < 1.0:
            return IntermediateNode('schema', token, tags)

        if "." in tag:
            return AttributeNode(tag)
        else:
            return TableNode(tag)


    @staticmethod
    def get_corpus_node(node, tags):
        token = node['word']

        # Because the Node Type for this object is either Schema or Corpus
        # We can safely make the assumption that the Node Tag will be a list
        tag, score = tags[0]

        if score < 1.0:
            return IntermediateNode('corpus', token, tags)

        return ValueNode(token, tag)

from sql.nodes.IntermediateNode import IntermediateNode
from sql.nodes.AttributeNode import AttributeNode
from sql.nodes.TableNode import TableNode
from sql.nodes.ValueNode import ValueNode


class NodeSelector(object):
    def __init__(self, communicator):
        self.communicator = communicator


    def __call__(self, tree):
        for node in self.intermediate_nodes(tree):
            choices = self.create_choices(node)
            choice = 0 if len(choices) == 1 else self.communicator.choose(node.label, choices)
            self.update_tree(node, choices[choice])


    def create_choices(self, node):
        label = None
        choices = []

        if node.type == 'schema':
            for child in node.children:
                if isinstance(child, TableNode):
                    label = child.label
                    break

        choices = [choice[0] for choice in node.choices]
        if label:
            choices = [choice for choice in choices if label in choice]

        return choices


    def update_tree(self, node, choice):
        if node.type == 'schema':
            if '.' in choice:
                new_node = AttributeNode(choice)
            else:
                new_node = TableNode(choice)

        if node.type == 'corpus':
            new_node = ValueNode(node.label, choice)

        self.replace_node(node, new_node)


    @staticmethod
    def replace_node(node, new_node):
        parent = node.parent
        children = node.children

        new_node.parent = parent
        new_node.children = children

        for child in children:
            child.parent = new_node

        parent.children = [new_node if child == node else child for child in parent.children]


    def intermediate_nodes(self, tree):
        while True:
            intermediate = self.find_first_choice(tree)
            if not intermediate:
                break

            yield intermediate


    def find_first_choice(self, tree):
        if isinstance(tree, IntermediateNode):
            return tree

        for child in tree.children:
            return self.find_first_choice(child)

        return None

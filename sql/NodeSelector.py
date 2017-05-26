from sql.nodes.IntermediateNode import IntermediateNode
from sql.nodes.AttributeNode import AttributeNode
from sql.nodes.TableNode import TableNode
from sql.nodes.ValueNode import ValueNode


class NodeSelector(object):
    def __init__(self, communicator):
        self.communicator = communicator
        self.tree = None


    def __call__(self, tree):
        self.tree = tree

        for node in self.intermediate_nodes():
            choices = self.create_choices(node)
            choice = 0 if len(choices) == 1 else self.communicator.choose(node.label, choices)
            self.update_tree(node, choices[choice])

        return self.tree


    def create_choices(self, node, threshold=.5):
        label = None

        # Return single choice if only one item is above threshold
        choices = [choice[0] for choice in node.choices if choice[1] > threshold]
        if len(choices) == 1:
            return choices

        if node.type == 'schema':
            for child in node.children:
                if isinstance(child, TableNode):
                    label = child.label
                    break

        if node.type == 'corpus':
            if isinstance(node.parent, ValueNode):
                label = node.parent.attribute.split(".")[0]

        choices = [choice[0] for choice in node.choices]
        filtered_choices = []

        if label:
            filtered_choices = [choice for choice in choices if label in choice]

        return filtered_choices or choices


    def update_tree(self, node, choice):
        if node.type == 'schema':
            if '.' in choice:
                new_node = AttributeNode(choice)
            else:
                new_node = TableNode(choice)

        if node.type == 'corpus':
            new_node = ValueNode(node.label, choice)

        self.replace_node(node, new_node)


    def replace_node(self, node, new_node):
        parent = node.parent
        children = node.children

        new_node.parent = parent
        new_node.children = children

        for child in children:
            child.parent = new_node

        if parent:
            parent.children = [new_node if child == node else child for child in parent.children]
        else:
            self.tree = new_node


    def intermediate_nodes(self):
        while True:
            intermediate = self.find_first_choice(self.tree)
            if not intermediate:
                break

            yield intermediate


    def find_first_choice(self, tree):
        if isinstance(tree, IntermediateNode):
            return tree

        for child in tree.children:
            intermediate = self.find_first_choice(child)
            if intermediate:
                return intermediate

        return None

import cPickle as pickle
from database.Node import Node

class SchemaGraph(object):
    def __init__(self, file_path=None):
        if file_path is None:
            self.graph_dict = {}
        else:
            self.graph_dict = pickle.load(open(file_path, "rb"))


    def get_node(self, label):
        return self.graph_dict[label]


    def nodes(self, type=None):
        if type is None:
            return self.graph_dict.keys()

        return [node.label for node in self.graph_dict.values() if node.type == type]


    def add_node(self, node):
        if node.label not in self.graph_dict:
            self.graph_dict[node.label] = node

    def get_direct_path(self, table_name_a, table_name_b):
        queue = [(table_name_a, [])]
        while queue:
            (vertex, path) = queue.pop(0)
            node = self.get_node(vertex)
            for next in node.relations:
                if next[0] == table_name_b:
                    return path + [next]
                else:
                    queue.append((next[0], path + [next]))

    def construct(self, database, file_path):
        for (table_name,) in database.get_tables():
            table = Node(table_name)
            self.add_node(table)

            fields = database.get_fields(table_name)
            for field in fields:
                attribute = Node(table_name, field[0])
                table.add_attribute(attribute)
                self.add_node(attribute)

        for table, self_key, _, foreign_table, foreign_key in database.get_foreign_keys():
            table_node = self.get_node(table)
            foreign_node = self.get_node(foreign_table)

            table_node.add_relation(foreign_node, self_key, foreign_key)
            foreign_node.add_relation(table_node, foreign_key, self_key)

        pickle.dump(self.graph_dict, open(file_path, "wb"))

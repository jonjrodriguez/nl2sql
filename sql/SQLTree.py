from SelectNode import SelectNode
from AttributeNode import AttributeNode
from FunctionNode import FunctionNode
from FunctionNodeType import FunctionNodeType
from TableNode import TableNode
from SQLNodeType import SQLNodeType


class SQLTree(object):
    def __init__(self,root):
        self.root = root

    def get_sql(self):
        if not self.root.type is SQLNodeType.SELECT_NODE:
            raise ValueError("Root type is not SELECT_NODE")
        self.select = self.root.to_sql()
        print self.root.get_child()
        self.get_attributes_and_tables(self.root.get_child())
        return " ".join([self.select, self.attributes, "FROM", self.tables, ";"])

    def get_attributes_and_tables(self,second_level):
        if not second_level:
            return None
            
        if second_level[0].type is SQLNodeType.ATTRIBUTE_NODE:
            self.set_attributes(second_level)
            self.set_tables_from_attributes(second_level)
        elif second_level[0].type is SQLNodeType.FUNCTION_NODE:
            self.attributes = second_level[0].to_sql()
            if second_level[0].get_child().type is SQLNodeType.TABLE_NODE:
                self.tables = second_level[0].get_child().to_sql()
            elif second_level[0].get_child().type is SQLNodeType.VALUE_NODE:
                self.tables = second_level[0].get_child().to_sql()
            else:
                self.set_tables_from_attributes([second_level[0]])


    def set_attributes(self,second):
        if not self.all_child_same_type(second):
            raise ValueError("All children must be of same type")
        if not self.all_child_acceptable(second):
            raise ValueError("Child type is not ATTRIBUTE or TABLE Node")
        self.attributes = ",".join([x.to_sql() for x in second])

    def all_child_same_type(self,some_list):
        child_type = None
        for child in some_list:
            if child_type is None:
                child_type = child.type
            else:
                if not child_type is child.type:
                    return False
        return True

    def all_child_acceptable(self,some_list):
        for child in some_list:
            if child.type not in [SQLNodeType.ATTRIBUTE_NODE, SQLNodeType.TABLE_NODE]:
                return False
        return True

    def set_tables_from_attributes(self,second_level):
        flattened = [child2 for child in second_level for child2 in child.get_child() ]
        self.tables =  ",".join(set([x.to_sql() for x in flattened]))
#
#
# root = SelectNode()
# attribute_node = AttributeNode("*")
# table_node = TableNode("students")
# function_node = FunctionNode(table_node, FunctionNodeType.COUNT)
# #attribute_node.add_child(table_node)
# # attribute_node2 = AttributeNode("id")
# # table_node2 = TableNode("students")
# # attribute_node2.add_child(table_node2)
# root.add_child(function_node)
# # root.add_child(attribute_node2)
# print SQLTree(root).get_sql()

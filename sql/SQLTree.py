from sql.nodes.SQLNodeType import SQLNodeType


class SQLTree(object):
    def __init__(self, root):
        self.root = root


    def get_sql(self):
        if not self.root.type is SQLNodeType.SELECT_NODE:
            raise ValueError("Root type is not SELECT_NODE")

        select = self.root.to_sql()
        print self.root.get_child()

        attributes, tables = self.get_attributes_and_tables(self.root.get_child())

        return " ".join([select, attributes, "FROM", tables, ";"])


    def get_attributes_and_tables(self, second_level):
        if not second_level:
            return None

        if second_level[0].type is SQLNodeType.ATTRIBUTE_NODE:
            attributes = self.set_attributes(second_level)
            tables = self.set_tables_from_attributes(second_level)
        elif second_level[0].type is SQLNodeType.FUNCTION_NODE:
            attributes = second_level[0].to_sql()
            if second_level[0].get_child().type is SQLNodeType.TABLE_NODE:
                tables = second_level[0].get_child().to_sql()
            elif second_level[0].get_child().type is SQLNodeType.VALUE_NODE:
                tables = second_level[0].get_child().to_sql()
            else:
                tables = self.set_tables_from_attributes([second_level[0]])

        return attributes, tables


    def set_attributes(self, second):
        if not self.all_child_same_type(second):
            raise ValueError("All children must be of same type")

        if not self.all_child_acceptable(second):
            raise ValueError("Child type is not ATTRIBUTE or TABLE Node")

        return ",".join([x.to_sql() for x in second])


    def all_child_same_type(self, some_list):
        child_type = None
        for child in some_list:
            if child_type is None:
                child_type = child.type
            else:
                if not child_type is child.type:
                    return False
        return True


    def all_child_acceptable(self, some_list):
        for child in some_list:
            if child.type not in [SQLNodeType.ATTRIBUTE_NODE, SQLNodeType.TABLE_NODE]:
                return False
        return True


    def set_tables_from_attributes(self, second_level):
        flattened = [child2 for child in second_level for child2 in child.get_child()]
        return ",".join(set([x.to_sql() for x in flattened]))

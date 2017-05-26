import itertools
from sql.SelectNode import SelectNode
from sql.AttributeNode import AttributeNode
from sql.ValueNode import ValueNode


class SQLGenerator(object):
    def __init__(self, tree, schema_graph):
        self.node_dict = {}
        self.generateNodeDict(tree)
        self.schema_graph = schema_graph


    def generateNodeDict(self, node):
        if not node:
            return None

        if type(node) == SelectNode:
            self.generateNodeDict(node.children)
        elif type(node) == list:
            for nd in node:
                self.generateNodeDict(nd)
        elif type(node) == AttributeNode:
            values = node.label.split(".")
            if values:
                table = values[0]
                self.addToNodeDict("tables", table)
                self.addToNodeDict(node.sql_label, node.label)
                self.generateNodeDict(node.children)
        elif type(node) == ValueNode:
            values = node.attribute.split(".")
            table = values[0]
            self.addToNodeDict("tables", table)
            self.addToNodeDict(node.sql_label, "%s %s '%s'" % (node.attribute, node.operator, node.label))
            self.generateNodeDict(node.children)
        else:
            self.addToNodeDict(node.sql_label, node.label)
            self.generateNodeDict(node.children)


    def addToNodeDict(self, key, value):
        if key in self.node_dict:
            self.node_dict[key].add(value)
        else:
            self.node_dict[key] = {value}


    def getSQL(self):
        _select = "*"
        _from = ""
        _where = ""
        _limit = ""
        sql = ""

        if not self.node_dict['tables']:
            raise ValueError, "At least one table must be specified"

        self.getTableMappings(self.node_dict['tables'])

        for keyword, values in self.node_dict.iteritems():
            if keyword == "select":
                _select = ", ".join(values)
            elif keyword == "tables":
                _from  = ", ".join(values)
            elif keyword == "where":
                _where = " and ".join(values)
            elif keyword == "limit":
                _limit = max(values)

        sql = "SELECT %s" % _select
        sql += " FROM %s" % _from

        if _where:
            sql += " WHERE %s" % _where

        if _limit:
            sql += " LIMIT %s" % _limit


        return sql + ";"

    def getTableMappings(self, tables):
        if not self.schema_graph:
            raise Exception, "No Schema Graph was found"

        for table_a, table_b in itertools.combinations(tables, 2):
            relations = self.schema_graph.get_direct_path(table_a, table_b)
            
            for relation in relations:
                current_table_id = relation[1]
                next_table_id = relation[2]
                join_table = relation[0]
                self.addToNodeDict("tables", join_table)
                self.addToNodeDict("where", "%s.%s = %s.%s" % (table_a, current_table_id, join_table, next_table_id))
                table_a = relation[0]

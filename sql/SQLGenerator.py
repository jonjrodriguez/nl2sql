import pprint
from sql.SelectNode import SelectNode
from sql.AttributeNode import AttributeNode
from sql.ValueNode import ValueNode


class SQLGenerator(object):
    def __init__(self, tree):
        self.node_dict = {}
        self.generateNodeDict(tree)


    def generateNodeDict(self, node):
        if not node:
            return None

        if type(node) == SelectNode:
            self.generateNodeDict(node.children)
        elif type(node) == list:
            for nd in node:
                self.generateNodeDict(nd)
                #self.addToNodeDict(nd.sql_label, nd.label)
        elif type(node) == AttributeNode:
            values = node.label.split(".")
            if values:
                table = values[0]
                self.addToNodeDict("tables", table)
                self.addToNodeDict(node.sql_label, node.label)
                self.generateNodeDict(node.children)
        elif type(node) == ValueNode:
            values = node.attribute.split(".")
            if values:
                table = values[0]
                self.addToNodeDict("tables", table)
                self.addToNodeDict(node.sql_label, node.label)
                self.generateNodeDict(node.children)
            else:
                self.addToNodeDict(node.sql_label, node.label)
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
        _select = ""
        _from = ""
        _where = ""
        _limit = ""
        sql = ""

        for keyword, values in self.node_dict.iteritems():
            if keyword == "select":
                _select = ", ".join(values)
            elif keyword == "tables":
                _from  = ", ".join(values)
            elif keyword == "where":
                _where = ", ".join(values)
            elif keyword == "limit":
                _limit = ", ".join(values)

        if not _select:
            raise ValueError, "A Select Node is required"

        if not _from:
            raise ValueError, "At least one table must be specified"

        sql = "SELECT %s" % _select
        sql += " FROM %s" % _from

        if _where:
            sql += " WHERE %s" % _where

        if _limit:
            sql += " LIMIT %s" % _limit

        return sql

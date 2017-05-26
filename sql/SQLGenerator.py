import itertools
from sql.nodes.SelectNode import SelectNode
from sql.nodes.TableNode import TableNode
from sql.nodes.AttributeNode import AttributeNode
from sql.nodes.ValueNode import ValueNode


class SQLGenerator(object):
    def __init__(self, tree, schema_graph):
        self.node_dict = {}
        self.generate_node_dict(tree)
        self.schema_graph = schema_graph


    def generate_node_dict(self, node):
        if not node:
            return None

        if isinstance(node, AttributeNode):
            values = node.label.split(".")
            table = values[0]
            self.add_to_node_dict("tables", table)
            self.add_to_node_dict(node.sql_label, node.label)
        elif isinstance(node, ValueNode):
            values = node.attribute.split(".")
            table = values[0]
            self.add_to_node_dict("tables", table)
            self.add_to_node_dict(node.sql_label, "%s %s '%s'" % (node.attribute, node.operator,
                                                                  node.label))
        elif isinstance(node, TableNode):
            self.add_to_node_dict('tables', node.label)
            self.add_to_node_dict('froms', "%s.*" % node.label)
        elif not isinstance(node, SelectNode):
            self.add_to_node_dict(node.sql_label, node.label)

        for child in node.children:
            self.generate_node_dict(child)


    def add_to_node_dict(self, key, value):
        if key in self.node_dict:
            self.node_dict[key].add(value)
        else:
            self.node_dict[key] = {value}


    def get_sql(self):
        _select = ""
        _from = ""
        _where = ""
        _limit = ""
        sql = ""

        if not self.node_dict['tables']:
            raise ValueError, "At least one table must be specified"

        self.get_table_mappings(self.node_dict['tables'])

        for keyword, values in self.node_dict.iteritems():
            if keyword == "select":
                _select = ", ".join(values)
            elif keyword == "tables":
                _from = ", ".join(values)
            elif keyword == "where":
                _where = " and ".join(values)
            elif keyword == "limit":
                _limit = max(values)

        if not _select:
            _select = "*" if not 'forms' in self.node_dict else ", ".join(self.node_dict['froms'])

        sql = "SELECT %s" % _select
        sql += " FROM %s" % _from

        if _where:
            sql += " WHERE %s" % _where

        if _limit:
            sql += " LIMIT %s" % _limit


        return sql + ";"

    def get_table_mappings(self, tables):
        if not self.schema_graph:
            raise Exception, "No Schema Graph was found"

        for table_a, table_b in itertools.combinations(tables, 2):
            relations = self.schema_graph.get_direct_path(table_a, table_b)

            for relation in relations:
                current_table_id = relation[1]
                next_table_id = relation[2]
                join_table = relation[0]
                self.add_to_node_dict("tables", join_table)
                self.add_to_node_dict("where", "%s.%s = %s.%s" % (table_a, current_table_id,
                                                                  join_table, next_table_id))
                table_a = relation[0]

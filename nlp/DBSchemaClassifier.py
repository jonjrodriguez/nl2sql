from math import sqrt
from nlp.utils import jaccard_sim, wup_sim
from database import NodeType

class DBSchemaClassifier(object):
    """
    Find tokens that are similiar to database tables or column names
    """
    def __init__(self, schema_graph):
        self.nodes = [schema_graph.get_node(label) for label in schema_graph.nodes()]


    def __call__(self, doc):
        doc['db_schema'] = self.find_db_matches(doc['sanitized_text'].split())


    def find_db_matches(self, tokens, cutoff=.7, table=''):
        nodes = [node for node in self.nodes if node.label.startswith(table)]

        matches = []
        for word in tokens:
            matches.append((word, self.most_sim_node(word, cutoff, nodes)))

        return matches


    def most_sim_node(self, word, cutoff, nodes):
        matches = []
        for node in nodes:
            name = node.table if node.type == NodeType.TABLE else node.attribute

            sim = self.similarity(word, name)

            if sim >= cutoff:
                matches.append((node.label, sim))

        return sorted(matches, key=lambda x: x[1], reverse=True)


    def similarity(self, word1, word2):
        wup = wup_sim(word1, word2)
        jaccard = jaccard_sim(word1, word2)

        return max(wup, sqrt(jaccard))

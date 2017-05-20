import re
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
        trees = [tree.leaves() for tree in doc['parse'].subtrees(self.filter_tree)]
        tokens = [token for leaves in trees for token in leaves if token not in doc['tagged']]

        matches = [match for match in self.find_db_matches(tokens) if match[1]]

        for match in matches:
            doc['tagged'][match[0]] = {
                'type': 'schema',
                'tags': match[1]
            }


    def find_db_matches(self, tokens, cutoff=.8, table=''):
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


    @staticmethod
    def similarity(word1, word2):
        wup = wup_sim(word1, word2)
        jaccard = jaccard_sim(word1, word2)

        return max(wup, sqrt(jaccard))


    @staticmethod
    def filter_tree(tree):
        """
        Filters parse tree to Nouns located in Noun Phrases
        May need to expand or remove this filter
        """
        if tree.parent() is None:
            return False

        noun_phrase = re.match("NP|WHNP", tree.parent().label())
        noun = re.match("NN.*", tree.label())

        return noun_phrase and noun

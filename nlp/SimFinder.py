from math import sqrt
from nltk.corpus import wordnet
from nltk.metrics import jaccard_distance
from database import NodeType

class SimFinder(object):
    """
    Finds the similarity between words
    """
    def __init__(self, schema_graph):
        self.nodes = [schema_graph.get_node(label) for label in schema_graph.nodes()]
    

    def __call__(self, doc):
        doc['db_matches'] = self.find_db_matches(doc['tokens'])


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
        wup_sim = self.wup_sim(word1, word2)
        jaccard_sim = self.jaccard_sim(word1, word2)

        return max(wup_sim, jaccard_sim)


    def wup_sim(self, word1, word2):
        synset1 = wordnet.synsets(word1)
        synset2 = wordnet.synsets(word2)

        if not synset1 or not synset2:
            return 0
        
        if synset1[0] == synset2[0]:
            return 1.0

        return wordnet.wup_similarity(synset1[0], synset2[0])

 
    def jaccard_sim(self, word1, word2):
        set1 = set(word1)
        set2 = set(word2)
 
        coefficient = 1 - jaccard_distance(set1, set2)

        return sqrt(coefficient)

import re
from utils import ALL_TYPES


class QuestionChunker(object):
    def __init__(self):
        pass

    def __call__(self, doc):
        self.classify(doc['text'])

    def classify(self, sentence):
        Matches = []
        for feature_type, expression in ALL_TYPES.iteritems():
            p = re.compile(expression, re.IGNORECASE)
            if p.match(sentence):
                Matches.append(feature_type)
        print("All Matches")
        print(Matches)
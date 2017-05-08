import re
from utils import ALL_TYPES


class NodeGenerator(object):
    def __init__(self):
        pass

    def __call__(self, doc):
        self.getNodeType(doc['text'])

    def getNodeType(self, word):
        for feature_type, expression in ALL_TYPES.iteritems():
            if (feature_type == "OPERATOR"):
                for operator_type, expr in expression:
                    p = re.compile(expression, re.IGNORECASE)
                    if p.match(word):
                        return feature_type

            p = re.compile(expression, re.IGNORECASE)
            if p.match(word):
                return feature_type
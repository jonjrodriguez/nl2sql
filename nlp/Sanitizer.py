import re
from utils import ALL_TYPES


class Sanitizer(object):
    def __init__(self):
        pass

    def __call__(self, doc):
        doc['sanitized_text'] = self.Saznitize(doc['text'])


    def Saznitize(self, sentence):
        result = sentence.lower()

        for feature_type, expression in ALL_TYPES.iteritems():
            p = re.search(expression, result)
            if p:
                match = p.groups()[0]
                if (feature_type == "STOP"):
                    result = result.replace(match, "")
                else:
                    result = result.replace(match, feature_type)
        return result
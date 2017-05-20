import math, re
from utils import merge_results
from ClassifierExpressions import ALL_TYPES


class QuestionClassifier(object):
    """
    Classify tokens based on Regular Expressions
    """
    def __init__(self):
        pass


    def __call__(self, doc):
        doc['tagged'] = self.classify(doc)


    def classify(self, doc):
        unigrams = doc['tokens']
        bigrams = self.createNGram(unigrams, 2)
        trigrams =  self.createNGram(unigrams, 3)
        results = {}

        for token in unigrams + bigrams + trigrams:
            result = self.classifyToken(token)
            if result:
                results = merge_results(results, result)
        return results


    def createNGram(self, tokens, length):
        grams = []

        for i in range(length - 1, len(tokens) - 1):
            result = ""

            for j in range(length -1, -1, -1):
                result += tokens[abs(i - j)] + " "

            grams.append(result.rstrip())
        return grams


    def classifyToken(self, token):
        for feature_type, expression in ALL_TYPES.iteritems():
            m = re.compile(expression, re.IGNORECASE)
            if m.match(token):
                result = {}
                tokens = token.split()
                tokenLen = len(tokens)
                
                if (tokenLen > 1):
                    for i in range(0, tokenLen):
                        if (i == tokenLen - 1):
                            result[tokens[i]] = {
                                'type': 'question_classifier',
                                'tags': feature_type
                            }
                        else:
                            result[tokens[i]] = {
                                'type': 'question_classifier',
                                'tags': 'null'
                            }
                else:
                    result[tokens[0]] = {
                                'type': 'question_classifier',
                                'tags': feature_type
                            }
                return result

        return None

        